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
setwd("C:/Users/Roy/Documents/Data Analysis/Portfolios/Spatial Analysis")

# load GIS shapefiles for Cambridge outer layer
suppressMessages(library(rgdal))
suppressMessages(library(rgeos))
output.areas <- readOGR(dsn = "../../Codes/Data/Cambridge/Shapefiles",
                        layer = "Cambridge_oa11")
#house.points <- readOGR(dsn = "../../Codes/Data/Cambridge/House_Sales",
#                        layer = "House_Points")

# load 2011 house median price data for Cambridge
price <- read.csv("../../Codes/Data/Cambridge/HouseSales2011.csv")

# convert price dataframe to SpatialPointsDataFrame
suppressMessages(library(sp))
coords <- SpatialPoints(price[, c("Longitude", "Latitude")])
crime_spdf <- SpatialPointsDataFrame(coords, violent_crimes)
proj4string(crime_spdf) <- CRS("+proj=longlat +ellps=WGS84")


# run IDW interpolation
suppressMessages(library(gstat))
suppressMessages(library(xts))
# first define sample grid based on the extent of the house.points file
grid <-spsample(house.points, type = "regular", n = 10000)
# next run idw for the 2011 median price variable of house.points
house.idw <- idw(md_2011 ~ 1, house.points, newdata = grid)
idw_df <- as.data.frame(house.idw)
names(idw_df)[1:3] <- c("long", "lat", "prediction")

# convert idw data to raster for plotting
library(raster)
coordinates(idw_df) <- ~ long + lat   # create SpatialPointsDF
gridded(idw_df) <- T                  # coerce to SpatialPixelsDF
raster_idw <- raster(idw_df)          # coerce to raster
projection(raster_idw) <- CRS("+proj=longlat +ellps=WGS84")
#plot(raster_idw)

suppressMessages(library(ggmap))
cambridge_map <- get_map(location = geocode("Cambridge, UK"),
                         zoom = 12,
                         scale = 1,
                         maptype = "terrain",
                         source = "google")

map <- ggmap(cambridge_map) +
  geom_point(aes(x = Longitude, y = Latitude, size = md_2011),
             color = "blue",
#             size = 1.5,
#               alpha = 0.5,
             data = violent_crimes) +
  ggtitle("Terrain Map (2)") +
  scale_color_manual(breaks = c("Robbery", "Assault", "Shooting", "Rape", "Homicide"),
                     values = c("yellow3", "lightsalmon", "darkorange", "orangered", "red")) +
  theme(plot.title = element_text(hjust = 0.5),
        panel.background = element_rect(fill = "white"),
        axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        legend.background = element_rect(fill = alpha("white", 0.6)),
        legend.key = element_rect(colour = NA, fill = NA),
        legend.title = element_text(size = 11, face = "bold"),
        legend.text = element_text(size = 10),
        legend.position = c(0.13, 0.19))


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
