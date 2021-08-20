#!/usr/bin/env python3

# miscDebugCodes.py - Example Codes to debug codes

# raise exception (can use inside try-except block)
# tmp1 = 5
# tmp2 = 1
# if tmp1 != 1:
#    raise Exception("tmp1 must equal 1.")  # rest of the code does not execute
# if tmp2 == 1:
#    raise Exception("tmp2 must not equal 1.")

# assertion (sanity check) (do not use inside try-except block)
# asssertion is programmer error (not user error), to be used only when
# program is under development, and  must be allowed to fail if incorrect
# user should never see it - using inside try-except block allows user to
# turn it off
ages = [26, 57, 92, 54, 22, 15, 17, 80, 47, 73]
ages.sort()
assert ages[0] <= ages[-1]  # assert 1st age <= last age (does nothing)
ages.reverse()
assert ages[0] <= ages[-1]  # assert 1st age <= last age (crashes)
