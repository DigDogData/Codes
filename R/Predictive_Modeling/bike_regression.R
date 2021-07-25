#====================================
# REGRESSION PROBLEM WITH BIKES DATA
#====================================
# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# attach packages and headers
library(caret)
library(dplyr)
library(doSNOW)
source("Libs/to_NAME.R")
source("Libs/to_FACTOR.R")
source("Libs/impute_NA.R")
source("Libs/select_MODEL.R")
source("Libs/select_FEATURES.R")

#===========================
# get data
#===========================
bikeData <- read.csv("Data/Bike Rental UCI dataset.csv", check.names = F,
                     strip.white = T, na.strings=c(""," ","?","NA","na"),
                     stringsAsFactors = F)

#===========================
# prep data
#===========================
# replace weekday and month number by name
bikeData$weekday <- to.dayname(bikeData, "weekday")
bikeData$mnth <- to.monthname(bikeData, "mnth")

# remove unneeded columns
dropCols <- c('instant', 'dteday', 'atemp', 'casual', 'registered')
bikeData <- bikeData[, !(names(bikeData) %in% dropCols)]

# check for any NA data (returns column names with NA value)
names(bikeData)[apply(is.na(bikeData), 2, any)]

# impute NA if any (numeric default "knnImpute", categorical default "Unknown")
bikeData <- impute.NA(bikeData)

# transform all character columns (and some non-char columns) to factor/category
cols <- names(bikeData)[sapply(bikeData, is.character)]
cols <- c(cols, "season", "yr", "hr", "holiday", "workingday", "weathersit")
bikeData[, cols] <- to.factor(bikeData, cols)  # add ", Rname = T" for valid R name

# reorder day & month factor levels chronoloigcally (default order alphabetical)
bikeData$weekday <- factor(bikeData$weekday, levels = c("Sunday", "Monday", "Tuesday",
                                                        "Wednesday", "Thursday", "Friday",
                                                        "Saturday"))
bikeData$mnth <- factor(bikeData$mnth, levels = c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))

# remove any duplicated rows
bikeData <- bikeData %>% filter(!duplicated(bikeData, ))

# identify any zero-variance and/or near-zero-variance predictor
nzv <- nearZeroVar(bikeData, saveMetrics = T)
nzv

#===========================
# split data
#===========================
# 70%/30% split
set.seed(42)
inTrain <- createDataPartition(bikeData$cnt, p=0.7, list=F)
trainData <- bikeData[inTrain, ]
testData <- bikeData[-inTrain, ]

#============================================================================
# train model (~34sec with glmnet, ~7min with xgboost, ~**** with ranger)
#============================================================================
# set up parallel processing (#cores - 1)
cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores - 1, type="SOCK")
registerDoSNOW(cl)

cat(noquote("================================\n"))
cat(noquote("model training begins...\n"))
set.seed(42)
start_time <- Sys.time()
formula <- as.formula("cnt ~ .")
fit <- train.model(formula, trainData, model = "boost")   # "glm"/"rf"/"boost"
end_time <- Sys.time()
cat(noquote("model training ends...\n"))
print(end_time - start_time)
cat(noquote("================================\n"))

# stop processes after completion
stopCluster(cl)

# look up tuning profile and best tune
fit$results
fit$bestTune
print(plot(fit))

# get important features
vimp1 <- varImp(fit, scale = F)$importance
vimp2 <- varImp(fit, scale = F, useModel = F)$importance
features <- select.features(vimp1, vimp2, names(bikeData))

#=================
# score model
#=================
# make predictions on test set (using best tune)
score <- predict(fit, testData)

#=================
# evaluate model
#=================
performance <- postResample(pred = score, obs = testData$cnt)
print(performance)
