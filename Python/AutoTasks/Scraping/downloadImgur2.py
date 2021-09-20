#!/usr/bin/env python3

# downloadImgur.py - Download Imgur images by keyword
# USAGE: py downloadImgur.py <keyword> <limit>

import sys
import time
import os
import bs4
import requests
import logging
from selenium.webdriver.common.by import By
from util import startBrowser


# function to auto-scroll 'num' times to expose more of page
def scrollToEnd(browser, num):
    for __ in range(num):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # pause between interactions


# function to download and save image (uses requests)
def downloadImage(i, image_url, folderName, logging):
    try:
        image_res = requests.get(image_url, timeout=10)
        try:
            image_res.raise_for_status()
            image_name = os.path.basename(image_url)
            imageFile = open(os.path.join(folderName, image_name), "wb")
            for chunk in image_res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            logging.info("Image(#%s) '%s' saved.", i + 1, image_name)
        except Exception as err:  # if there is connection error
            logging.error("Connection Error: " + str(err))
            pass
    except Exception as err:  # if there is other error (e.g. timeout)
        logging.error("Image Download Error: " + str(err))
        pass


# function to search Imgur
def searchImgur(keyword, limit, url, folderName, browser):

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # open keyword page in browser
    keyword_url = url + "/search?q=" + keyword
    browser.get(keyword_url)

    scrollToEnd(browser, 1)  # auto-scroll page few times

    # find images to be scraped from page
    imgList = browser.find_elements(By.XPATH, '//a[contains(@class,"image-list-link")]')
    imgCountElem = browser.find_elements(
        By.XPATH, '//span[contains(@class,"sorting-text-align")]//i'
    )
    imgCount = imgCountElem[0].get_attribute("innerHTML")
    print("------------------------------------------")
    print("There are %s images about '%s'." % (imgCount, keyword))
    print("Downloading first %s images..." % limit)
    print("------------------------------------------")

    # loop through image thumbnails
    for i in range(int(limit)):
        thumbElem = imgList[i]
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
            # raiseStatus(image_res)
            image_name = os.path.basename(image_url)
            imageFile = open(os.path.join("imgur", image_name), "wb")
            for chunk in image_res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            logging.info("Image(#%s) '%s' saved.", i + 1, image_name)
        except Exception as err:
            logging.error("Image Download Error: " + str(err))


def main():
    # get keyword from CLI
    if len(sys.argv) == 3:
        keyword = sys.argv[1]
        limit = sys.argv[2]
    else:
        sys.exit("USAGE: python downloadImgur.py <category> <limit>")

    url = "https://imgur.com"
    folderName = "imgur"  # create ./imgur folder to store images
    os.makedirs(folderName, exist_ok=True)
    browser = startBrowser("brave", headless=False)
    searchImgur(keyword, limit, url, folderName, browser)
    # browser.quit()


if __name__ == "__main__":
    main()
