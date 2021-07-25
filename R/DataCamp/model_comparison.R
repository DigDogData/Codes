rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

library(caret)
library(C50)
library(doSNOW)
library(mlbench)

data(churn)

# make a list of models
model_list <- list(
  glmnet = model_glmnet,
  rf = model_rf
)

# collect resamples from CV folds
resamps <- resamples(model_list)
print(resamps)

# summarize results
print(summary(resamps))


# box-and-whisker plot of model comparison
bwplot(resamps, metric = "ROC")

# dot plot
dotplot(resamps, metric = "ROC")

# density plot
densityplot(resamps, metric = "ROC")

# scatterplot
xyplot(resamps, metric = "ROC")

# for many models dotplot is nice
dotplot(lot_of_models, metric = "ROC")
