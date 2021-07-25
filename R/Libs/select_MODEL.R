#=========================
# FUNCTION TO SELECT MODEL
#=========================
train.model <- function(formula, data, model, isFormula = TRUE){
  
  # extract response and predictor names (for non-formula interface)
  response <- as.character(formula)[2]
  predictors <- names(data)[!(names(data) %in% response)]
  
  # define train control using repeat Cv
  ifelse(is.numeric(data[, response]),
         # if regression model
         train.control <- trainControl(method = "repeatedcv",
                                       number = 10,
                                       repeats= 5),
         # else if classifier model,
         # twoClassSummary (only for binary classifier) gives ROC metric
         # (default metric is Accuracy)
         train.control <- trainControl(method = "repeatedcv",
                                       number = 10,
                                       repeats= 5,
                                       classProbs = T,
                                       summaryFunction = twoClassSummary))
  
  # if glm
  if(model == "glm"){
    suppressMessages(library(glmnet))
    tune.grid <- expand.grid(lambda = seq(0.001,0.2,length=20),
                             alpha = c(0, 0.2, 0.4, 0.6, 0.8, 1))
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "glmnet",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "glmnet",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        trControl = train.control))
  }
  
  # if randomforest
  else if(model == "rf"){
    suppressMessages(library(mlbench))
    if(is.factor(data[, response])) train.control$classProbs <- TRUE  # needed for classifier
    tune.grid <- expand.grid(mtry = c(2, 3, 4, 5, 10, 20),
                             splitrule = c("variance", "extratrees"),
                             min.node.size = c(3, 5, 7))
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "ranger",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        importance = "permutation",
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "ranger",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        importance = "permutation",
                        trControl = train.control))
  }
  
  # if boost
  else if(model == "boost"){
    suppressMessages(library(xgboost))
    tune.grid <- expand.grid(eta = c(0.1, 0.125, 0.15),
                             nrounds = 100,
                             max_depth = 7:9,
                             min_child_weight = c(1.5, 2.0),
                             colsample_bytree = c(0.5, 0.6, 0.7),
                             gamma = 0,
                             subsample = 1)
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "xgbTree",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "xgbTree",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        trControl = train.control))
  }
  
  #==========================================
  # models below are for nonlinear regression
  #==========================================
  # if nnet (uses *average nnet* model, not base nnet)
  else if(model == "nnet"){
    suppressMessages(library(nnet))
    tune.grid <- expand.grid(decay = c(0, 0.01, 0.1),
                             size = 1:10)
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "nnet",
                        preProcess = c("zv", "center", "scale"),
                        linout = T,
                        trace = F,
                        maxit = 500,
                        MaxNWts = 5 * (length(predictors) + 1) + 5 + 1,
                        tuneGrid = tune.grid,
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "nnet",
                        preProcess = c("zv", "center", "scale"),
                        linout = T,
                        trace = F,
                        maxit = 500,
                        MaxNWts = 5 * (length(predictors) + 1) + 5 + 1,
                        tuneGrid = tune.grid,
                        trControl = train.control))
  }

  # if mars
  else if(model == "mars"){
    suppressMessages(library(earth))
    tune.grid <- expand.grid(.degree = 1:2,
                             .nprune = 2:38)
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "earth",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "earth",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = tune.grid,
                        trControl = train.control))
  }
  
  # if svm
  else if(model == "svm"){
    suppressMessages(library(kernlab))
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "svmRadial",   # or "svmLinear"/"svmPoly"
                        preProcess = c("zv", "center", "scale"),
                        tuneLength = 14,    # default grid search with 14 cost values
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "svmRadial",   # or "svmLinear"/"svmPoly"
                        preProcess = c("zv", "center", "scale"),
                        tuneLength = 14,    # default grid search with 14 cost values
                        trControl = train.control))
  }
  
  # if knn
  else if(model == "knn"){
    ifelse(isFormula,
           mod <- train(formula, data = data,
                        method = "knn",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = data.frame(k = 1:20),
                        trControl = train.control),
           mod <- train(x = data[, predictors], y = data[, response],
                        method = "knn",
                        preProcess = c("zv", "center", "scale"),
                        tuneGrid = data.frame(k = 1:20),
                        trControl = train.control))
  }

  mod
  
}