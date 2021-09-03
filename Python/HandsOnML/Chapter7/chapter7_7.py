######################################################################
# Exercise #1: Split MNIST data into training + validation + test sets
######################################################################
import numpy as np
import matplotlib
import sklearn
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score as acc

print("numpy version:", np.__version__)
print("matplotlib version:", matplotlib.__version__)
print("sklearn version:", sklearn.__version__)

# load data
X, y = datasets.fetch_openml(name="mnist_784", return_X_y=True)
print(X.shape, y.shape)

# shuffle and sample
random_indices = np.random.permutation(X.shape[0])
X = X[random_indices]
y = y[random_indices]

print("y[33]:", y[33])
plt.imshow(X[33].reshape(28, 28), cmap="binary")
plt.axis("off")
plt.show()

# split data
X_train, y_train = X[:50000], y[:50000]
X_val, y_val = X[50000:60000], y[50000:60000]
X_test, y_test = X[60000:], y[60000:]
print(
    X_train.shape, y_train.shape, X_val.shape, y_val.shape, X_test.shape, y_test.shape
)

############################################################################
# Exercise #2: Train RF Classifier + Extra-Trees Classifier + SVM Classifier
############################################################################
rfc = RandomForestClassifier(n_estimators=10)
etc = ExtraTreesClassifier(n_estimators=10)
svc = SVC(probability=True)

# truncate data to save time
X_train, y_train = X_train[:5000], y_train[:5000]
X_val, y_val = X_val[:1000], y_val[:1000]
X_test, y_test = X_test[:1000], y_test[:1000]
print(
    X_train.shape, y_train.shape, X_val.shape, y_val.shape, X_test.shape, y_test.shape
)

# train and evaluate models
rfc.fit(X_train, y_train)
etc.fit(X_train, y_train)
svc.fit(X_train, y_train)

print(
    "RF Classifier score:",
    acc(y_val, rfc.predict(X_val)),
    "\nET Classifier score:",
    acc(y_val, etc.predict(X_val)),
    "\nSV Classifier score:",
    acc(y_val, svc.predict(X_val)),
)

############################################################################
# Exercise #3: Combine them into an ensemble with soft or hard voting, to
# outperform each individual classifier on validation set
############################################################################
hard_voter = VotingClassifier(
    estimators=[
        ("random forest", rfc),
        ("extra trees", etc),
        ("support vector classifier", svc),
    ],
    n_jobs=-1,
)
hard_voter.fit(X_train, y_train)
soft_voter = VotingClassifier(
    estimators=[
        ("random forest", rfc),
        ("extra trees", etc),
        ("support vector classifier", svc),
    ],
    voting="soft",
    n_jobs=-1,
)
soft_voter.fit(X_train, y_train)
print("Hard voter score:", acc(y_val, hard_voter.predict(X_val)))
print("Soft voter score:", acc(y_val, soft_voter.predict(X_val)))

############################################################################
# Exercise #4: Score best voter ensemble on test set and compare with
# individual classifiers
############################################################################
print(
    "RF Classifier score on test set:",
    acc(y_test, rfc.predict(X_test)),
    "\nET Classifier score on test set:",
    acc(y_test, etc.predict(X_test)),
    "\nSV Classifier score on test set:",
    acc(y_test, svc.predict(X_test)),
)
print("Hard voter score on test set:", acc(y_test, hard_voter.predict(X_test)))
print("Soft voter score on test set:", acc(y_test, soft_voter.predict(X_test)))

############################################################################
# Exercise #5: Create a new training set from predictions of each classifier
# on validation set: each training instance is a vector of predictions from
# all classifiers for an image, and target/label is the class image
############################################################################
rfc_preds = rfc.predict(X_val)[..., None]
etc_preds = etc.predict(X_val)[..., None]
svc_preds = svc.predict(X_val)[..., None]
print(rfc_preds.shape, etc_preds.shape, svc_preds.shape)
X_val_ = np.concatenate((rfc_preds, etc_preds, svc_preds), axis=1)
print(X_val_.shape)

##############################################################################
# Exercise #6: Stacking Ensemble: Train a classifier on this new training set;
# Model trained on outputs of predictors is a 'Blender' or a 'Meta Learner';
# Blender together wih the predictors forms a 'stacking ensemble'
# Evaluate this blender on the test set
##############################################################################
rfc_ = RandomForestClassifier(n_estimators=10)
rfc_.fit(X_val_, y_val)

##############################################################################
# Exercise #7: # Evaluate this ensemble on the test set
##############################################################################
rfc_preds = rfc.predict(X_test)[..., None]
etc_preds = etc.predict(X_test)[..., None]
svc_preds = svc.predict(X_test)[..., None]
X_test_ = np.concatenate((rfc_preds, etc_preds, svc_preds), axis=1)
print(X_test_.shape)
y_test_ = rfc_.predict(X_test_)
print("Stacking Ensemble score:", acc(y_test, y_test_))
# score comparable with hard/soft voter
