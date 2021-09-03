import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.datasets import load_iris
from sklearn.datasets import make_moons
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit

###################################################
# Decision Tree Classifier
###################################################
iris = load_iris()
X = iris.data[:, 2:]  # petal length and width
y = iris.target
print(X.shape, y.shape)

tree_clf = DecisionTreeClassifier(max_depth=2)
tree_clf.fit(X, y)

# visualize trained tree
filename = "models/iris_tree.dot"
if not os.path.exists(filename):  # create graphviz file if absent
    export_graphviz(
        tree_clf,
        out_file=filename,  # save tree to .dot file
        feature_names=iris.feature_names[2:],
        class_names=iris.target_names,
        rounded=True,
        filled=True,
    )

# convert .dot file to .png with command
# <dot -Tpng models\iris_tree.dot -o models\iris_tree.png>
# if needed, install open-source graphviz package from https://www.graphviz.org/:
# -> to download stable 64-bit windows10 package go to
#    https://www2.graphviz.org/Packages/stable/windows/10/cmake/Release/x64/
# -> at install: add path for all users
# -> post-install: run <dot -c> from command line *as administrator* to install
#    plugins (for image formats)
"""
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
img = mpimg.imread("models/iris_tree.png")
ax[0].imshow(img)
ax[0].axis("off")
ax[0].set_title("Decision Tree")
img = mpimg.imread("decision_tree_boundaries.png")
ax[1].imshow(img)
ax[1].axis("off")
ax[1].set_title("Decision Boundaries")
plt.show()
"""
# class probabilities and prediction for petal length=5cm, width=1.5cm
print(tree_clf.predict_proba([[5, 1.5]]))
print(tree_clf.predict([[5, 1.5]]))  # predicts class with largest probability

###################################################
# Decision Tree Regressor
###################################################
#  first generate noisy quadratic data
X = np.linspace(start=0, stop=1, num=500)
y = (X - 0.5) ** 2 + np.random.randn(500) / 50.0

# train model
tree_reg = DecisionTreeRegressor(max_depth=2)
tree_reg.fit(X[..., None], y[..., None])

# visualize trained tree
filename = "models/reg_tree.dot"
if not os.path.exists(filename):
    export_graphviz(
        tree_reg,
        out_file=filename,
        feature_names=["X"],
        class_names=["y"],
        rounded=True,
        filled=True,
    )
"""
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
img = mpimg.imread("models/reg_tree.png")
ax[0].imshow(img)
ax[0].axis("off")
ax[0].set_title("Decision Tree")
img = mpimg.imread("decision_tree_regressor.png")
ax[1].imshow(img)
ax[1].axis("off")
ax[1].set_title("Decision Boundaries")
plt.show()
"""

##################################################################
# Exercise #1: Train & fine-tune a decision tree for moons dataset
##################################################################
X, y = make_moons(n_samples=10000, noise=0.4)
# plt.scatter(X[:, 0], X[:, 1], c=y, s=1)
# plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

# grid search (with cross validation) for hyperparameter 'max_leaf_nodes'
tree_clf = DecisionTreeClassifier()
param_grid = {"max_leaf_nodes": [3, 4, 5, 6, 7]}
grid_searcher = GridSearchCV(estimator=tree_clf, param_grid=param_grid, n_jobs=1)
grid_searcher.fit(X_train, y_train)
print(grid_searcher.best_score_)
print(grid_searcher.best_params_)  # best hyperparameter

# retrain using optimal hyperparameter
n = grid_searcher.best_params_.get("max_leaf_nodes")
tree_clf = DecisionTreeClassifier(max_leaf_nodes=n)
tree_clf.fit(X_train, y_train)
print(tree_clf.score(X_test, y_test))

##################################################################
# Exercise #2: Grow a forest by splitting moons dataset
##################################################################
# first generate 1000 subsets of the training set of size 100 each
rs = ShuffleSplit(n_splits=1000, train_size=100, test_size=0)

# next train one decision tree on each subset using best hyperparameter value,
# and evaluate all 1000 trees on the test set
# (accuracy should suffer because training set is much smaller)
decision_trees = list()
ds_test_scores = list()
# code below is buggy (run pdb)
for train_idxs, _ in rs.split(X_train, y_train):
    # get training subsets
    x_bs = X_train[train_idxs]
    y_bs = y_train[train_idxs]
    # train decision tree
    tree_clf = DecisionTreeClassifier(max_leaf_nodes=n)
    tree_clf.fit(x_bs, y_bs)
    decision_trees.append(tree_clf)
    # evaluate decision tree
    ds_test_scores.append(tree_clf.score(X_test, y_test))
    # delete model
    del tree_clf
