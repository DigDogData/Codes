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
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Spatial Analysis")

# load files for 2011 Camden census and house sales data
census <- read.csv("../Data/Camden/practicaldata.csv")
price <- read.csv("../Data/Camden/camdenhousesales15.csv")
price <- price[, c(1, 2, 8, 9)]   # keep only relevant columns

# conver price dataframe to SpatialPointsDataFrame
library(sp)
price.points <- SpatialPointsDataFrame(price[, 3:4],
                                       price,
                                       proj4string = CRS("+init=EPSG:27700"))

# load GIS shapefiles for Camden outer layer and house points
suppressMessages(library(rgdal))
suppressMessages(library(rgeos))
output.areas <- readOGR(dsn = "../Data/Camden/Camden_oa11", layer = "Camden_oa11")
house.points <- readOGR(dsn = "../Data/Camden/Camden_house_sales", layer = "Camden_house_sales")

# join census data to shapefile (using "OA" cloumn for outer area code)
oa.census <- merge(output.areas, census, by.x = "OA11CD", by.y = "OA")

# set CRS to British National Grid
proj4string(oa.census) <- CRS("+init=EPSG:27700")
proj4string(house.points) <- CRS("+init=EPSG:27700")

# generate choropleth map of qualification variable + house price points
library(tmap)
map1 <- tm_shape(shp = oa.census) +
  tm_fill(col = "Qualification",
          style = "quantile",
          palette = "Reds",
          title = "% Qualification",
          legend.hist = F) +
  tm_borders(alpha = 0.4) +
  tm_shape(shp = price.points) +
  tm_bubbles(size = "Price",
             col = "Price",
             palette = "Blues",
             style = "quantile",
             legend.size.show = F,
             title.col = "Price (Pound)",
             border.lwd = 0.1,
             border.alpha = 0.1) +
  tm_compass(position=c("right", "top"),
             type = "4star",
             show.labels = 2,
             fontsize = 0.7) +
  tm_layout(title = "Camden",
            title.size = 1.2,
            legend.position = c("left", "bottom"),
            legend.title.size = 1,
            legend.text.size = 0.6,
            legend.bg.color = "white",
            legend.bg.alpha = 0.5,
            frame = F)

# get google map for Camden
library(dismo)
camden.map <- gmap(x = "Camden, London",
                   zoom = 13,
                   scale = 1,
                   type = "terrain")
camden.map2 <- gmap(x = "Camden, London",
                   zoom = 13,
                   scale = 1,
                   type = "satellite")

# reproject house.points to the WGS84 projection
CRS.new <- CRS("+proj=longlat +ellps=WGS84 +datum=WGS84")
reprojected.houses <- spTransform(house.points, CRS.new)

# plot base map + house price points
map2 <- tm_shape(shp = camden.map) +
  tm_raster() +
  tm_shape(shp = reprojected.houses) +
  tm_bubbles(size = "Price",
             col = "Price",
             palette = "Reds",
             style = "quantile",
             legend.size.show = F,
             title.col = "Price (Pound)",
             border.lwd = 0.1,
             border.alpha = 0.1) +
  tm_compass(position=c("right", "top"),
             type = "4star",
             show.labels = 2,
             fontsize = 0.7) +
  tm_layout(title = "Camden",
            title.size = 1.2,
            title.bg.color = "white",
            title.bg.alpha = 0.7,
            legend.position = c("left", "bottom"),
            legend.title.size = 1,
            legend.text.size = 0.6,
            legend.bg.color = "white",
            legend.bg.alpha = 0.7,
            frame = F)

map3 <- tm_shape(shp = camden.map2) +
  tm_raster() +
  tm_shape(shp = reprojected.houses) +
  tm_bubbles(size = "Price",
             col = "Price",
             palette = "Reds",
             style = "quantile",
             legend.size.show = F,
             title.col = "Price (Pound)",
             border.lwd = 0.1,
             border.alpha = 0.1) +
  tm_compass(position=c("right", "top"),
             type = "4star",
             show.labels = 2,
             fontsize = 0.7) +
  tm_layout(title = "Camden",
            title.size = 1.2,
            title.bg.color = "white",
            title.bg.alpha = 0.5,
            legend.position = c("left", "bottom"),
            legend.title.size = 1,
            legend.text.size = 0.6,
            legend.bg.color = "white",
            legend.bg.alpha = 0.5,
            frame = F)

library(grid)
library(gridExtra)
pushViewport(viewport(layout = grid.layout(2,2)))
print(map1, vp=viewport(layout.pos.col = 1, layout.pos.row =1))
print(map2, vp=viewport(layout.pos.col = 2, layout.pos.row =1))
print(map3, vp=viewport(layout.pos.col = 1, layout.pos.row =2))

# generate interactive (zoomable) map
library(leaflet)
map4 <- tm_shape(shp = price.points) +
  tm_bubbles(size = "Price",
             col = "Price",
             palette = "Blues",
             style = "quantile",
             legend.size.show = F,
             title.col = "Price (Pound)",
             border.lwd = 0.1,
             border.alpha = 0.1) +
  tm_compass(position=c("right", "top"),
             type = "4star",
             show.labels = 2,
             fontsize = 0.7) +
  tm_layout(title = "Camden",
            title.size = 1.2,
            legend.position = c("left", "bottom"),
            legend.title.size = 1,
            legend.text.size = 0.6,
            legend.bg.color = "white",
            legend.bg.alpha = 0.5,
            frame = F)
#tmap_mode("view")
#print(map4)



# save shapefile
#writeOGR(oa.census,
#         dsn = "../Data/Camden/Camden_oa11/Camden_oa11_new",
#         layer =  "Census_OA_Shapefile",
#         driver="ESRI Shapefile")


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
