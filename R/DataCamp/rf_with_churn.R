rm(list=ls())
#cat("\014")
#if(!is.null(dev.list())) dev.off()

library(caret)
library(C50)
library(doSNOW)
library(mlbench)

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

# default tuneGrid is already good for this model, external tuing not needed

# change positive level from "yes" to "no"
churnTrain$churn <- factor(churnTrain$churn, levels = c("no", "yes"))
X <- churnTest[, !(names(churnTest) %in% "churn")]
Y <- churnTest$churn
model_rf <- train(
#  x = X, y = Y,
  churn ~ .,
  churnTrain,
  metric = "ROC",
  method = "ranger",
  trControl = myControl
)

stopCluster(cl)

print(plot(model_rf))


