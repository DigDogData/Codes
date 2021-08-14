#!/usr/bin/env python3

# miscBulkFileManagement.py - Example Codes for bulk file/folder management

import os
import shutil  # module to copy/move/delete/rename files
from pathlib import Path

p = Path.cwd()

### copy ###
shutil.copy(p / "hello.txt", p / "hello2.txt")  # copy file
shutil.copy(p / "hello.txt", p / "test")  # copy file to folder
# copy entire folder (overwrite if destination folder exists)
shutil.copytree(p / "QuizFiles", p / "QuizFiles_backup", dirs_exist_ok=True)

### remove ###
if Path(p / "test/hello2.txt").exists():
    os.unlink(p / "test/hello2.txt")  # remove file
# remove selected files
for filename in Path(p / "QuizFiles_backup").glob("*answer*"):
    os.unlink(filename)
shutil.rmtree(p / "QuizFiles_backup")  # remove entire folder

### move ###
shutil.move(p / "hello2.txt", p / "test")  # move file (if does not exist)
# shutil.move(p / "hello2.txt", p / "test/hello2.txt")  # overwrite if exists

### walk directory tree ###
p2 = Path.home() / "Downloads"
for folderName, subfolders, filenames in os.walk(p2):
    print("The current folder is " + folderName)
    for subfolder in subfolders:
        print("Subfolder of " + folderName + ": " + subfolder)
    for filename in filenames:
        print("File inside " + folderName + ": " + filename)
    print("")
