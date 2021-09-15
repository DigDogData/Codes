#!/usr/bin/env python3

# downloadXkcd.py - Downloads every single XKCD comics

import os
import bs4
import requests


def main():
    url = "https://xkcd.com"
    os.makedirs("xkcd", exist_ok=True)  # store comcs in ./xkcd
    downloadXkcd(url)


def downloadXkcd(url):
    # user specifies search terms using command-line arguments, which are
    # stored as a list of strings in sys.argv
    res = requests.get(url + "/search/?q=")
    try:
        res.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s" % (exc))

    # retrieve top search result links
    # soup = bs4.BeautifulSoup(res.text, "lxml")

    # open a browser tab for each result
    # use browser's developer tools to inspect link elements, and select
    # only relevant elements that contain string 'package-snippet'
    # (this code may need changing if pypi.org does any code update)
    # print(len(linkElems))
    # print(linkElems[0].get("href"))


if __name__ == "__main__":
    main()
