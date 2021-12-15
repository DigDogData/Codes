# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# load data
suppressMessages(library(sp))
suppressMessages(library(gstat))
data(meuse)
data(meuse.grid)

# convert meuse data to SpatialPointsDataFrame
coordinates(meuse) <- ~ x + y

# compute variogram
meuse$logCopper <- log(meuse$copper)
v <- variogram(object = logCopper ~ 1,
               locations = meuse,
               cutoff = 1300,
               width = 90)

# fit variogram model
vm <- vgm(psill = 0.32,     # semivariance value at saturation
          model = "Sph",
          range = 900,      # distance at saturation
          nugget = 0.09)    # y-intercept at distance = 0
vmfit <- fit.variogram(object = v, model = vm)
print(vmfit)
print(plot(v, plot.numbers = T, model = vmfit))

# convert meuse grid to SpatialPixelDataFrame
# (SpatialPointsDataFrame on a regular grid)
coordinates(meuse.grid) <- ~ x + y    # convert to SpatialPointsDF
gridded(meuse.grid) <- T              # convert to SpatialPixelDF

################################################################
# "ordinary" kriging (model variable depends on itself) on grid
################################################################
krg <- krige(formula = logCopper ~ 1,
             locations = meuse,
             newdata = meuse.grid,
             model = vmfit)
print(spplot(krg, zcol = "var1.pred", asp = 1, col.regions = bpy.colors(64),
             main = "OK prediction, log-ppm Copper"))

######################################################
# indicator kriging (for binary/categorical response)
######################################################
meuse$copper.i <- (meuse$copper < 50)   # generate (logical) indicator column
vi <- variogram(object = copper.i ~ 1,  # variogram
                locations = meuse,
                cutoff = 1300)
print(plot(vi, plot.numbers = T))
vimfit <- fit.variogram(object = vi,    # model fitting
                        model = vgm(psill = 0.21,
                                    model = "Sph",
                                    range = 800,
                                    nugget = 0.1))
print(vimfit)
print(plot(vi, plot.numbers = T, model = vimfit))
krg.i <- krige(formula = copper.i ~ 1,  # indicator kriging
               locations = meuse,
               newdata = meuse.grid,
               model = vimfit)
print(spplot(krg.i, zcol = "var1.pred", asp = 1, col.regions = heat.colors(64),
             main = "Probability (Copper < 50)"))

######################################################
# mixed predictors (response depends on predictor(s))
######################################################




# detach all user-loaded packages and personal environment(s)
#detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
