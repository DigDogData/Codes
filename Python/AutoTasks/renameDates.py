#!/usr/bin/env python3

# renameDates.py - Renames filenames with American MM-DD-YYYY date format to
# European DD-MM-YYYY format

import os
import shutil  # import file manipulation module
import re  # import regex module

# create oversimplified regex that matches files with American date format
# (can accept invalid dates like 4-31-2004, 2-29-2014, 0-15-2004 etc)
dateRegex = re.compile(
    r"""^(.*?)              # all text before the date
        ((0|1)?\d)-         # 1 or 2 digits for month (starts with 0/1)
        ((0|1|2|3)?\d)-     # 1 or 2 digits for day (starts with 0/1/2/3)
        ((18|19|20)\d\d)    # 4 digits for year (starts with 18/19/20)
        (.*?)$              # all text after the date
        """,
    re.VERBOSE,
)

# loop over files in the current working directory
for USFilename in os.listdir("."):
    mo = dateRegex.search(USFilename)

    # skip files without a date
    if mo is None:
        continue  # move to next filename

    # get different parts of the filename
    beforePart = mo.group(1)  # group '^(1)'
    monthPart = mo.group(2)  # group '(2 (3) )-'
    dayPart = mo.group(4)  # group '(4 (5) )-'
    yearPart = mo.group(6)  # group '(6 (7) )'
    afterPart = mo.group(8)  # group '(8)$'

    # form the European-style filename
    EUFilename = beforePart + dayPart + "-" + monthPart + "-" + yearPart + afterPart

    # get the full, absolute file paths
    absWorkingDir = os.path.abspath(".")
    USFilename = os.path.join(absWorkingDir, USFilename)
    EUFilename = os.path.join(absWorkingDir, EUFilename)

    # rename files
    print(f'Renaming "{USFilename}" to "{EUFilename}"...')
    # shutil.move(USFilename, EUFilename)
