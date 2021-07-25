##############################################
# Nullspace example
# (from Gilbert Strang lecture #7)
##############################################

# sympy library includes nullspace() module
import sympy as sp

# create sympy matrix object
M = sp.Matrix([[1, 2, 2, 2], [2, 4, 6, 8], [3, 6, 8, 10]])
N = M.nullspace()  # nullspace
print(M)
print("")
print(N)

M = M.T
N = M.nullspace()
print("")
print("")
print(M)
print("")
print(N)
