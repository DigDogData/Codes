#!/usr/bin/env python3

# miscFileReadWriteCodes.py - Example Codes for file read/write

from pathlib import Path
import shelve
import pprint

# open and read file
helloFile = open(Path.cwd() / "hello.txt")
# helloFile = open("home/roy/Documents/DS/Codes/Python/AutoTasks/hello.txt")
helloContent = helloFile.read()
print(helloContent)

# open and read multi-line file
sonnetFile = open("sonnet29.txt", "r")
print(sonnetFile.readlines())

# write to file
baconFile = open("bacon.txt", "w")
baconFile.write("Hello, world!\n")
baconFile.close()
baconFile = open("bacon.txt", "a")
baconFile.write("Bacon is not a vegetable.")
baconFile.close()
baconFile = open("bacon.txt", "r")
content = baconFile.read()
baconFile.close()
print(content)

# save/open python data in file
shelfFile = shelve.open("PyData/mydata")  # create (empty)/open (existing) file
cats = ["Zophie", "Pooka", "Simon"]
shelfFile["cats"] = cats  # save list
shelfFile.close()
shelfFile = shelve.open("PyData/mydata")
print(list(shelfFile.keys()))  # get keys
print(list(shelfFile.values()))  # get values
shelfFile.close()

# pretty format & printing (also gives syntactically corrct python code)
# create a list of dictionaries
cats = [{"name": "Zophie", "desc": "chubby"}, {"name": "Pooka", "desc": "fluffy"}]
fileObj = open("myCats.py", "w")
fileObj.write("cats = " + pprint.pformat(cats) + "\n")  # save list as python code
fileObj.close()

# import myCats.py
import myCats  # noqa: E402 (ignore flake8 error 'import not at the top')

print(myCats.cats)
print(myCats.cats[0])
print(myCats.cats[0]["name"])
