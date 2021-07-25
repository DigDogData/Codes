rm(list=ls())
if(!is.null(dev.list())) dev.off()

library(caret)
library(doSNOW)
library(mlbench)

data(Sonar)

cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores-1, type="SOCK")
registerDoSNOW(cl)

set.seed(42)
myGrid <- data.frame(mtry = c(2, 3, 4, 5, 10, 20))
myModel <- train(
  Class ~ .,
  data = Sonar,
  method = "ranger",
  tuneLength = 10,     # default tuneLength = 3
  trControl = trainControl(method = "cv", number = 5, verboseIter = T)
#  tuneGrid = myGrid
)

stopCluster(cl)

print(plot(myModel))

detach(package:mlbench)
detach(package:doSNOW)
detach(package:caret)
detach(package:ggplot2)   # ggplot2 detached after caret (to avoid error)
