# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(magick)
library(EBImage)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/image_HISTOGRAM.R", envir = myEnv)
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Image Processing")

# load image files
img <- image_read("beach.jpg")

# explore image
print(image_info(img))
#print(image)                    # display opens on RStudio Viewer
#print(plot(as.raster(image)))   # display opens on RStudip Plots window
#image_browse(image)             # display opens on external viewer

# plot color histogram
print(hist.plot(img))

# many of the standard image manipulations can be done by converting
# image to EBImage format and then using EBImage methods on it
#imageEB <- as_EBImage(image)

# edge detection using Sobel filter
Shoriz <- matrix(c(1, 2, 1, 0, 0, 0, -1, -2, -1), nrow = 3)
Svert <- t(Shoriz)
imgH <- image_convolve(img, Shoriz)
imgV <- image_convolve(img, Svert)
#print(plot(as.raster(img)))
#print(plot(as.raster(imgH)))
#print(plot(as.raster(imgV)))



# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)
