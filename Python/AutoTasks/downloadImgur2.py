#!/usr/bin/env python3

# downloadImgur2.py - Downloads 'all' Imgur images based on category
# (page dynamically scrolled to expose more of category thumbnails)
# USAGE: py downloadImgur2.py <category>

import sys
import time
import os
import bs4
import requests
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

    # get category from CLI
    if len(sys.argv) == 2:
        category = sys.argv[1]
    else:
        sys.exit("USAGE: python downloadImgur2.py <category>")

    # open category page in browser
    category_url = url + "/search?q=" + category
    browser.get(category_url)
    htmlElem = browser.find_element(By.TAG_NAME, "html")
    # scroll down 2 times to expose more of category page
    for __ in range(2):
        htmlElem.send_keys(Keys.END)  # scroll to bottom
        time.sleep(2)

    # parse page with bs4
    thumb_soup = bs4.BeautifulSoup(browser.page_source, "lxml")
    image_count_elem = thumb_soup.select(".sorting-text-align > i")
    image_count = image_count_elem[0].getText()
    image_list = thumb_soup.select(".post > .image-list-link")
    limit = len(image_list)
    print("------------------------------------------")
    print("There are %s images about '%s'." % (image_count, category))
    print("Downloading first %s images..." % limit)
    print("------------------------------------------")

    # loop through image thumbnails
    for i in range(limit):
        thumbElem = image_list[i]
        page_url = url + thumbElem.get("href")

        # open image page in browser (because of scripting, page source
        # must be accessed from loaded page)
        browser.get(page_url)
        image_soup = bs4.BeautifulSoup(browser.page_source, "lxml")
        image_elem = image_soup.select(".image-placeholder")
        if len(image_elem) == 0:  # skip if not an image (e.g. video page)
            logging.warning("Page does not have image. Skipping...")
            continue
        image_url = image_elem[0].get("src")

        # download image
        try:
            image_res = requests.get(image_url)
            raiseStatus(image_res)
            image_name = os.path.basename(image_url)
            imageFile = open(os.path.join("imgur", image_name), "wb")
            for chunk in image_res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            logging.info("Image(#%s) '%s' saved.", i + 1, image_name)
        except Exception as err:
            logging.error("Image Download Error: " + str(err))


if __name__ == "__main__":
    main()
