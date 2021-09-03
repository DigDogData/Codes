#################################################################################
# 'bagging' (training with replacement) and 'pasting' (training # w/o replacement)
# same classifier but trained with different (bagging) or same (pasting) sets
# (automatically runs soft voting if predict_proba() method is available)
#################################################################################
# load modules
import sklearn
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn import datasets
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("sklearn version:", sklearn.__version__)

# get data
X, y = datasets.make_moons(n_samples=10000, noise=0.5)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.33)
print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)

# train model
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(),
    n_estimators=500,
    max_samples=100,  # training subset size
    bootstrap=True,  # bagging ('b'ootstrap 'ag'gregating)
    n_jobs=-1,  # train classifiers in parallel
)
bag_clf.fit(X_train, y_train)

# evaluate models
y_hat = bag_clf.predict(X_val)
print("accuracy:", accuracy_score(y_val, y_hat))

# image shows comparison of decision boundaries between one tree and a bagging
# ensemble of 500 trees, both trained on moons dataset: ensemble's predictions
# will generalize better than the single tree; ensemble has a comparable bias
# but smaller variance (makes roughly same number of errors on training set,
# but decision boundary is less irregular)
img = mpimg.imread("dt_bagging.png")
plt.figure(figsize=(14, 6))
plt.imshow(img)
plt.axis("off")
plt.show()

# train & evaluate model with oob (out-of-bag) instances
# (oob refers to training instances not seen by models)
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(),
    n_estimators=500,
    max_samples=0.63,  # 1 - exp(-1) = 0.63
    bootstrap=True,
    n_jobs=-1,
    oob_score=True,
)
bag_clf.fit(X_train, y_train)
print("oob score:", bag_clf.oob_score_)

# evaluate with accuracy score (these two scores should be close)
y_hat = bag_clf.predict(X_val)
print("accuracy:", accuracy_score(y_val, y_hat))

# oob decision function (see p.187 of the book)
print(bag_clf.oob_decision_function_)
