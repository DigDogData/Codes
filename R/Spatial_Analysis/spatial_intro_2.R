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

######################################
# get and prep crime data
######################################
# load 2017 crime data for Baltimore
crime_df <- read.csv("../Data/Baltimore/Crimes2017.csv")

# keep only needed columns
crime_df <- crime_df[, c("CrimeDate", "Description", "Longitude", "Latitude", "Total.Incidents")]

# remove NA rows
crime_df <- crime_df[complete.cases(crime_df), ]

# collapse robbery subcategories to a single "robbery" category
suppressMessages(library(dplyr))
crime_df$Description <- as.character(crime_df$Description)
crime_df <- crime_df %>% mutate(Description = ifelse(Description %in%
                                                       c("ROBBERY - CARJACKING",
                                                         "ROBBERY - COMMERCIAL",
                                                         "ROBBERY - RESIDENCE",
                                                         "ROBBERY - STREET"),
                                                     "ROBBERY", Description))

# consider only violent crimes
violent_crimes <- subset(crime_df,
                         Description == "AGG. ASSAULT" | Description == "HOMICIDE" |
                           Description == "RAPE" | Description == "ROBBERY" |
                           Description == "SHOOTING")

# transform back to factor and reorder+rename levels
crime_df$Description <- factor(crime_df$Description)
violent_crimes$Description <- factor(violent_crimes$Description,
                                     levels = c("ROBBERY", "AGG. ASSAULT", "SHOOTING", "RAPE", "HOMICIDE"))
levels(violent_crimes$Description) <- c("Robbery", "Assault", "Shooting", "Rape", "Homicide")
names(violent_crimes) <- c("Date", "Crime", "Longitude", "Latitude", "Count")

# convert to SpatialPointsDataFrame
library(sp)
coords <- SpatialPoints(crime_df[, c("Longitude", "Latitude")])
crime_sp <- SpatialPointsDataFrame(coords, crime_df)
proj4string(crime_sp) <- CRS("+proj=longlat +ellps=WGS84")

# create and save shapefile of crime data
suppressMessages(library(rgdal))
writeOGR(obj = crime_sp,
         dsn = "../Data/Baltimore/Shapefiles",
         layer = "Crime_Shapefile",
         driver = "ESRI Shapefile",
         overwrite_layer = T)

# get shapefile for Baltimore 2010 Census Tract
baltimore_shp <- readOGR(dsn = "../Data/Baltimore/Shapefiles",
                      layer = "Census_Tracts_2010")

# get shapefile for Maryland 2017 census tract data
maryland_shp <- readOGR(dsn = "../Data/Baltimore/Shapefiles",
                        layer = "Maryland_2010")

#plot(maryland_shp, col = "grey", axes = T)
#plot(crime_sp, pch = 21, bg = "red", cex = .5, add = T)

#plot(baltimore_shp, col = "grey", axes = T)
#plot(crime_sp, pch = 21, bg = "red", cex = .5, add = T)

# plot data
suppressMessages(library(ggplot2))
suppressMessages(library(ggmap))

# get Baltimore map
geo_reply <- geocode("Baltimore", output = "all", messaging = T, override_limit = T)
if(geo_reply$status == "OK"){
  lon <- geo_reply$results[[1]]$geometry$location$lng
  lat <- geo_reply$results[[1]]$geometry$location$lat
  baltimore_map <- get_map(location = c(lon, lat),
                           zoom = 12,
                           scale = 1,
                           maptype = "terrain",
                           source = "google")
  baltimore_map2 <- get_map(location = c(lon, lat),
                            zoom = 12,
                            scale = 1,
                            maptype = "satellite",
                            source = "google")
  
  map1 <- ggmap(baltimore_map) +
    geom_point(aes(x = Longitude, y = Latitude, color = Crime),
               size = 1.5,
#               alpha = 0.5,
               data = violent_crimes) +
    ggtitle("Terrain Map") +
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
          legend.position = c(0.11, 0.17))

  map2 <- ggmap(baltimore_map2) +
    geom_point(aes(x = Longitude, y = Latitude, color = Crime),
               size = 1.5,
#               alpha = 0.5,
               data = violent_crimes) +
    ggtitle("Satellite Map") +
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
          legend.position = c(0.11, 0.17))
  
  map3 <- ggmap(baltimore_map) +
    stat_density2d(aes(x = Longitude, y = Latitude, fill = ..level.., alpha = ..level..),
                   size = 2,
                   bins = 10,
                   data = violent_crimes,
                   geom = "polygon") +
    labs(fill = "Contour") +
    scale_fill_gradient(low = "#8b5a00", high = "#ff0000") +
    guides(alpha = F) +
    ggtitle("Distribution Plot") +
    theme(plot.title = element_text(hjust = 0.5),
          panel.background = element_rect(fill = "white"),
          axis.title = element_blank(),
          axis.text = element_blank(),
          axis.ticks = element_blank(),
          legend.background = element_rect(fill = alpha("white", 0.6)),
          legend.key = element_rect(colour = NA, fill = NA),
          legend.title = element_text(size = 11, face = "bold"),
          legend.text = element_text(size = 10),
          legend.position = c(0.11, 0.17))
  
  # convert baltimore census tract shapefile to dataframe
  baltimore_df <- fortify(baltimore_shp)
  map4 <- ggplot() +
    geom_polygon(data = baltimore_df,
                 aes(x=long, y=lat, group = group),
                 color = "black",
                 fill = "darkolivegreen4") +
    coord_equal(expand = F) +
    geom_point(aes(x = Longitude, y = Latitude, color = Crime),
               size = 1.5,
#               alpha = 0.5,
               data = violent_crimes) +
    ggtitle("Shapefile Plot") +
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
          legend.position = c(0.11, 0.17))
}

if(geo_reply$status == "OK"){
  pushViewport(viewport(layout = grid.layout(2,2)))
  print(map1, vp=viewport(layout.pos.col = 1, layout.pos.row = 1))
  print(map2, vp=viewport(layout.pos.col = 2, layout.pos.row = 1))
  print(map3, vp=viewport(layout.pos.col = 1, layout.pos.row = 2))
  print(map4, vp=viewport(layout.pos.col = 2, layout.pos.row = 2))
} else{
  cat(paste("geocode failed with", geo_reply$status, "\n"))
}

# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
