############################################################
# SVD (Singular Value Decomposition):
# Decomposes training set matrix X into dot product of three
# matrices: X = U . Sigma . V^T (V^T contains all PCs)
############################################################
# load modules
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
import sklearn
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

print("numpy version:", np.__version__)
print("pandas version:", pd.__version__)
print("matplotlib version:", matplotlib.__version__)
print("seaborn version:", sns.__version__)
print("sklearn version:", sklearn.__version__)

# get data
X = np.linspace(start=-1, stop=1, num=100)
y = X + np.random.normal(size=100) / 7.0
print(X.shape, y.shape)

plt.scatter(X, y, c="blue")
plt.xlabel("$X_1$")
plt.ylabel("$X_2$")
plt.grid()
plt.show()

# use numpy's svd() to get first two PCs of data
X = np.concatenate((X[..., None], y[..., None]), axis=1)
print(X.shape)
X_centered = X - X.mean(axis=0)  # PCA assumes data is centered around origin
U, s, V = np.linalg.svd(a=X_centered)
c1 = V.T[:, 0]
c2 = V.T[:, 1]
print(c1, c2)

# project to d(=2) dimensional hyperplane
W2 = V.T[:, :2]  # matrix W_d containing first d PCs
X2D = X_centered.dot(W2)  # X_proj = X . W_d

# use sklearn's PCA class implementation
pca = PCA(n_components=2)
X2D = pca.fit_transform(X)
assert np.all(np.abs(pca.components_) == np.abs(W2))
print(pca.explained_variance_ratio_)  # proportion of variance in first d PCs

# reduce X to preserve 95% of original variance
pca = PCA()  # first compute full PCA (without dimensionality reduction)
pca.fit(X)
cumsum = np.cumsum(pca.explained_variance_ratio_)
d = np.argmax(cumsum >= 0.95) + 1  # reduced dimension d
pca = PCA(n_components=d)  # recompute PCA with reduced dimensionality
X_reduced = pca.fit_transform(X)

# much shorter way to do the same
pca = PCA(n_components=0.95)  # possible to set float n_components (0,1)
X_reduced = pca.fit_transform(X)
