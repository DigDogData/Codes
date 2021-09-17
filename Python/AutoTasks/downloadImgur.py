#!/usr/bin/env python3

# downloadImgur.py - Downloads every single Imgur images based on tag/category

import sys
import os
import bs4
import requests

# import user-created library 'Libs'
sys.path.append("/home/roy/Documents/DS/Codes/Python/Libs")
from util import raiseStatus  # noqa E402


def main():
    os.makedirs("imgur", exist_ok=True)  # create ./imgur directory
    tag = "coronavirus"
    downloadImgur(tag)


def downloadImgur(tag):
    url = "https://imgur.com"

    # download main page
    print("Downloading page %s..." % url)
    res = requests.get(url)
    raiseStatus(res)

    # pass text attribute of response to BeautifulSoup()
    soup = bs4.BeautifulSoup(res.text, "lxml")

    # find all tags/categories
    tagElem = soup.select("a.Tag ")
    print(len(tagElem))


if __name__ == "__main__":
    main()
