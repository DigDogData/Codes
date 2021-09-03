#########################################################################
# Gradient Boosting (instead of tweaking instance weights as in AdaBoost,
# next predictor tries to fit residual errors of the previous predictor)
#########################################################################
# load modules
import numpy as np
import matplotlib
import sklearn
import xgboost  # available only with python <=3.7 (use 'da37' env)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

print("numpy version:", np.__version__)
print("matplotlib version:", matplotlib.__version__)
print("sklearn version:", sklearn.__version__)
print("xgboost version:", xgboost.__version__)

# get training data (noisy quadratic)
X = np.linspace(start=0, stop=1, num=500)
y = (X - 0.5) ** 2 + np.random.randn(500) / 50.0
X = X[..., None]  # 1 feature

# train 1st regression model (uses Decision Tree as base predictor)
tree_reg1 = DecisionTreeRegressor(max_depth=2)
tree_reg1.fit(X, y)

# train 2nd regressor with residual errors of 1st regressor
y2 = y - tree_reg1.predict(X)
tree_reg2 = DecisionTreeRegressor(max_depth=2)
tree_reg2.fit(X, y2)

# train 3rd regressor with residual errors of 2nd regressor
y3 = y2 - tree_reg2.predict(X)
tree_reg3 = DecisionTreeRegressor(max_depth=2)
tree_reg3.fit(X, y3)

# make ensemble prediction by adding up predictions of all trees
y_pred = sum(tree.predict(X) for tree in (tree_reg1, tree_reg2, tree_reg3))

# visualize
# plt.scatter(X.squeeze(), y.squeeze(), s=1)
# plt.scatter(X.squeeze(), y_pred.squeeze(), s=1, c="red")
img = mpimg.imread("boosting_ensembles.png")
plt.figure(figsize=(10, 10))
plt.imshow(img)
plt.axis("off")
plt.tight_layout()
plt.show()

# a simpler way: using sklearn's GradientBoostingRegressor() class
# (learning rate hyperparameter scales the contribution of each tree:
# low value such as 0.1 means more trees needed to fit the training set)
gbrt = GradientBoostingRegressor(max_depth=2, n_estimators=3, learning_rate=1.0)
gbrt.fit(X, y)

# too few estimators on the left (underfitting), too many on the right (overfitting)
img = mpimg.imread("ensemble_overunderfit.png")
plt.figure(figsize=(12, 6))
plt.imshow(img)
plt.axis("off")
plt.tight_layout()
plt.show()

# one way out is by implementing early stopping with staged_predict() method
# first train a GBRT (Gradient Boosting Regression Tree) ensemble with 120 trees
X_train, X_val, y_train, y_val = train_test_split(X, y)
gbrt = GradientBoostingRegressor(max_depth=2, n_estimators=120)
gbrt.fit(X_train, y_train)

# next compute validation errors at each stage to find optimal number of trees
errors = [mean_squared_error(y_val, y_pred) for y_pred in gbrt.staged_predict(X_val)]
bst_n_estimators = np.argmin(errors) + 1
print("bst_n_estimators:", bst_n_estimators)

# finally train another GBRT ensemble using optimal number of trees
gbrt_best = GradientBoostingRegressor(max_depth=2, n_estimators=bst_n_estimators)
gbrt_best.fit(X_train, y_train)

# validation error on the left, best model's prediction on the right
img = mpimg.imread("gradient_boosting_optimization.png")
plt.figure(figsize=(12, 6))
plt.imshow(img)
plt.axis("off")
plt.tight_layout()
plt.show()

# possible to stop eartly, instead of training large number of estimators first
# and then looking back to find optimal number
# set 'warm_start=True' to allow incremental training
gbrt = GradientBoostingRegressor(max_depth=2, warm_start=True)

# stop training when validation error does not improve for five iterations in a row
min_val_error = float("inf")
error_going_up = 0
for n_estimators in range(1, 120):
    gbrt.n_estimators = n_estimators
    gbrt.fit(X_train, y_train)
    y_pred = gbrt.predict(X_val)
    val_error = mean_squared_error(y_val, y_pred)
    if val_error < min_val_error:
        min_val_error = val_error
        error_going_up = 0
    else:
        error_going_up += 1
        if error_going_up == 5:
            break  # early stopping

# Stochastic Gradient Boosting - using 'subsample' hyperparameter with
# GradientBoostingRegressor: subsample=0.25 means each tree is trained on 25%
# of training instances, selected randomly - trades higher bias for lower variance,
# speeds up training considerably

# XGBoost: popular python library for optimized implementation of gradient Boosting
xgb_reg = xgboost.XGBRegressor()

# early stopping (stop if valiadation error does not improve after 2 rounds)
print(xgb_reg.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=2))

# evaluation
y_pred = xgb_reg.predict(X_val)
print("mean_squared_error:", mean_squared_error(y_val, y_pred))

# visualize
plt.scatter(X_val.squeeze(), y_val.squeeze(), s=1)
plt.scatter(X_val.squeeze(), y_pred.squeeze(), s=1, c="red")
plt.show()
