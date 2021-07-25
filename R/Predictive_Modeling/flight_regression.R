#====================================
# REGRESSION PROBLEM WITH AUTOS DATA
#====================================
# clear workspace, console and plots
#rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# attach packages and headers
library(caret)
library(dplyr)
library(doSNOW)
source("Libs/impute_NA.R")
source("Libs/to_FACTOR.R")
source("Libs/select_MODEL.R")
source("Libs/select_FEATURES.R")

#===========================
# get data
#===========================
#flightData <- read.csv("Data/Flight Delays Data.csv", check.names = F,
#                       strip.white = T, na.strings=c(""," ","?","NA","na"),
#                       stringsAsFactors = F)

# truncate data (for manageability)
#flightData <- flightData[sample(1:nrow(flightData), 100000), ]

#===========================
# prep data
#===========================
# remove unneeded features
#dropCols <- c('Year', 'DepDel15', 'ArrDel15', 'Cancelled')
#flightData <- flightData[, !(names(flightData) %in% dropCols)]

# check for any NA data (returns column names with NA value)
#names(flightData)[apply(is.na(flightData), 2, any)]

# impute NA if any (numeric default "knnImpute", categorical default "Unknown")
#flightData <- impute.NA(flightData)

# transform all character columns to factor/category
#cols <- names(flightData)[sapply(flightData, is.character)]
#flightData[, cols] <- to.factor(flightData, cols)

# remove any duplicated rows
#flightData <- flightData %>% filter(!duplicated(flightData, ))

# identify any zero-variance and/or near-zero-variance predictor
#nzv <- nearZeroVar(flightData, saveMetrics = T)
#nzv

#===========================
# split data
#===========================
# 70%/30% split
set.seed(42)
inTrain <- createDataPartition(flightData$ArrDelay, p=0.7, list=F)
trainData <- flightData[inTrain, ]
testData <- flightData[-inTrain, ]

#=========================================================================
# train model (~1.5min with glmnet, ~28min with xgboost, ~*** with ranger)
#=========================================================================
# set up parallel processing (#cores - 1)
cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores - 1, type="SOCK")
registerDoSNOW(cl)

cat(noquote("================================\n"))
cat(noquote("model training begins...\n"))
set.seed(42)
start_time <- Sys.time()
formula <- as.formula("ArrDelay ~ .")
fit <- train.model(formula, trainData, model = "rf")   # "glm"/"rf"/"boost"
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
features <- select.features(vimp1, vimp2, names(flightData))

#=================
# score model
#=================
# make predictions on test set (using best tune)
score <- predict(fit, testData)

#=================
# evaluate model
#=================
performance <- postResample(pred = score, obs = testData$ArrDelay)
print(performance)
