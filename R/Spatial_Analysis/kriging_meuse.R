# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# transform meuse data to SpatialPointsDataFrame
suppressMessages(library(sp))
data(meuse)
coordinates(meuse) <- ~ x + y
proj4string(meuse) <- CRS("+proj=stere
                          +lat_0=52.15616055555555 +lon_0=5.38763888888889
                          +k=0.999908 +x_0=155000 +y_0=463000
                          +ellps=bessel +units=m +no_defs
                          +towgs84=565.2369,50.0087,465.658,
                          -0.406857330322398,0.350732676542563,-1.8703473836068, 4.0812")

# define a regular grid for kriging
xrange <- range(as.integer(meuse@coords[, 1])) + c(0,1)
yrange <- range(as.integer(meuse@coords[, 2]))
grid <- expand.grid(x = seq(xrange[1], xrange[2], by = 40),
                    y = seq(yrange[1], yrange[2], by = 40))
coordinates(grid) <- ~ x + y
gridded(grid) <- T

# do kriging
suppressMessages(library(automap))
krg <- autoKrige(formula = copper ~ 1,
                 input_data = meuse,
                 new_data = grid)

# extract kriged data
krg_df <- data.frame(krg$krige_output@coords,
                     pred = krg$krige_output@data$var1.pred)

# transform to SpatialPointsDF & assign original (meuse) projection
krg_spdf <- krg_df
coordinates(krg_spdf) <- ~ x + y 
proj4string(krg_spdf) <- proj4string(meuse)

# transform again to longlat coordinates (for overlaying on google map below)
krg_spdf <- spTransform(krg_spdf, CRS("+init=epsg:4326"))
krg_df <- data.frame(krg_spdf@coords, pred = krg_spdf@data$pred)

# find grid point closest to Maasband
suppressMessages(library(ggmap))
pt <- as.numeric(geocode("Maasband"))       # longlat of Maasband
pts <- as.matrix(krg_df[c("x", "y")])       # longlat of grid points
distVect <- spDistsN1(pts = pts, pt = pt, longlat = T)  # distance vector
indx <- which(distVect == min(distVect))
xy0 <- as.numeric(krg_df[indx,][c("x", "y")])   # nearest longlat
krg0 <- krg_df[indx, ]$pred                     # value @nearest longlat

# get meuse map and overlay kriged data
lon <- range(krg_df$x)
lat <- range(krg_df$y)
meuse_map <- get_map(location = c(lon = mean(lon), lat = mean(lat)),
                     zoom = 13)
suppressMessages(library(RColorBrewer))
print(ggmap(meuse_map, extent = "normal", maprange = F) +
        stat_summary_2d(aes(x = x, y = y, z = pred),
                        binwidth = c(0.001,0.001),
                        alpha = 0.5,
                        data = krg_df) +
        scale_fill_gradientn(name = "Copper",
                             colours = brewer.pal(6, "YlOrRd")) +
        geom_point(aes(x = pt[1], y = pt[2]),     # Maasband point
                   color = "red",
                   size = 6) +
        geom_point(aes(x = xy0[1], y = xy0[2]),   # nearest grid point
                   color = "blue",
                   size = 6) +
        coord_cartesian(xlim = lon, ylim = lat, expand = 0) +
        theme(aspect.ratio = 1))

# detach all user-loaded packages and personal environment(s)
source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R")
detachAll(unload = F)   # "unload = F" avoids sp/rgeos package load error
detachAll(unload = T)   # second call with "unload = T" seems to work
