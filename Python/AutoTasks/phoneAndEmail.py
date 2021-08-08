#!/usr/bin/env python3

# phoneAndEmail.py - Finds phone numbers and email addresses on the clipboard

import re  # import regex module

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing

phoneRegex = re.compile(
    r"""(
        (\d{3}|\(\d{3}\))?              # area code
        (\s|-|\.)?                      # separator
        (\d{3})                         # first 3 digits
        (\s|-|\.)                       # separator
        (\d{4})                         # last 4 digits
        (\s*(ext|x|ext.)\s*(\d{2,5}))?  # extension
        )""",
    re.VERBOSE,
)

# TODO: Create email regex.

# TODO: Find matches in clipboard text.

# TODO: Copy results to the clipboard.
