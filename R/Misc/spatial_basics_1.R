# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(sp)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Misc")

#======================================================================
# learning vector data
#======================================================================
# create a SpatialPoints object
longitude <- c(-116.7, -120.4, -116.7, -113.5, -115.5, -120.8, -119.5, -113.7, -113.7, -110.7)
latitude <- c(45.3, 42.6, 38.9, 42.1, 35.7, 38.9, 36.2, 39, 41.6, 36.9)
lonlat <- cbind(longitude, latitude)
pts <- SpatialPoints(lonlat)

# add CRS (coordinate reference system)
crdref <- CRS("+proj=longlat +datum=WGS84")
pts <- SpatialPoints(lonlat, proj4string = crdref)

# create SpatialPointsDataFrame
df <- data.frame(ID = 1:nrow(lonlat), precip = (latitude - 30)^3)
ptsdf <- SpatialPointsDataFrame(pts, data = df)
#======================================================================
# create SpatialLines and SpatialPolygons object
# (using spLines() and spPolygons() from raster package)
library(raster)
lon <- c(-116.8, -114.2, -112.9, -111.9, -114.2, -115.4, -117.7)
lat <- c(41.3, 42.9, 42.4, 39.8, 37.6, 38.3, 37.6)
lonlat <- cbind(lon, lat)
lns <- spLines(lonlat, crs = crdref)
pols <- spPolygons(lonlat, crs = crdref)
#======================================================================
# print data
pts
ptsdf
lns
pols

#======================================================================
# learning raster data
#======================================================================
# create a skeletal RasterLayer (single-layer)
library(raster)
r <- raster(ncol = 10, nrow = 10, xmx = -80, xmn = -150, ymn = 20, ymx = 60)

# assign values to r (assign cell index)
values(r) <- 1:ncell(r)

# plot r
plot(r)
plot(pols, border = 'blue', lwd = 2, add = TRUE)
points(lonlat, col = 'red', pch = 20, cex = 3)
#======================================================================
# create a RasterStack from multiple single layers
r2 <- r * r
r3  <- sqrt(r)
s <- stack(r, r2, r3)

plot(s)
#======================================================================
# create a RasterBrick from RasterStack
b <- brick(s)


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
