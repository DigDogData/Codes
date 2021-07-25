# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# install package "EBImage" from bioconductor.org
#source("https://bioconductor.org/biocLite.R")
#biocLite()
#biocLite("EBImage")

# load packages & personal library functions (hide function list from environment)
library(EBImage)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/image_HISTOGRAM.R", envir = myEnv)
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Image Processing")

# load image files
img <- readImage("beach.jpg")
#img <- readImage("https://www.r-project.org/logo/Rlogo.png")

# explore image files
#print(img)
#print(img, short = T)
#print(class(img))
#print(str(img))

# display image
#print(display(img, method = "raster"))

# plot image historgram
#print(hist.plot(img))

# convert to grayscale
#print(display(img, method = "raster"))
colorMode(img) <- Grayscale
#print(hist.plot(img))
#print(display(img, method = "raster", all = T))
#print(display(img, method = "raster", frame = 1))
#print(display(img, method = "raster", frame = 2))
#print(display(img, method = "raster", frame = 3))

# revert back to original color
colorMode(img) <- Color
#print(display(img, method = "raster"))

# equalize image histogram
img2 <- equalize(img)
#print(hist.plot(img2))
#print(display(combine(img, img2), method = "raster", all = T))

# resize, rotate, transplate image
w0 <- nrow(img)    # original width (in pixel)
h0 <- ncol(img)    # original height (in pixel)
img3 <- resize(img, w = w0/10, h = h0/5)
img3 <- resize(img, w = w0/10)    # only w or h preserves aspect ratio
img4 <- rotate(img, angle = 45, bg.col = "white")
img5 <- translate(img, c(100, -100), bg.col = "white")
#print(display(img, method = "raster"))
#print(display(img3, method = "raster"))
#print(display(img4, method = "raster"))
#print(display(img5, method = "raster"))

#===============================================
# denoising with gaussian and median filtering
#===============================================
# first corrupt image by adding uniform noise
img2 <- img
l <- length(img)
n <- l/5
img2[sample(l, n)] <- runif(n, 0, 1)    # corrupt 20% of image

# gaussian & median filtering
#img3 <- gblur(img2, sigma = 5)
#img4 <- medianFilter(img2, size = 1)
#print(display(combine(img, img2, img3, img4), method = "raster", all = T))

#===============================================
# edge detection using Sobel filter
#===============================================
# first construct horizontal and vertical Sobel kernels
Shoriz <- matrix(c(1, 2, 1, 0, 0, 0, -1, -2, -1), nrow = 3)
Svert <- t(Shoriz)

# next get edges via image convolution (apply filter)
imgH <- filter2(img, Shoriz)    # horizontal edges
imgV <- filter2(img, Svert)     # vertical edges

# next combine edge data to get overall edges
hdata <- imageData(imgH)
vdata <- imageData(imgV)
edata <- sqrt(hdata^2 + vdata^2)

# next transform edge data to image
imgE <- Image(edata, colormode = 2)
#print(display(combine(img, imgH, imgV, imgE), method = "raster", all = T))

# clean up edges by thresholding above 0.5
#print(hist.plot(imgE))
e2data <- array(sapply(edata, function(x) ifelse(x > 0.5, x, 0)), dim(edata))
imgE2 <- Image(e2data, colormode = 2)
#print(hist.plot(imgE2))
#print(display(combine(imgE, imgE2), method = "raster", all = T))

#===============================================
# Harris corner detection (not available ?)
#===============================================

#===========================================================
# erosion/dilation, opening(eros->dila)/closing(dila->eros)
#===========================================================
colorMode(img) <- Grayscale
img1 <- getFrame(img, 1)
kern <- makeBrush(size = 7, shape = "diamond")
imgErode <- erode(img1, kern)
imgDilate <- dilate(img1, kern)
#print(display(combine(img1, imgErode, imgDilate), method = "raster", all = T))

colorMode(img) <- Color
imgO <- opening(img, kern)
imgC <- closing(img, kern)
print(display(combine(img, imgO, imgC), method = "raster", all = T))

# detach all user-loaded packages and personal environment(s)
detachAll(unload = T)
