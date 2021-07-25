rm(list=ls())
if(!is.null(dev.list())) dev.off()

library(caret)
library(doSNOW)
library(glmnet)

setwd("C:/Users/Roy/Documents/Data Analysis/Codes/DataCamp")

overfit <- read.csv("../Data/overfit.csv")

set.seed(1234)
myControl <- trainControl(
  method = "cv",
  number = 10,
  summaryFunction = twoClassSummary,
  classProbs = T,
  verboseIter = T,
  allowParallel = F
)

# for each alpha, glmnet fits all lambda simultaneously
# ("submodeling" => collapses entire tuning grid to 2 model fits)
myGrid <- expand.grid(
  alpha = 0:1,
  lambda = seq(0.0001, 0.1, length=10)
)

# tuning grid uses 3 values of alpha and 3 values of lambda (for tuning)default)
cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores-1, type="SOCK")
registerDoSNOW(cl)

myModel <- train(
  y ~ .,
  overfit,
  method = "glmnet",
  metric = "ROC",
  tuneGrid = myGrid,
  trControl = myControl
)

stopCluster(cl)

print(plot(myModel))

# plot full regularization path (all models with alpha = 0)
# this plot is specific to glmnet
print(plot(myModel$finalModel))

detach(package:glmnet)
detach(package:doSNOW)
detach(package:caret)
detach(package:ggplot2)   # ggplot2 detached after caret (to avoid error)
