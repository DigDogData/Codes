#####################################################################
# Exercise #1: Compare runtime before and after PCA reduction
#####################################################################
# load MNIST dataset & split it into train/test sets
import numpy as np
import pandas as pd
import matplotlib
import timeit
import sklearn
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.manifold import TSNE
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

print("----------------------------------")
print("numpy version:", np.__version__)
print("pandas version:", pd.__version__)
print("matplotlib version:", matplotlib.__version__)
print("sklearn version:", sklearn.__version__)
print("----------------------------------")

X, y = datasets.fetch_openml(name="mnist_784", return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=10000)
# print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# train a random forest classifier on the dataset and time how long it takes
forest = RandomForestClassifier(n_estimators=100)


def fun1():
    forest.fit(X_train, y_train)


print(f"Time taken before PCA: {round(timeit.timeit(fun1, number=1), 2):0.2f}s")

# evaluate model on test set
print(f"Accuracy before PCA: {accuracy_score(y_test, forest.predict(X_test))}")

# next use PCA to reduce dataset's dimensionality while retaining 95% variance
pca = PCA(n_components=0.95)
pca.fit(X_train)
X_train_ = pca.transform(X_train)
X_test_ = pca.transform(X_test)

# train a random forest classifier on the reduced dataset and time it again
forest = RandomForestClassifier(n_estimators=100)


def fun2():
    forest.fit(X_train_, y_train)


print(f"Time taken after PCA: {round(timeit.timeit(fun2, number=1), 2):0.2f}s")

# evaluate model on test set
print(f"Accuracy after PCA: {accuracy_score(y_test, forest.predict(X_test_))}")

#####################################################################
# Exercise #2: t-SNE (t-Distributed Stochastic Neighbor Embedding):
# dimensionality reduction while keeping similar instances close and
# dissimilar instances apart
#####################################################################
# reduce MNIST dataset down to 2D and visualize result using matplotlib
tsne = TSNE()
X_train_ = tsne.fit_transform(X_train[:1000])

"""
plt.figure(figsize=(9, 9))
plt.scatter(X_train_[:, 0], X_train_[:, 1], c=y_train[:1000].astype(int), cmap="Greys")
plt.axis("off")
plt.show()

# replace each dot with its instance class (from 0 to 9)
plt.figure(figsize=(9, 9))
labels = y_train[:1000].astype(int)
for idx in range(len(X_train_)):
    plt.scatter(
        X_train_[idx, 0],
        X_train_[idx, 1],
        marker=f"$ {labels[idx]} $",
        c="black",
        edgecolors="none",
    )
plt.axis("off")
plt.show()

# plot scaled-down versions of digit images themselves
fig, ax = plt.subplots(figsize=(9, 9))
ax.scatter(X_train_[:, 0], X_train_[:, 1])
for idx in range(len(X_train_)):
    ab = AnnotationBbox(
        OffsetImage(X_train[idx].reshape(28, 28), zoom=0.4),
        (X_train_[idx, 0], X_train_[idx, 1]),
        frameon=False,
    )
    ax.add_artist(ab)
plt.axis("off")
plt.show()
"""

###########################################################################
# Exercise #3: Try other dimensionality reduction algorithm (PCA, LLE, MDS)
# and compare resulting visualizations
###########################################################################
# KernelPCA
pca = KernelPCA(n_components=2)
X2_train_ = pca.fit_transform(X_train[:1000])

# LLE
lle = LocallyLinearEmbedding(n_components=2, n_neighbors=10)
X3_train_ = lle.fit_transform(X_train[:1000])

# side-by-side visualization plots (t-SNE, KernelPCA, LLE)
# (t-SNE generates best interpretable visualizations)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
ax[0].scatter(X_train_[:, 0], X_train_[:, 1])
for idx in range(len(X_train_)):
    ab = AnnotationBbox(
        OffsetImage(X_train[idx].reshape(28, 28), zoom=0.4),
        (X_train_[idx, 0], X_train_[idx, 1]),
        frameon=False,
    )
    ax[0].add_artist(ab)
ax[0].axis("off")
ax[0].set_title("t-SNE")

ax[1].scatter(X2_train_[:, 0], X2_train_[:, 1])
for idx in range(len(X2_train_)):
    ab = AnnotationBbox(
        OffsetImage(X_train[idx].reshape(28, 28), zoom=0.4),
        (X2_train_[idx, 0], X2_train_[idx, 1]),
        frameon=False,
    )
    ax[1].add_artist(ab)
ax[1].axis("off")
ax[1].set_title("KernelPCA")

ax[2].scatter(X3_train_[:, 0], X3_train_[:, 1])
for idx in range(len(X3_train_)):
    ab = AnnotationBbox(
        OffsetImage(X_train[idx].reshape(28, 28), zoom=0.4),
        (X3_train_[idx, 0], X3_train_[idx, 1]),
        frameon=False,
    )
    ax[2].add_artist(ab)
ax[2].axis("off")
ax[2].set_title("LLE")
plt.show()
