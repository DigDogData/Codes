################################################################################
# Kernel PCA: 'kernel trick' (mapping instances to high-dimensional feature
# space using nonlinear kernels, turning nonlinear decision boundary in original
# space to linear decision boundary in high-D feature space) can be used here:
# performing complex nonlinear projections to reduce dimensionality
################################################################################
# load modules
import numpy as np
import pandas as pd
import matplotlib
import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import KernelPCA
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

print("----------------------------------")
print("numpy version:", np.__version__)
print("pandas version:", pd.__version__)
print("matplotlib version:", matplotlib.__version__)
print("sklearn version:", sklearn.__version__)
print("----------------------------------")

# Swiss roll data
X, _ = datasets.make_swiss_roll(n_samples=1000, noise=1)

# kPCA model
rbf_pca = KernelPCA(n_components=2, kernel="rbf", gamma=0.04, n_jobs=-1)
X_reduced = rbf_pca.fit_transform(X)
print(X.shape, X_reduced.shape)

# selecting kernel + tuning hyperparameters with MNIST data:
# (kPCA is unsupervised learning, so no performance measure is available
# to select best kernel+hyperparameters; it can be used with a supervised
# learner (e.g. a classifier) and grid search to find best parameters to
# optimize the learner's performance
X2, y = datasets.fetch_openml(name="mnist_784", return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.33)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# pipelining 2-dimensional kPCA with logistic regressor classifier
clf = Pipeline([("kpca", KernelPCA(n_components=2)), ("log_reg", LogisticRegression())])
param_grid = [
    {"kpca__gamma": np.linspace(0.03, 0.05, 5), "kpca__kernel": ["rbf", "sigmoid"]}
]
# grid search to tune hyperparameters to optimize classifier accuracy
grid_search = GridSearchCV(clf, param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train[:10000], y_train[:10000])
print("grid_search_best_params_:", grid_search.best_params_)

# unsupervised tuning to yield lowest reconstruction error (p220 of book)
rbf_pca = KernelPCA(
    n_components=2, kernel="rbf", gamma=0.0433, fit_inverse_transform=True
)
X_reduced = rbf_pca.fit_transform(X)  # use swiss roll data
X_preimage = rbf_pca.inverse_transform(X_reduced)
print(mean_squared_error(X, X_preimage))  # reconstruction preimage error
# grid search can now be used like before to minimize this error
