#!/usr/bin/env python3

# miscDebugCodes.py - Example Codes to debug codes

# raise excetion
tmp1 = 5
tmp2 = 1
if tmp1 != 1:
    raise Exception("tmp1 must equal 1.")  # rest of the code does not execute
if tmp2 == 1:
    raise Exception("tmp2 must not equal 1.")

# assertion
