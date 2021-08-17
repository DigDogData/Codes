#!/usr/bin/env python3

# backupToZip.py - Backs up an working folder into a zipped archive

import os
import zipfile  # module to zip/unzip files
from pathlib import Path


def backupToZip(folder):
    folder = os.path.abspath(folder)  # make sure folder is absolute

    # figure out the filename this code should use


p = Path.cwd()
