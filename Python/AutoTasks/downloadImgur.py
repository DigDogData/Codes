#!/usr/bin/env python3

# downloadImgur.py - Downloads every single Imgur images based on tag/category
# Usage: py downloadImgur.py <category> <limit>

import sys
import os
import bs4
import requests
import logging

# import user-created library 'Libs'
sys.path.append("/home/roy/Documents/DS/Codes/Python/Libs")
from util import raiseStatus  # noqa E402


def main():
    os.makedirs("imgur", exist_ok=True)  # create ./imgur directory
    downloadImgur()


def downloadImgur():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.disable(logging.CRITICAL)  # comment to enable all logging

    if len(sys.argv) == 3:
        logging.info("Command line arguments = 3")
        category = sys.argv[1]
        limit = sys.argv[2]

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
