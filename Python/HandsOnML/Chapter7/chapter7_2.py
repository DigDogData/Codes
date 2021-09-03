#################################################################################
# train a 'soft' voting classifier
# (highest probable class, averaged over all individual classifier probabilities)
# (classifier must have 'predict_proba()' method for computing probability)
# (SVC does not have it by default: setting 'probability=True' will make SVC use
# cross-validation, which adds predict_proba() method but slows down trainig)
#################################################################################
# load modules
import numpy as np
import pandas as pd
import sklearn
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("pandas version:", pd.__version__)
print("numpy version:", np.__version__)
print("sklearn version:", sklearn.__version__)

# get data
X, y = datasets.make_moons(n_samples=10000, noise=0.5)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.33)
print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)

# train models for soft voting
log_clf = LogisticRegression(solver="lbfgs")
rnd_clf = RandomForestClassifier(n_estimators=100)
svm_clf = SVC(gamma="scale", probability=True)
voting_clf = VotingClassifier(
    estimators=[("lr", log_clf), ("rf", rnd_clf), ("svc", svm_clf)], voting="soft"
)
voting_clf.fit(X_train, y_train)

# evaluate models
for clf in [log_clf, rnd_clf, svm_clf, voting_clf]:
    clf.fit(X_train, y_train)
    y_hat = clf.predict(X_val)
    print(clf.__class__.__name__, ":", accuracy_score(y_val, y_hat))
