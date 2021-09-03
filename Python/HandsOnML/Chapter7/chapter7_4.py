#################################################################################
# Random Forest (ensemble of Decision Trees)
# (same as bagging/pasting with max_samples=training dataset size)
#################################################################################
# load modules
import sklearn
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("sklearn version:", sklearn.__version__)

# get data
X, y = datasets.make_moons(n_samples=10000, noise=0.5)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.33)
# print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)

# train model (500 trees, each limited to maximum 16 nodes)
rnd_clf = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)
rnd_clf.fit(X_train, y_train)

# evaluate model
y_pred_rf = rnd_clf.predict(X_val)
print("RF accuracy:", accuracy_score(y_val, y_pred_rf))

# bagging classifier below mimics RF above (see p.189)
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(splitter="random", max_leaf_nodes=16),
    n_estimators=500,
    max_samples=1.0,
    bootstrap=True,
    n_jobs=-1,
)
bag_clf.fit(X_train, y_train)
y_pred_bag = bag_clf.predict(X_val)
print("Bag accuracy:", accuracy_score(y_val, y_pred_bag))

##############################################################
# Feature importance
##############################################################
# in a single tree, important features appear closer to the root node,
# whereas unimportant features appear closer to the leaf node (or not at all)
# => this allows estimating feature importance in terms of average depth
# at which it a feature appears across all trees in a forest
# feature importance for iris dataset
iris = datasets.load_iris()
rnd_clf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
rnd_clf.fit(iris["data"], iris["target"])
for name, score in zip(iris["feature_names"], rnd_clf.feature_importances_):
    print(name, ":", score)

# plot pixel-wise Moon's feature importance
digits = datasets.load_digits()
rnd_clf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
rnd_clf.fit(digits["data"], digits["target"])
plt.imshow(rnd_clf.feature_importances_.reshape(8, 8), cmap="Blues")
plt.colorbar()
plt.show()
