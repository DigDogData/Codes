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

# load 2017 crime data for Baltimore
crime_df <- read.csv("../../Codes/Data/Baltimore/Crimes2017.csv")

# keep only needed columns
crime_df <- crime_df[, c("Description", "Longitude", "Latitude")]

# remove NA and duplicated rows
suppressMessages(library(dplyr))
crime_df <- crime_df[complete.cases(crime_df), ]
crime_df <- crime_df %>% filter(!duplicated(crime_df, ))

# collapse robbery subcategories to a single "robbery" category
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
names(violent_crimes) <- c("Crime", "Longitude", "Latitude")

# remove duplicated columns
violent_crimes <- violent_crimes %>% filter(!duplicated(violent_crimes, ))

# convert to SpatialPointsDataFrame
suppressMessages(library(sp))
coords <- SpatialPoints(violent_crimes[, c("Longitude", "Latitude")])
crime_spdf <- SpatialPointsDataFrame(coords, violent_crimes)
proj4string(crime_spdf) <- CRS("+proj=longlat +ellps=WGS84")

##########################################
# create Thiessen (or Voronoi) polygons
##########################################
# create a tessellated surface
suppressMessages(library(spatstat))
suppressMessages(library(maptools))
crime_ppp <- as.ppp(crime_spdf)           # convert SPDF to PPP (point pattern) object
dat.pp <- dirichlet(crime_ppp)            # dirichlet tessellation of PP object

# convert to Spatial Polygon
dat.pp <- as(dat.pp,"SpatialPolygons")
proj4string(dat.pp) <- CRS("+proj=longlat +ellps=WGS84")

# assign crime data to each polygon
suppressMessages(library(sp))
val.Z <- over(dat.pp, crime_spdf)

# create SpatialPolygonsDataFrame
thiessen <- SpatialPolygonsDataFrame(dat.pp, val.Z)

# crop to Baltimore outer area shapefile
suppressMessages(library(raster))
thiessen.crop <-crop(thiessen, baltimore_shp)

# get Baltimore map
suppressMessages(library(ggmap))
baltimore_map <- get_map(location = geocode("Baltimore"),
                         zoom = 16,
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

# convert thiessen SPDF to dataframe and assign crime to each polygon
thiessen_df <- fortify(thiessen.crop)
val.Z[, c("Longitude", "Latitude")] <- NULL
val.Z$id <- row.names(val.Z)
thiessen_df <- thiessen_df %>% left_join(val.Z, by='id')

# create thiessen polygon map
map2 <- ggmap(baltimore_map, extent = "normal", maprange = F) +
  geom_polygon(data = thiessen_df,
               aes(x=long, y=lat, group = group, fill = Crime),
               color = "gray80",
               alpha = 0.3) +
  geom_point(aes(x = Longitude, y = Latitude, color = Crime),
             size = 2,
             #             alpha = 0.5,
             data = violent_crimes) +
  coord_cartesian(xlim = xlim, ylim = ylim, expand = 0) +
  ggtitle("Crime Neighborhood") +
  scale_fill_manual(breaks = c("Robbery", "Assault", "Shooting", "Rape", "Homicide"),
                     values = c("yellow3", "lightsalmon", "darkorange", "orangered", "red")) +
  scale_color_manual(breaks = c("Robbery", "Assault", "Shooting", "Rape", "Homicide"),
                     values = c("yellow3", "lightsalmon", "darkorange", "orangered", "red")) +
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
