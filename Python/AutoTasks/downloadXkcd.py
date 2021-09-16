#!/usr/bin/env python3

# downloadXkcd.py - Downloads every single XKCD comics

import sys
import os
import bs4
import requests

# import user-created library 'Libs'
sys.path.append("/home/roy/Documents/DS/Codes/Python/Libs")
from util import raiseStatus  # noqa E402


def main():
    url = "https://xkcd.com"
    os.makedirs("xkcd", exist_ok=True)  # create ./xkcd directory to save comics images
    downloadXkcd(url)


def downloadXkcd(url0):
    url = url0
    while not url.endswith("#"):  # 1st page URL ends with '#'

        # download page
        print("Downloading page %s..." % url)
        res = requests.get(url)
        raiseStatus(res)

        # pass text attribute of response to BeautifulSoup()
        soup = bs4.BeautifulSoup(res.text, "lxml")

        # find URL of the comic image
        # (each comic image has <img> element inside <div> element with id
        # attribute set to 'comic', so the selector "#comic img" gets the
        # correct <img> element from BeautifulSoup object)
        comicElem = soup.select("#comic img")
        if comicElem == []:
            print("Could not find comic image.")  # skip pages without image
        else:
            comicUrl = "https:" + comicElem[0].get("src")  # image URL
            print("Downloading image %s..." % (comicUrl))
            res = requests.get(comicUrl)
            raiseStatus(res)

            # save image to ./xkcd
            # (iter_content() method returns 'chunks' of content on each iteration of
            # the loop, and the size of each chunk is specified to be 100000 bytes)
            imageFile = open(os.path.join("xkcd", os.path.basename(comicUrl)), "wb")
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

        # get Prev button's url
        prevLink = soup.select('a[rel="prev"]')[0]
        url = url0 + prevLink.get("href")

    print("Done.")


if __name__ == "__main__":
    main()
