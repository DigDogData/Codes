############################################################
# K-Means
############################################################
# load modules
import numpy as np
import pandas as pd
import matplotlib
import sklearn
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

print("----------------------------------")
print("numpy version:", np.__version__)
print("pandas version:", pd.__version__)
print("matplotlib version:", matplotlib.__version__)
print("sklearn version:", sklearn.__version__)
print("----------------------------------")

# get data
X, y = datasets.make_blobs(
    n_samples=1000, n_features=2, centers=5, cluster_std=[0.5, 0.5, 0.5, 1, 1]
)
# plot data
"""
plt.figure(figsize=(8, 8))
plt.scatter(X[:, 0], X[:, 1], s=2)
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()
"""

# train model with k clusters
k = 5
kmeans = KMeans(n_clusters=k)
y_pred = kmeans.fit_predict(X)
print(y_pred)
print(y_pred is kmeans.labels_)
print(kmeans.cluster_centers_)

# predict/assign new instances
X_new = np.array([[0, 2], [3, 2], [-3, 3], [-3, 2.5]])
print(kmeans.predict(X_new))

# plot decision boundaries (Voronoi tesselation)
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

"""
plt.figure(figsize=(8, 8))
plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X[:, 0], X[:, 1], c=y_pred, edgecolor="k")
plt.show()
"""

# hard clustering: assigning each instance to one cluster (as above)
# soft clustering: giving each instance a score (e.g. distance to centroid) per cluster
print(kmeans.transform(X_new))  # distance to centroid for each new instance

# centroid initialization method
good_init = np.array([[-3, 3], [-3, 2], [-3, 1], [-1, 2], [0, 2]])
kmeans = KMeans(n_clusters=k, init=good_init, n_init=1)
