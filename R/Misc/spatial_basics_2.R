# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Misc")

#======================================================================
# reading and writing vector data
#======================================================================
# read vector data using shapefile (from filename that came with raster package)
library(raster)
filename <- system.file("external/lux.shp", package = "raster")
filename
s <- shapefile(filename)
s

# write shapefile
outfile <- "test.shp"
shapefile(s, outfile, overwrite = T)

#======================================================================
# reading and writing raster data
#======================================================================
# read raster data
filename <- system.file("external/rlogo.grd", package = "raster")
r1 <- raster(filename)            # read 1st "band" (layer) out of 3 bands
r2 <- raster(filename, band = 2)  # read 2nd band
r1
r2

# read all layers in a single brick (object)
b <- brick(filename)
b

# or use stack (less efficient)
s <- stack(filename)
s

# write raster data
x <- writeRaster(s, "output.tif", overwrite = T)



# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
