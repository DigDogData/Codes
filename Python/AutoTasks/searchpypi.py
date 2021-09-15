#!/usr/bin/env python3

# searchpypi.py - Opens several search results
# Usage: python searchpypi.py <search string>

import sys
import bs4
import requests
import webbrowser


def main():
    url = "https://pypi.org"
    tabNum = 5  # number of tabs to open
    print("Searching...")  # display text while downloading search result page
    searchpypi(url, tabNum)


def searchpypi(url, num):
    # user specifies search terms using command-line arguments, which are
    # stored as a list of strings in sys.argv
    res = requests.get(url + "/search/?q=" + " ".join(sys.argv[1:]))
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
    # print(len(linkElems))
    # print(linkElems[0].get("href"))
    numOpen = min(num, len(linkElems))  # open at least 'num' number of tabs
    for i in range(numOpen):
        urlToOpen = url + linkElems[i].get("href")
        print("Opening", urlToOpen)
        webbrowser.open(urlToOpen)  # ignore console error messages (debian bug)


if __name__ == "__main__":
    main()
