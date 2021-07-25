########################################
## for regression model
########################################
# Mean Squared Error (MSE)
def mse(data, prediction):
    from sklearn.metrics import mean_squared_error
    return mean_squared_error(data, prediction)

########################################
## for classifier model
########################################
# jaccard index
def jaccard(data, prediction):
#    from sklearn.metrics import jaccard_similarity_score
#    return jaccard_similarity_score(data, prediction)
    from sklearn.metrics import jaccard_score
    return jaccard_score(data, prediction)

# confusion matrix
def cfmatrix(data, prediction, labels=None):
    from sklearn.metrics import confusion_matrix
    return confusion_matrix(data, prediction, labels=labels)

# classification report (based on confusion matrix)
def cfreport(data, prediction):
    from sklearn.metrics import classification_report
    return classification_report(data, prediction)

# f-score
def f1score(data, prediction, average=None):
    from sklearn.metrics import f1_score
    return f1_score(data, prediction, average=average)  # default 'binary'
    
# log loss
def logloss(data, probs):
    from sklearn.metrics import log_loss
    return log_loss(data, probs)
