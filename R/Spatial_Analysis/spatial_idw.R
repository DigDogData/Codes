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

# get shapefile for Baltimore 2010 Census Tract
suppressMessages(library(rgdal))
baltimore_shp <- readOGR(dsn = "../../Codes/Data/Baltimore/Shapefiles",
                         layer = "Census_Tracts_2010")

#####################################
# load and prep crime data
#####################################
# load 2017 crime data for Baltimore
crime_df <- read.csv("../../Codes/Data/Baltimore/Crimes2017.csv",
                     na.strings=c(""," ","?","NA","na"))

# keep only needed columns
crime_df <- crime_df[, c("Description", "Inside.Outside", "Longitude", "Latitude")]

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
                                     levels = c("ROBBERY", "AGG. ASSAULT", "SHOOTING", "RAPE", "HOMICIDE"),
                                     labels = c("Robbery", "Assault", "Shooting", "Rape", "Homicide"))

# remove NA and duplicated rows
violent_crimes <- violent_crimes[complete.cases(violent_crimes), ]
violent_crimes <- violent_crimes %>% filter(!duplicated(violent_crimes, ))
names(violent_crimes) <- c("crime", "in_out", "long", "lat")

# rearrange columns
violent_crimes <- violent_crimes[, c("long", "lat", "in_out", "crime")]

# collapse in_out categories
violent_crimes$in_out <- ifelse(violent_crimes$in_out == "I" | violent_crimes$in_out == "I",
                                "Inside",
                                "Outside")
violent_crimes$in_out <- factor(violent_crimes$in_out)

#################################################
# compute idw interpolation for each crime type
#################################################
# function to transform all categorical variables to indicator variables
indicator.transform <- function(x){
  dat <- violent_crimes[, x]
  lvls = levels(dat)
  trans <- matrix(nrow = length(dat), ncol = length(lvls))
  for(i in 1:length(lvls)){
    for(j in 1:length(dat))
      ifelse(dat[j] == lvls[i], trans[j, i] <- 1, trans[j, i] <- 0)
  }
  trans <- as.data.frame(trans)
  names(trans) <- lvls
  cbind(violent_crimes, trans)
}

# add indicator columns for each factor column
violent_crimes <- indicator.transform("in_out")
violent_crimes <- indicator.transform("crime")

#remove unneeded columns
dropCols <- c("in_out", "crime")
violent_crimes <- violent_crimes[, !(names(violent_crimes) %in% dropCols)]

#################################################
# compute idw interpolation for each crime type
#################################################
# next, convert to SpatialPointsDataFrame
suppressMessages(library(sp))
crime_spdf <- violent_crimes
coordinates(crime_spdf) <- ~ long + lat
proj4string(crime_spdf) <- CRS("+proj=longlat +ellps=WGS84")







# next run IDW interpolation
suppressMessages(library(gstat))
suppressMessages(library(xts))
# define sample grid based on the extent of crime_spdf
grid <-spsample(crime_spdf, type = "regular", n = 10000)
# run idw
robbery.idw <- idw(Robbery ~ 1, crime_spdf, newdata = grid)
assault.idw <- idw(Assault ~ 1, crime_spdf, newdata = grid)
shooting.idw <- idw(Shooting ~ 1, crime_spdf, newdata = grid)
rape.idw <- idw(Rape ~ 1, crime_spdf, newdata = grid)
homicide.idw <- idw(Homicide ~ 1, crime_spdf, newdata = grid)

########################################################
# convert idw->raster->polygons->dataframe for plotting
########################################################
# first, convert idw to raster
suppressMessages(library(raster))
gridded(robbery.idw) <- T         # coerce to SpatialPixelsDF
gridded(assault.idw) <- T
gridded(shooting.idw) <- T
gridded(rape.idw) <- T
gridded(homicide.idw) <- T
robbery.raster <- raster(robbery.idw)
assault.raster <- raster(assault.idw)
shooting.raster <- raster(shooting.idw)
rape.raster <- raster(rape.idw)
homicide.raster <- raster(homicide.idw)

# next convert raster to polygons
robbery.rtp <- rasterToPolygons(robbery.raster)
assault.rtp <- rasterToPolygons(assault.raster)
shooting.rtp <- rasterToPolygons(shooting.raster)
rape.rtp <- rasterToPolygons(rape.raster)
homicide.rtp <- rasterToPolygons(homicide.raster)

# add id column to polygon data for join later
robbery.rtp@data$id <- 1:nrow(robbery.rtp@data)
assault.rtp@data$id <- 1:nrow(assault.rtp@data)
shooting.rtp@data$id <- 1:nrow(shooting.rtp@data)
rape.rtp@data$id <- 1:nrow(rape.rtp@data)
homicide.rtp@data$id <- 1:nrow(homicide.rtp@data)

# next convert polygons to dataframe
robbery_df <- fortify(robbery.rtp)
assault_df <- fortify(assault.rtp)
shooting_df <- fortify(shooting.rtp)
rape_df <- fortify(rape.rtp)
homicide_df <- fortify(homicide.rtp)

# add prediction data to dataframe by merging via id column
robbery_df <- merge(robbery_df, robbery.rtp@data, by.x = "id", by.y = "id")
assault_df <- merge(assault_df, assault.rtp@data, by.x = "id", by.y = "id")
shooting_df <- merge(shooting_df, shooting.rtp@data, by.x = "id", by.y = "id")
rape_df <- merge(rape_df, rape.rtp@data, by.x = "id", by.y = "id")
homicide_df <- merge(homicide_df, homicide.rtp@data, by.x = "id", by.y = "id")

# get Baltimore map
suppressMessages(library(ggmap))
baltimore_map <- get_map(location = geocode("Baltimore"),
                         zoom = 12,
                         scale = 1,
                         maptype = "satellite",
                         source = "google")
baltimore_map2 <- get_map(location = geocode("Baltimore"),
                          zoom = 12,
                          scale = 1,
                          maptype = "satellite",
                          source = "google")

# get zoom-level bounding box
xlim <- bb2bbox(attr(baltimore_map, "bb"))[c(1, 3)]
ylim <- bb2bbox(attr(baltimore_map, "bb"))[c(2, 4)]

# create thiessen polygon map
map2 <- ggmap(baltimore_map2, extent = "normal", maprange = F) +
  geom_polygon(aes(x = long, y = lat, group = group, fill = var1.pred),
               alpha = 0.7,
               data = robbery_df) +
  scale_fill_continuous(low = "yellow", high = "red") +
  geom_point(aes(x = long, y = lat),
             size = 1.5,
             #             alpha = 0.5,
             data = subset(violent_crimes, crime == "Robbery")) +
  coord_cartesian(xlim = xlim, ylim = ylim, expand = 0) +
  ggtitle("Crime Neighborhood") +
  theme(aspect.ratio = 1,
        plot.title = element_text(hjust = 0.5),
        panel.background = element_rect(fill = "white"),
        axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        legend.background = element_rect(fill = alpha("white", 0.6)),
        legend.key = element_rect(colour = NA, fill = NA),
        legend.title = element_text(size = 11, face = "bold"),
        legend.text = element_text(size = 10),
        legend.position = c(0.11, 0.17))

map3 <- ggmap(baltimore_map2, extent = "normal", maprange = F) +
  geom_raster(aes(fill = robbery.raster@data$var1.pred),
               alpha = 0.7,
               data = robbery.raster) +
  scale_fill_continuous(low = "yellow", high = "red") +
  geom_point(aes(x = long, y = lat),
             size = 2,
             #             alpha = 0.5,
             data = subset(violent_crimes, crime == "Robbery")) +
  coord_cartesian(xlim = xlim, ylim = ylim, expand = 0) +
  ggtitle("Crime Neighborhood") +
  theme(aspect.ratio = 1,
        plot.title = element_text(hjust = 0.5),
        panel.background = element_rect(fill = "white"),
        axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        legend.background = element_rect(fill = alpha("white", 0.6)),
        legend.key = element_rect(colour = NA, fill = NA),
        legend.title = element_text(size = 11, face = "bold"),
        legend.text = element_text(size = 10),
        legend.position = c(0.11, 0.17))

# create terrain map
map1 <- ggmap(baltimore_map) +
  geom_point(aes(x = Longitude, y = Latitude, color = Crime),
             size = 2,
#             alpha = 0.5,
             data = violent_crimes) +
  ggtitle("Crime Data") +
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
        legend.position = c(0.11, 0.165))

# plot maps
library(grid)
pushViewport(viewport(layout = grid.layout(1,2)))
print(map1, vp=viewport(layout.pos.col = 1, layout.pos.row = 1))
print(map2, vp=viewport(layout.pos.col = 2, layout.pos.row = 1))

# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
