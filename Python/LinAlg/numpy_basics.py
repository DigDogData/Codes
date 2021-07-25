import numpy as np
import matplotlib.pyplot as plt

# vector-scalar multiplication
# vec2d = np.array([1, 2])
# s1 = 2
# s2 = 0.5
# s3 = -1
# x coordinates=[0,vec2d[0]], y coordinates=[0,vec2d[1]]
# plt.plot([0, vec2d[0]], [0, vec2d[1]], "bs-", label="v")
# plt.plot([0, s1 * vec2d[0]], [0, s1 * vec2d[1]], "ro-", label="s1*v")
# plt.plot([0, s2 * vec2d[0]], [0, s2 * vec2d[1]], "kp-", label="s2*v")
# plt.plot([0, s3 * vec2d[0]], [0, s3 * vec2d[1]], "g*-", label="s3*v")
# plt.legend()
# plt.show()

# vecor dot.product (v1 & v2 are orthogonal => v1.v2 = 0)
# v1 = np.array([1, 2])
# v2 = np.array([-2, 1])
# v3 = np.array([1, 3])
# print(np.dot(v1, v2))
# print(np.dot(v1, v3))
# print(np.dot(v2, v3))
# plt.plot([0, v1[0]], [0, v1[1]], "bs-", label="v1")
# plt.plot([0, v2[0]], [0, v2[1]], "ro-", label="v2")
# plt.plot([0, v3[0]], [0, v3[1]], "g*-", label="v3")
# plt.axis("square")
# plt.legend()
# plt.show()

# vector transposition
# python does not internally code vector orientation, that is, it does not
# see np.array() as a row or column vector, just a vector; for transposition
# to work, we must specify dimension, so that a row vector becomes a column
# vector and vice versa
# v1 = np.array([2, 3, -1], ndmin=2)
# print(v1)
# print(v1.T)

# special matrices
# M1 = np.eye(3)  # 3x3 identity matrix (always square)
# print(M1)
# M2 = np.zeros((3, 4))  # 3x4 zeros matrix (size in tuple argument)
# print(M2)
# M3 = np.ones((3, 4))  # 3x4 ones matrix (size in tuple argument)
# print(M3)
# M4 = np.full((5, 3), 8)  # 5x3 full (no zeros) 'constant' matrix with element 8
# print(M4)
# v = np.array([1, 2, 3, 4])
# M = np.diag(v)  # 4x4 diagonal matrix
# Minv = np.linalg.inv(M)
# print(M)

# regular matrix
# M1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print(M1)
# M = np.random.randint(0, 10, size=(4, 5))     # random integer matrix
# print(M)
# plt.imshow(M)
# plt.show()
# M = np.random.randn(3, 4)      # random unit normal matrix
# print(M)
# plt.imshow(M)
# plt.show()

# matrix transposition
# M = np.round(10 * np.random.randn(3, 4))
# print(M)
# print("")
# print(M.T)
# print("")
# print(M.T.T)

# matrix inner (dot) product (not pointwise multiplication)
# M1 = np.random.randn(4, 5)
# M2 = np.random.randn(4, 5)
# print(M1 @ M2.T)
# print("")
# print(np.matmul(M1, M2.T))

# matrix outer (kronecker) product
# (m,n) x (p,q) => (m*p,n*q)
# M1 = np.random.randint(0, 10, size=(2, 3))
# M2 = np.random.randint(0, 10, size=(3, 4))
# print(M1)
# print("")
# print(M2)
# print("")
# print(np.kron(M1, M2))

######################
# matrix inversion
######################
# For invertible (non-singular) matrices
# A = np.random.randn(4, 4)
# Ainv = np.linalg.inv(A)
# print(A)
# print("")
# print(Ainv)
# print("")
# print(A @ Ainv)
# fig, ax = plt.subplots(1, 3, figsize=(7, 4))
# ax[0].imshow(A)
# ax[0].set_title("A")
# ax[1].imshow(Ainv)
# ax[1].set_title("A$^{-1}$")
# ax[2].imshow(A @ Ainv)
# ax[2].set_title("AxA$^{-1}$")
# plt.show()

# For singular (non-invertible) matrices
# A = np.array([[1, 2], [2, 4]])
# Ainv = np.linalg.pinv(A)  # pseudo-inverse
# print(A)
# print("")
# print(Ainv)
# print("")
# print(A @ Ainv)

# matrix power
# A = np.random.randint(0, 10, size=(4, 4))
# Ap = np.linalg.matrix_power(A, 2)
# Ap2 = np.matmul(A, A)
# print(A)
# print("")
# print(Ap)
# print("")
# print(Ap2)

# matrix norms
# L2 (Frobenius) norm
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# L2 = np.linalg.norm(M)
# print(L2)

# condition number
# (measures sensitivity to input change, or how close it is to singularity)
# (smaller the value, closer it is)
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# C = np.linalg.cond(M)
# print(C)

# matrix determinant
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# d = np.linalg.det(M)
# print(d)

# matrix rank
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# r = np.linalg.matrix_rank(M)
# print(r)

# matrix trace 9sum of diagonal elements)
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# t = np.trace(M)
# print(t)

###########################
# matrix decomposition
###########################
# Cholesky decomposition: M = L*L^H
# (L->lower triangular matrix, ^H->conjugate transpose)
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# L = np.linalg.cholesky(M)
# M2 = np.matmul(L, L.T.conj())  # approximate reconstruction
# print(M)
# print("")
# print(L)
# print("")
# print(M2)
# print("")
# M = np.array([[1, -2j], [2j, 5]])
# L = np.linalg.cholesky(M)
# M2 = np.matmul(L, L.T.conj())  # exact reconstruction
# print(M)
# print("")
# print(L)
# print("")
# print(M2)

# QR decomposition: M = Q*R
# (Q->orthogonal matrix, R->upper triangular matrix)
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# QR = np.linalg.qr(M)
# Q = QR[0]
# R = QR[1]
# M2 = np.matmul(Q, R)
# print(M)
# print("")
# print(Q)
# print("")
# print(R)
# print("")
# print(M2)

# Eigenvalue decomposition: M = P*D*P^-1
# (P -> eigenvectors, D -> diagonal matrix of eigenvalues)
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# (d, P) = np.linalg.eig(M)
# d = np.linalg.eigvals(M)    # extract eigenvalues only
# D = np.diag(d)  # construct diagonal matrix from diagonal elements
# M2 = np.matmul(np.matmul(P, D), np.linalg.inv(P))
# M2 = np.real(M2)  # for visualization (imaginary parts are all zeros)
# print(M)
# print("")
# print(D)
# print("")
# print(P)
# print("")
# print(M2)

# Singular Value decomposition: M = U*S*V^T
# (U->left singular matrix, V->right singular matrix, S->diagonal matrix)
# M = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
# (U, s, V) = np.linalg.svd(M)
# S = np.diag(s)
# print(M)
# print("")
# print(U)
# print("")
# print(S)
# print("")
# print(V)

#######################################
# solving equations Ax = b (x = A^-1*b)
#######################################
# for invertible matrix A (see above on how to invert singular matrices)
A = np.array([[1, 5, 6], [1, 8, 9], [0, -1, 6]])
b = np.random.random((3, 1))  # 1d column vector
x1 = np.matmul(np.linalg.inv(A), b)
x2 = np.linalg.solve(A, b)
print(x1)
print("")
print(x2)
