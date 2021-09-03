#!/usr/bin/env python3

# miscRequestsCodes.py - Example codes using requests module

import requests

# download a web page
res = requests.get("https://automatetheboringstuff.com/files/rj.txt")
print(type(res))
print(res.status_code == requests.codes.ok)
print(len(res.text))
print(res.text[:250])
print("----------------------------")

# check for errors
# (always call raise_for_status() after calling requests.get(), to make sure download
# actually works)
res = requests.get("https://inventwithpython.com/page_that_does_not_exist.html")
try:
    res.raise_for_status()
except Exception as exc:
    print("There was a problem: %s" % (exc))
print("----------------------------")

# save downloaded content to a file
res = requests.get("https://automatetheboringstuff.com/files/rj.txt")
try:
    res.raise_for_status()
except Exception as exc:
    print("There was a problem: %s" % (exc))
playFile = open("RomeoAndJuliet.txt", "wb")
for chunk in res.iter_content(100000):
    playFile.write(chunk)
playFile.close()
