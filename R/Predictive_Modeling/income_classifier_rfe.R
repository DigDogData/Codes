#===========================================================================
# CLASSIFICATION/LOGISTIC REGRESSION PROBLEM WITH INCOME DATA USING glmnet()
#===========================================================================
# clear workspace, console and plots (if present)
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# attach library packages
library(caret)
library(dplyr)
library(doSNOW)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

#===========================
# get data
#===========================
incomeData <- read.csv("Data/Adult Census Income Binary Classification dataset.csv",
                        check.names=F, strip.white=T, na.strings="?")

#===========================
# prep data
#===========================
# remove unneeded features
dropCols <- c('workclass','education','occupation','capital-gain',
              'capital-loss','native-country')
incomeData <- incomeData[, !(names(incomeData) %in% dropCols)]

# check for any NA data (returns column names with NA value)
names(incomeData)[apply(is.na(incomeData), 2, any)]

# remove any duplicated rows
incomeData <- incomeData %>% filter(!duplicated(incomeData, ))

# normalize (minmax) all numeric features
pre.process <- preProcess(incomeData, method = c("range"))
incomeData <- predict(pre.process, incomeData)

# replace income factor levels ("<=50K",">50K") by valid R names ("lo","hi")
levels(incomeData$income) <- c("lo", "hi")

#===========================
# split data
#===========================
# 70%/30% split via stratified sampling (heavily imbalanced data)
set.seed(1234)
rowIndx <- createDataPartition(incomeData$income, p=0.7, list=F)
trainData <- incomeData[rowIndx, ]
testData <- incomeData[-rowIndx, ]

#=================
# train model
#=================
# create a vector of feature subsets to evaluate
featureNames <- names(incomeData)[!(names(incomeData) %in% "income")]
featureSizes <- seq(1, length(featureNames)-1, by=1)

# expanded list of performance measures
fiveStats <- function(...) c(twoClassSummary(...), defaultSummary(...))

# create resampling datasets to use for all models
reps <- 2
index <- createMultiFolds(trainData$income, times = reps)

cat(noquote("================================\n"))
cat(noquote("model training begins...\n"))
# set up control functions for rfe()
# (uses caretFuncs & detailed stats, and allowParallel=TRUE by default)
rfe.control <- rfeControl(method = "repeatedcv",
                          number = 10,
                          repeats= reps,
                          saveDetails = T,
                          returnResamp = "final",
                          index = index,
                          verbose = T)
rfe.control$functions <- caretFuncs
rfe.control$functions$summary <- fiveStats

# set up control functions for train(), to be passed to rfe()
# (allowParallel set to FALSE to prevent double parallelizing)
train.control <- trainControl(method = "cv",
                              number = 10,
                              repeats = 1,
                              classProbs = T,
                              search = "grid",
                              verboseIter = T,
                              allowParallel = F)

# set up search grid for tuning parameters (50 X 2 = 100 models)
tune.grid <- expand.grid(lambda = seq(0.0001,0.1,length=50),  # regulatization param
                         alpha = c(0,0.1))    # L2 => alpha=0, L1 => alpha=1

# set up parallel processing
cl <- makeCluster(4, type="SOCK")
registerDoSNOW(cl)

# train model
start_time <- Sys.time()
glmTune <- rfe(income ~ .,
               data = trainData,
               sizes = featureSizes,
               rfeControl = rfe.control,
               metric = "ROC",
               # now train() arguments follow
               method = "glmnet",
#               trControl = train.control,
#               tuneGrid = tune.grid)
              trControl = train.control)
end_time <- Sys.time()
cat(noquote("model training ends...\n"))
print(end_time - start_time)
cat(noquote("================================\n"))

# stop processes after completion
stopCluster(cl)

browser()

# look up tuning profile and best tune
glmTune$results
glmTune$bestTune

# get important features
source("Libs/select_FEATURES.R")
vimp <- varImp(glmTune, scale=F)
features <- select.features(vimp, names(incomeData))

#=================
# score model
#=================
# make predictions & probabilities on test set
scores <- predict(glmTune, testData)
probs <- predict(glmTune, testData, type = "prob")

#================
# evaluate model
#================
source("Libs/eval_MODEL.R")
eval.MODEL(scores, testData$income, probs)


detach(package:doSNOW)
detach(package:dplyr)
detach(package:caret)
detach(package:ggplot2)   # ggplot2 detached after caret (to avoid error)
