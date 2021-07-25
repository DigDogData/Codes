##############################################
# Reduced Row Echelon Form (RREF) example
# (from Gilbert Strang lecture #7)
##############################################

# sympy module includes rref() method
import sympy as sp

# create sympy matrix object
# M = sp.Matrix([[1, 2, 2, 2], [2, 4, 6, 8], [3, 6, 8, 10]])
M = sp.Matrix([[1, 2, 3, 1], [1, 1, 2, 1], [1, 2, 3, 1]])
R = M.rref()  # reduced row echelon form
print(M)
print("")
print(R)
print("")
print("")

M = M.T
R = M.rref()
print(M)
print("")
print(R)
