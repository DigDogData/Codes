#!/usr/bin/env python3

# miscFilePathCodes.py - Example Codes to work with file/folder path variables

from pathlib import Path
import os

path1 = Path("spam", "bacon", "eggs")  # Path() returns path with correct separators
path2 = str(Path("spam", "bacon", "eggs"))
path3 = Path("spam") / "bacon" / "eggs"  # '/' operator joins path strings
print(path1)
print(path2)
print(path3)

myFiles = ["accounts.txt", "details.csv", "invite.docx"]
for filename in myFiles:
    print(Path(r"/home/roy/Documents", filename))

cwd = Path.cwd()  # returns current working directory
home = Path.home()  # returns home directory
os.chdir(home)  # change to home directory
print(Path.cwd())
os.chdir(cwd)  # change to current working directory
print(Path.cwd())

# working with list of folder content
dirlist = os.listdir(cwd)  # returns folder content as a list of strings
for filename in dirlist:
    print(
        filename, ": ", os.path.getsize(Path.cwd() / filename)
    )  # print filesize (in bytes) in cwd

# another way to work with list of folder content
p = Path.cwd()
# print(list(p.glob("*")))  # list all contents
# print(list(p.glob("*.txt")))  # list only text files
# print(list(p.glob("misc*")))  # list only files beginning with 'misc'

for filePathObj in p.glob("*.py"):  # glob() method creates a generator object
    print(filePathObj, os.path.getsize(filePathObj))

# path validation
newFolder = Path(Path.cwd() / "NewFolder")
if newFolder.exists():
    print("This is a valid path")
else:
    print(str(newFolder) + " does not exist")

newFile = Path(Path.cwd() / "ticTacToe.py")
print(newFile.is_file())  # is newFile a file?
print(newFile.is_dir())  # is newFile a directory?
