#!/usr/bin/env python3

# searchpypi.py - Opens several search results
import sys
import bs4
import requests
import webbrowser

print("Searching...")  # display text while downloading search result page
# user specifies search terms using command-line arguments, which are
# stored as a list of strings in sys.argv
res = requests.get("https://pypi.org/search/?q=" + " ".join(sys.argv[1:]))
try:
    res.raise_for_status()
except Exception as exc:
    print("There was a problem: %s" % (exc))

# retrieve top search result links
soup = bs4.BeautifulSoup(res.text, "lxml")

# open a browser tab for each result
# use browser's developer tools to inspect link elements, and select
# only relevant elements that contain string 'package-snippet'
linkElems = soup.select(".package-snippet")
numOpen = min(5, len(linkElems))  # open at least 5 tabs
for i in range(numOpen):
    urlToOpen = "https://pypi.org" + linkElems[i].get("href")
    print("Opening", urlToOpen)
    webbrowser.open(urlToOpen)
