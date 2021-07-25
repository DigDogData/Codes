#=========================================
# CLASSIFICATION PROBLEM WITH INCOME DATA
#=========================================
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
#source("Libs/to_FACTOR.R")
source("Libs/impute_NA.R")
source("Libs/select_MODEL.R")
source("Libs/eval_MODEL.R")
source("Libs/select_FEATURES.R")

#===========================
# get data
#===========================
incomeData <- read.csv("Data/Adult Census Income Binary Classification dataset.csv",
                       check.names = F, strip.white=T, na.strings=c(""," ","?","NA","na"),
                       stringsAsFactors = F)

# truncate data for debugging
incomeData <- incomeData[sample(1:1000), ]

#===========================
# prep data
#===========================
# remove unneeded features
dropCols <- c('workclass','education','occupation','capital-gain',
              'capital-loss','native-country')
incomeData <- incomeData[, !(names(incomeData) %in% dropCols)]

# impute NA if any (numeric default "knnImpute", categorical default "Unknown")
incomeData <- impute.NA(incomeData)

# transform all character columns to factor/category
cols <- names(incomeData)[sapply(incomeData, is.character)]
incomeData[, cols] <- lapply(incomeData[, cols], factor)
#if(length(cols)>0) incomeData <- to.factor(incomeData, cols)

# remove any duplicated rows
incomeData <- incomeData %>% filter(!duplicated(incomeData, ))

# identify any zero-variance and/or near-zero-variance predictor
nzv <- nearZeroVar(incomeData, saveMetrics = T)
nzv

# use intuitive response class names
levels(incomeData$income) <- c("lo", "hi")

#===========================
# split data
#===========================
# 70%/30% split via stratified sampling (heavily imbalanced data)
set.seed(42)
inTrain <- createDataPartition(incomeData$income, p=0.7, list=F)
trainData <- incomeData[inTrain, ]
testData <- incomeData[-inTrain, ]

# examine proportions for class label 'income' across splits
prop.table(table(incomeData$income))
prop.table(table(trainData$income))
prop.table(table(testData$income))

#===================================================================
# train model (model = "glm"/"rf"/"boost"/"nnet"/"mars"/"svm"/"knn")
#===================================================================
# set up parallel processing (#cores - 1)
cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores - 1, type="SOCK")
registerDoSNOW(cl)

cat(noquote("================================\n"))
cat(noquote("model training begins...\n"))
set.seed(42)
start_time <- Sys.time()
formula <- as.formula("income ~ .")
fit <- train.model(formula, trainData, model = "rf", isFormula = F)
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
# vimp2 returns same importance column for each class label => merge columns
row.names <- rownames(vimp2)
vimp2 <- data.frame(Overall = rowMeans(vimp2))
rownames(vimp2) <- row.names
features <- select.features(vimp1, vimp2, names(incomeData))

#=================
# score model
#=================
# compute predictions & probabilities on test set (using best tune)
scores <- predict(fit, testData)
probs <- predict(fit, testData, type = "prob")

#================
# evaluate model
#================
eval.MODEL(scores, testData$income, probs)

detach(package:doSNOW)
detach(package:caret)
detach(package:dplyr)
