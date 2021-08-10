#!/usr/bin/env python3

# dateDetection.py - Cleans up dates in different formats

import re  # import regex module

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing

# TODO: Clean up dates in different date formats (e.g. 3/14/2019, 03-14-2019,
#       2019/3/14, 14/3/2019, 2019-14-03, 3-14-19; see p.186)
