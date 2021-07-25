rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

library(caret)
library(C50)
library(doSNOW)
library(glmnet)

data(churn)

cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores-1, type="SOCK")
registerDoSNOW(cl)

set.seed(42)
myFolds <- createFolds(churnTrain$churn, k = 5)

myControl <- trainControl(
  summaryFunction = twoClassSummary,
  classProbs = T,
  verboseIter = T,
  savePredictions = T,
  index = myFolds       # trainConrtrol uses same CV folds to fit each model
)

X <- churnTest[, !(names(churnTest) %in% "churn")]
Y <- churnTest$churn
model_glmnet <- train(
#  x = X, y = Y,
  churn ~ .,
  churnTrain,
  metric = "ROC",
  method = "glmnet",
  tuneGrid = expand.grid(
    alpha = 0:1,
    lambda = 0:10/10
  ),
  trControl = myControl
)

stopCluster(cl)

print(plot(model_glmnet))
print(plot(model_glmnet$finalModel))

source("../Libs/select_FEATURES.R")
vimp <- varImp(model_glmnet, scale=F)$importance
predimp <- select.features(vimp, names(churnTest))


