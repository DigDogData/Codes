##############################################
# Reduced Row Echelon Form (RREF) example
# (from Gilbert Strang lecture #7)
##############################################

# sympy module includes rref() method
import sympy as sp

# create sympy matrix (all rows & columns independent)
M = sp.Matrix([[1, 2, 3], [4, 5, 5], [7, 8, 9], [1, 4, 7], [2, 5, 8]])
B = M.col_join(2 * M)  # join matrices M & 2*M vertically -> B = [[M],[2M]]
C1 = M.row_join(M)  # join M & M horizontally
C2 = M.row_join(sp.zeros(5, 3))  # join M & [0] horizontally
C = C1.col_join(C2)  # join [M M] & [M 0] vertically -> C = [[M M],[M 0]]
R1 = C.rref()
R2 = B.rref()
print(M)
print("")
print(B)
print("")
print(R2)
print("")
print(B)
print("")
print(R1)
print("")
print("")

D = C.T
R = D.rref()
print(D)
print("")
print(R)
