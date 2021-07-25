rm(list=ls())
if(!is.null(dev.list())) dev.off()

library(caret)
library(doSNOW)

data(mtcars)

# introduce some random NA
mtcars[sample(1:nrow(mtcars), 10), "hp"] <- NA

cores <- as.numeric(Sys.getenv('NUMBER_OF_PROCESSORS'))
cl <- makeCluster(cores-1, type="SOCK")
registerDoSNOW(cl)

y <- mtcars$mpg
x <- mtcars[, 2:4]

set.seed(42)
#model <- train(x, y)
model <- train(x, y,
               # chained preProcessing (order is important!)
               preProcess = c("medianImpute", "center", "scale", "pca"),
               method = "glm"
)
#model <- train(x, y, method = "glm", preProcess = "knnImpute")

stopCluster(cl)

print(min(model$results$RMSE))
