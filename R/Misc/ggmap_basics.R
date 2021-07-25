# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(ggmap)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Misc")

# get data
sales <- read.csv("../Data/HomeSaleData.csv", check.names = F, strip.white = T,
                  na.strings=c(""," ","?","NA","na","<NA>"), stringsAsFactors = F)
ward <- read.csv("../Data/WardSaleData.csv", check.names = F, strip.white = T,
                  na.strings=c(""," ","?","NA","na","<NA>"), stringsAsFactors = F)
preds <- read.csv("../Data/HomeSalePreds.csv", check.names = F, strip.white = T,
                  na.strings=c(""," ","?","NA","na","<NA>"), stringsAsFactors = F)

# get map for Corvallis
corvallis <- geocode('Corvallis')
corvallis_map <- get_map(location = corvallis,
                         zoom = 13,
                         scale = 1,
                         maptype = "terrain",
                         source = "google")

# get satellite map
corvallis_map_sat <- get_map(location = corvallis,
                             zoom = 13,
                             scale = 1,
                             maptype = "satellite",
                             source = "google")

# get toner map from Stamen Maps
corvallis_map_bw <- get_map(location = corvallis,
                            zoom = 13,
                            scale = 1,
                            maptype = "toner",
                            source = "stamen")
print(ggmap(corvallis_map))
print(ggmap(corvallis_map_sat))
print(ggmap(corvallis_map_bw))

# plot sales data
#print(ggmap(corvallis_map,
#            base_layer = ggplot(data = sales, aes(lon, lat))) +
#        geom_point() +
#        facet_wrap(~ condition))

# plot point layer with color mapped to ward
ward$ward <- as.character(ward$ward)
#print(ggplot(ward, aes(lon, lat)) +
#        geom_point(aes(color = ward)))

# plot point layer with color mapped to group (polygon identifier)
ward$group <- as.character(ward$group)
#print(ggplot(ward, aes(lon, lat)) +
#        geom_point(aes(color = group)))

# plot path layer with group mapped to group
#print(ggplot(ward, aes(lon, lat)) +
#        geom_path(aes(group = group)))

# plot polygon layer with fill mapped to ward, and group to group
#print(ggplot(ward, aes(lon, lat)) +
#        geom_polygon(aes(group = group, fill = ward)))

# add polygon layer to original city map (use datarange instead of maprange)
print(ggmap(corvallis_map_bw,
            base_layer = ggplot(data = ward, aes(lon, lat)),
            extent = "normal",
            maprange = F) +
        geom_polygon(aes(group = group, fill = ward)))

# repeat, but fill by num_sales
print(ggmap(corvallis_map_bw,
            base_layer = ggplot(data = ward, aes(lon, lat)),
            extent = "normal",
            maprange = F) +
        geom_polygon(aes(group = group, fill = num_sales)))

# repeat, but fill by avg_price
print(ggmap(corvallis_map_bw,
            base_layer = ggplot(data = ward, aes(lon, lat)),
            extent = "normal",
            maprange = F) +
        geom_polygon(aes(group = group, fill = avg_price),
                     alpha = 0.8))

# plot predicted home price on map
print(ggmap(corvallis_map_bw) +
        geom_tile(aes(lon, lat, fill = predicted_price),
                  data = preds,
                  alpha = 0.8))


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
