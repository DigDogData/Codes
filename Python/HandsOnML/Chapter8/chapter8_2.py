############################################################
# PCA: Data compression and recovery
############################################################
# load modules
import numpy as np
import pandas as pd
import matplotlib
import sklearn
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA

print("----------------------------------")
print("numpy version:", np.__version__)
print("pandas version:", pd.__version__)
print("matplotlib version:", matplotlib.__version__)
print("sklearn version:", sklearn.__version__)
print("----------------------------------")

# MNIST data
X, y = datasets.fetch_openml(name="mnist_784", return_X_y=True)

# train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# model
d = 154
pca = PCA(n_components=d)
X_reduced = pca.fit_transform(X_train)
X_recovered = pca.inverse_transform(X_reduced)
print("data variance retained:", np.sum(pca.explained_variance_ratio_))

"""
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
img = mpimg.imread("index.png")
ax[0].imshow(img)
ax[0].axis("off")
ax[0].set_title("Original")
img = mpimg.imread("index2.png")
ax[1].imshow(img)
ax[1].axis("off")
ax[1].set_title("Recovered")
plt.show()
"""

# randomized PCA quickly computes d-dimensional approximation:
# (computational complexity O(m x d^2) + O(d^3) instead of O(m x n^2) + O(n^3)
# with original PCA)
rnd_pca = PCA(n_components=d, svd_solver="randomized")
X_reduced = rnd_pca.fit_transform(X_train)

# incremental PCA: uses 'partial_fit()' method with each mini-batches (rather than
# 'fit()' method with the whole training set)
n_batches = 100  # split training set into 100 mini-batches
inc_pca = IncrementalPCA(n_components=d)
for X_batch in np.array_split(X_train, n_batches):
    inc_pca.partial_fit(X_batch)
X_reduced = inc_pca.transform(X_train)

# alternatively, numpy's 'memmap' class allows using 'fit()' method with incremental
# PCA, by loading only the needed portion of data in memory
# (original large data needs to be stored on disk as a binary file)
"""
X_mm = np.memmap(filename, dtype='float32', mode='readonly', shape=(m, n))
batch_size = m // n_batches
inc_pca = IncrementalPCA(n_components=d, batch_size=batch_size)
inc_pca.fit(X_mm)
"""
