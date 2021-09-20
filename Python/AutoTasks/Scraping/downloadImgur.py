#!/usr/bin/env python3

# downloadImgur.py - Downloads preset number of Imgur images based on category
# USAGE: py downloadImgur.py <category> <limit>

import sys
import os
import bs4
import requests
import logging
from util import startBrowser
from util import raiseStatus


def main():
    url = "https://imgur.com"
    browser = startBrowser("firefox", headless=True)  # Brave is buggy
    os.makedirs("imgur", exist_ok=True)  # create ./imgur folder (to store images)
    downloadImgur(url, browser)
    browser.quit()


def downloadImgur(url, browser):

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # get category and limit from CLI
    if len(sys.argv) == 3:
        category = sys.argv[1]
        limit = sys.argv[2]
    else:
        sys.exit("USAGE: python downloadImgur.py <category> <limit>")

    # make request to category page
    category_url = url + "/search?q=" + category
    logging.info("Category Page URL: " + category_url)
    try:
        category_res = requests.get(category_url)
        raiseStatus(category_res)
    except Exception as err:
        logging.error(str(err))
        sys.exit(1)

    # find all image thumbnails for this category
    thumb_soup = bs4.BeautifulSoup(category_res.content, "lxml")
    image_count_elem = thumb_soup.select(".sorting-text-align > i")
    image_count = image_count_elem[0].getText()
    print("------------------------------------------")
    print("There are %s images about '%s'." % (image_count, category))
    print("Downloading first %s images..." % limit)
    print("------------------------------------------")
    image_list = thumb_soup.select(".post > .image-list-link")

    # loop through image thumbnails
    for i in range(int(limit)):
        thumbElem = image_list[i]
        page_url = url + thumbElem.get("href")
        logging.info("Image Page URL: " + page_url)

        # open image page in browser (because of scripting, page source
        # must be accessed from loaded page)
        browser.get(page_url)
        image_soup = bs4.BeautifulSoup(browser.page_source, "lxml")
        image_elem = image_soup.select(".image-placeholder")
        if len(image_elem) == 0:  # skip if not an image (e.g. video page)
            logging.warning("Page does not have image. Skipping...")
            continue
        image_url = image_elem[0].get("src")
        logging.info("Image URL: " + image_url)

        # download image
        try:
            image_res = requests.get(image_url)
            raiseStatus(image_res)
            image_name = os.path.basename(image_url)
            imageFile = open(os.path.join("imgur", image_name), "wb")
            for chunk in image_res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            logging.info("Image '" + image_name + "' saved.")
        except Exception as err:
            logging.error("Image Download Error: " + str(err))


if __name__ == "__main__":
    main()
