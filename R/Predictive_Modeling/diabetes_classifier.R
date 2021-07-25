#===========================================
# CLASSIFICATION PROBLEM WITH DIABETES DATA
#===========================================
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
diabetesData <- read.csv("Data/Diabetes Data.csv", check.names = F, strip.white = T,
                     na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)
admitInfo <- read.csv("Data/Admissions mapping.csv", check.names = F, strip.white = T,
                  na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

#===========================
# prep data
#===========================
# collapse similar levels in admission_type_description
admitInfo <- admitInfo %>% mutate(admission_type_description =
                        ifelse(admission_type_description %in% 
                                 c("Not Available", "NULL", "Not Mapped"),
                               "Unknown", admission_type_description))

# add admission type info from admissions data
diabetesData <- diabetesData %>% left_join(admitInfo, by='admission_type_id')

# remove unneeded features
#dropCols <- c('admission_type_id', 'encounter_id', 'patient_nbr', 'examide', 'citoglipton')
dropCols <- c('admission_type_id', 'encounter_id', 'patient_nbr')
diabetesData <- diabetesData[, !(names(diabetesData) %in% dropCols)]

# convsolidate response label "readmitted" to 2 classes (YES/NO) 
diabetesData <- diabetesData %>% mutate(readmitted =
                                          ifelse(readmitted!="NO", "YES", readmitted))

# impute NA if any (numeric default "knnImpute", categorical default "Unknown")
diabetesData <- impute.NA(diabetesData)

# transform all character columns to factor/category
cols <- names(diabetesData)[sapply(diabetesData, is.character)]
diabetesData[, cols] <- lapply(diabetesData[, cols], factor)

# remove any duplicated rows
diabetesData <- diabetesData %>% filter(!duplicated(diabetesData, ))

# identify any zero-variance and/or near-zero-variance predictor
nzv <- nearZeroVar(diabetesData, saveMetrics = T)
nzv

# remove zero-var features
dropCols <- c('examide', 'citoglipton')
diabetesData <- diabetesData[, !(names(diabetesData) %in% dropCols)]

# remove near-zero-var features
#dropCols <- c('acetohexamide', 'glimepiride-pioglitazone', 'metformin-pioglitazone')
#diabetesData <- diabetesData[, !(names(diabetesData) %in% dropCols)]

# make YES positive class
diabetesData$readmitted <- factor(diabetesData$readmitted, levels = c("YES","NO"))

#===========================
# split data
#===========================
# 70%/30% split via stratified sampling (heavily imbalanced data)
set.seed(1234)
inTrain <- createDataPartition(diabetesData$readmitted, p=0.7, list=F)
trainData <- diabetesData[inTrain, ]
testData <- diabetesData[-inTrain, ]

# examine proportions for class label 'income' across splits
prop.table(table(diabetesData$readmitted))
prop.table(table(trainData$readmitted))
prop.table(table(testData$readmitted))

#========================================================================
# train model (~31mins with glmnet, ~4hrs with xgboost, ~*** with ranger)
#========================================================================
# set up parallel processing (#cores - 1)
cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores - 1, type="SOCK")
registerDoSNOW(cl)

cat(noquote("================================\n"))
cat(noquote("model training begins...\n"))
set.seed(42)
start_time <- Sys.time()
formula <- as.formula("readmitted ~ .")
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
# vimp2 returns same importance column for each class label => merge columns
row.names <- rownames(vimp2)
vimp2 <- data.frame(Overall = rowMeans(vimp2))
rownames(vimp2) <- row.names
features <- select.features(vimp1, vimp2, names(diabetesData))

#=================
# score model
#=================
# compute predictions & probabilities on test set (using best tune)
scores <- predict(fit, testData)
probs <- predict(fit, testData, type = "prob")

#================
# evaluate model
#================
eval.MODEL(scores, testData$readmitted, probs)
