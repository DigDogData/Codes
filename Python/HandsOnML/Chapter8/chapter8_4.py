################################################################################
# LLR (Locally Linear Embedding): another nonlinear dimensionality reduction
# (NLDR) technique - a manifold learning technique that does not rely on
# projection, and instead finds low-dimenisonal representation of the training
# set that preserves local relationships (e.g distances) among data points
################################################################################
# load modules
import sklearn
from sklearn import datasets
from sklearn.manifold import LocallyLinearEmbedding

print("----------------------------------")
print("sklearn version:", sklearn.__version__)
print("----------------------------------")

# Swiss roll data
X, _ = datasets.make_swiss_roll(n_samples=1000, noise=1)

# LLE model
lle = LocallyLinearEmbedding(n_components=2, n_neighbors=10)
X_reduced = lle.fit_transform(X)
print(X.shape, X_reduced.shape)
