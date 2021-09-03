################################################################################
# AdaBoost - adaptive boosting with sequentially improved predictions
# (after training all predictors, ensemble makes precition like bagging/pasting)
################################################################################
# load modules
import sklearn
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("sklearn version:", sklearn.__version__)

# get data
X, y = datasets.make_moons(n_samples=10000, noise=0.5)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.33)
# print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)

# train AdaBoost (uses Decision Tree as base predictor)
ada_clf = AdaBoostClassifier(
    base_estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=200,
    algorithm="SAMME.R",
    learning_rate=0.5,
)
ada_clf.fit(X_train, y_train)

# evaluate model
y_pred_rf = ada_clf.predict(X_val)
print("AdaBoost accuracy:", accuracy_score(y_pred_rf, y_val))
