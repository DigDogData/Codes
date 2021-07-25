rm(list=ls())
if(!is.null(dev.list())) dev.off()

library(caret)
library(doSNOW)

data(BloodBrain)

cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores-1, type="SOCK")
registerDoSNOW(cl)

set.seed(42)
model <- train(
  bbbDescr, logBBB, method = "glm",
  trControl = trainControl(method = "cv", number = 10, verboseIter = T),
#  preProcess = c("zv", "center", "scale")
#  preProcess = c("nzv", "center", "scale")
  preProcess = c("zv", "center", "scale", "pca")  # keeps low-V predictors (no "nzv") with "pca"
)

stopCluster(cl)

print(min(model$results$RMSE))
