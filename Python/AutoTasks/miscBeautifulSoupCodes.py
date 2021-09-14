#!/usr/bin/env python3

# miscBeautifulSoupCodes.py - Example codes using BeautifulSoup module
import bs4
import requests

# download webpage and pass text attrib of response to bs4.BeautifulSoup()
# (install lxml using <pipenv install lxml> to use faster lxml parser, compared to
# python's own html.parser)
res = requests.get("https://nostarch.com")
try:
    res.raise_for_status()
except Exception as exc:
    print("There was a problem: %s" % (exc))
noStarchSoup = bs4.BeautifulSoup(res.text, "lxml")
# noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
print(type(noStarchSoup))

# read html file and parse using bs4.BeautifulSoup()
exampleFile = open("example.html")
exampleSoup = bs4.BeautifulSoup(exampleFile, "lxml")
# exampleSoup = bs4.BeautifulSoup(exampleFile, "html.parser")
print(type(exampleSoup))
elems = exampleSoup.select("#author")  # select list of tags with id="author"
print(type(elems))
print(len(elems))
print(type(elems[0]))
print(str(elems[0]))
print(elems[0].getText())  # get text string of this element
print(elems[0].attrs)

pElems = exampleSoup.select("p")  # select list of all <p> elements
print(len(pElems))
print(str(pElems[0]))
print(pElems[0].getText())
print(pElems[1].getText())
print(pElems[2].getText())
