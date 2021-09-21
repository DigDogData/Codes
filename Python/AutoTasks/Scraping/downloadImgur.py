#!/usr/bin/env python3

# downloadImgur.py - Download Imgur images by keyword (uses selenimu)
# USAGE: py downloadImgur.py <keyword> <limit>

import sys
import time
import os
import requests
import logging
from selenium.webdriver.common.by import By
from util import startBrowser


# function to auto-scroll 'num' times to expose more of page
def scrollToEnd(browser, num):
    for __ in range(num):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # pause between interactions


# function to print image count for keyword
def showImageCount(browser, keyword, limit):
    imgCountElem = browser.find_elements(
        By.XPATH, '//span[contains(@class,"sorting-text-align")]//i'
    )
    imgCount = imgCountElem[0].get_attribute("innerHTML")
    print("------------------------------------------")
    print("There are %s images about '%s'." % (imgCount, keyword))
    print("Downloading first %s images..." % limit)
    print("------------------------------------------")


# function to download and save image (uses requests)
def downloadImage(image_url, folderName, logging):
    try:
        image_res = requests.get(image_url, timeout=10)
        try:
            image_res.raise_for_status()
            image_name = os.path.basename(image_url)
            imageFile = open(os.path.join(folderName, image_name), "wb")
            for chunk in image_res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            logging.info("Image '%s' saved.", image_name)
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
    showImageCount(browser, keyword, limit)

    # find images to be scraped from page
    imgList = browser.find_elements(By.XPATH, '//a[contains(@class,"image-list-link")]')
    pageUrls = [url.get_attribute("href") for url in imgList]  # get all page URLs

    # loop through image thumbnails and load image page
    for i in range(int(limit)):
        pageUrl = pageUrls[i]
        logging.info("Page URL(#%s): %s" % (i + 1, pageUrl))
        try:
            browser.get(pageUrl)
            time.sleep(2)
            # get image URL(s)
            images = browser.find_elements(
                By.XPATH, '//img[contains(@class,"image-placeholder")]'
            )
            if len(images) > 0:
                for image in images:
                    imgUrl = image.get_attribute("src")
                    # logging.info("Image URL: " + imgUrl)
                    downloadImage(imgUrl, folderName, logging)
            else:
                logging.warning("There is no image in this page.")
        except Exception as err:
            logging.error(str(err))
            continue  # skip to beginning of loop


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
    browser = startBrowser("firefox", headless=True)  # Brave/Chrome buggy
    searchImgur(keyword, limit, url, folderName, browser)
    browser.quit()


if __name__ == "__main__":
    main()
