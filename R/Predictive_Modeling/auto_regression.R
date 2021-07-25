#====================================
# REGRESSION PROBLEM WITH AUTOS DATA
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
source("Libs/impute_NA.R")
source("Libs/select_MODEL.R")
source("Libs/select_FEATURES.R")

#===========================
# get data
#===========================
autoData <- read.csv("Data/Autos.csv", check.names = F, strip.white = T,
                     na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)
makes <- read.csv("Data/Makes.csv", check.names = F, strip.white = T,
                  na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

#===========================
# prep data
#===========================
# add make info from makes data
autoData <- autoData %>% left_join(makes, by='make-id')

# add a new label for log-transformed label 'price'
autoData <- autoData %>% mutate(lnprice = log(price))

# consolidate cylinder numbers to fewer categories
autoData <- autoData %>%
  mutate(`num-of-cylinders` = ifelse(`num-of-cylinders` %in% c("four","three","two"), "four-or-less",
                                     ifelse(`num-of-cylinders` %in% c("five","six"), "five-six", "eight-or-more")))

# remove unneeded features
dropCols <- c('symboling', 'normalized-losses', 'make-id', 'price')
autoData <- autoData[, !(names(autoData) %in% dropCols)]

# check for any NA data (returns column names with NA value)
names(autoData)[apply(is.na(autoData), 2, any)]

# impute NA if any (numeric default "knnImpute", categorical default "Unknown")
autoData <- impute.NA(autoData)

# scale data
#pre <- preProcess(autoData, method = c("center", "scale"))
#pre <- preProcess(autoData, method = "range")
#autoData <- predict(pre, autoData)

# transform all character columns to factor/category
colChars <- names(autoData)[sapply(autoData, is.character)]
autoData[, colChars] <- lapply(autoData[, colChars], factor)

# remove any duplicated rows
autoData <- autoData %>% filter(!duplicated(autoData, ))

# identify any zero-variance and/or near-zero-variance predictor
nzv <- nearZeroVar(autoData, saveMetrics = T)
nzv

#===========================
# split data
#===========================
# 70%/30% split
set.seed(42)
inTrain <- createDataPartition(autoData$lnprice, p=0.7, list=F)
trainData <- autoData[inTrain, ]
testData <- autoData[-inTrain, ]

#============================================================================
# train model (model = "glm"/"rf"/"boost"/"nnet"/"mars"/"svm"/"knn")
#============================================================================
# set up parallel processing (#cores - 1)
cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores - 1, type="SOCK")
registerDoSNOW(cl)

cat(noquote("================================\n"))
cat(noquote("model training begins...\n"))
set.seed(42)
start_time <- Sys.time()
formula <- as.formula("lnprice ~ .")
fit <- train.model(formula, trainData, model = "knn", isFormula = T)
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
features <- select.features(vimp1, vimp2, names(autoData))

#=================
# score model
#=================
# make predictions on test set (using best tune)
score <- predict(fit, testData)

#=================
# evaluate model
#=================
performance <- postResample(pred = score, obs = testData$lnprice)
print(performance)

detach(package:doSNOW)
detach(package:caret)
detach(package:dplyr)
