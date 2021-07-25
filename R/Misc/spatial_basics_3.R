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
# learning about CRS
#======================================================================
# get CRS
library(raster)
f <- system.file("external/lux.shp", package = "raster")
p <- shapefile(f)
crs(p)

# assign CRS (not a good approach)
pp <- p
crs(pp) <- NA
crs(pp) <- CRS("+proj=longlat +datum=WGS84")

#======================================================================
# transforming vector data (to data with another CRS)
#======================================================================
# convert to data with Robinson projection
newcrs <- CRS("+proj=robin +datum=WGS84")
rob <- spTransform(p, newcrs)
rob

# backtransform to longitude/latitude
p2 <- spTransform(rob, CRS("+proj=longlat +datum=WGS84"))
p2

#======================================================================
# transforming raster data
#======================================================================
r <- raster(xmn = -110, xmx = -90, ymn = 40, ymx = 60, ncols = 40, nrows = 40)
r <- setValues(r, 1:ncell(r))
r
plot(r)

newproj <- "+proj=lcc +lat_1=48 +lat_2=33 +lon_0=-100 +ellps=WGS84"
pr1 <- projectRaster(r, crs = newproj)
pr2 <- projectRaster(r, crs = newproj, res = 20000)   # set resolution
crs(pr1)
pr1
pr2




# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
