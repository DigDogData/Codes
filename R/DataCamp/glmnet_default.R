rm(list=ls())
if(!is.null(dev.list())) dev.off()

library(caret)
library(glmnet)

setwd("C:/Users/Roy/Documents/Data Analysis/Codes/DataCamp")

overfit <- read.csv("../Data/overfit.csv")

set.seed(1234)
myControl <- trainControl(
  method = "cv",
  number = 10,
  summaryFunction = twoClassSummary,
  classProbs = T,
#  verboseIter = T,
  allowParallel = F
)

# tuning grid uses 3 values of alpha and 3 values of lambda (for tuning)default)
myModel <- train(
  y ~ .,
  overfit,
  method = "glmnet",
  metric = "ROC",
  trControl = myControl
)

print(plot(myModel))


detach(package:glmnet)
detach(package:caret)
detach(package:ggplot2)   # ggplot2 detached after caret (to avoid error)
