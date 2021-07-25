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

# add a constant valued column
x$bad <- 1

set.seed(42)
#model <- train(x, y)
model <- train(x, y,
               # "zv" removes zero-variance predictor ("nzv" for near-zero V)
               # "pca" combines low-V and high-corr predictors to create a
               # single set of high-V perpendicular (perfectly uncorr) predictors
               preProcess = c("zv", "medianImpute", "center", "scale", "pca"),
               method = "glm"
)
#model <- train(x, y, method = "glm", preProcess = "knnImpute")

stopCluster(cl)

print(min(model$results$RMSE))
