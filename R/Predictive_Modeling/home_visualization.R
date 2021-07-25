# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(caret)
library(dplyr)
library(doSNOW)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/to_FACTOR.R", envir = myEnv)
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/impute_NA.R", envir = myEnv)
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/select_MODEL.R", envir = myEnv)
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/select_FEATURES.R", envir = myEnv)
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# get data
data <- read.csv("Data/HomeSaleData.csv", check.names = F, strip.white = T,
                  na.strings=c(""," ","?","NA","na","<NA>"), stringsAsFactors = F)

# convert year_built to character
data$year_built <- as.character(data$year_built)

# transform all character columns to factor/category
cols <- names(data)[sapply(data, is.character)]
data[, cols] <- to.factor(data, cols)  # add ", Rname = T" for valid R name

# check number of NAs
#summary(data)



# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
