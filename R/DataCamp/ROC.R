rm(list=ls())
if(!is.null(dev.list())) dev.off()

library(caret)
library(doSNOW)

data(Sonar)


model <- glm(Class ~ ., family = binomial(link = "logit"), train)

p <- predict(model, test, type = "response")

# model predicts probabilities, we need classes, so cut these probabilities
p_class <- ifelse(p > 0.5, "M", "R")

# now create confusion matrix (2-way frequency table)
print(confusionMatrix(p_class, test[["Class"]]))

# to catch more mines, at the expense of false positives, lower cutoff (e.g. 10%)
# to be more certain of predicted mines, at th expense of catching fewer
# of them, raise cutoff (e.g. 90%) => choosing a cutoff is balancing between
# TP rate and FP rate
# to get better certainty (high TP rate) at the expense of fewer mines predicted
p_class <- ifelse(p > 0.9, "M", "R")
print(confusionMatrix(p_class, test[["Class"]]))

# manullay computing best classification threshold is difficult
# hundreds of CFMatrix need to be computed, and visually inspected to find the one
# we like; better way is to let computer figure this out iteratively by computing
# TP and FP rate for each possible threshold, and visualize them to find the best tradeoff
# ==> ROC curve
#
