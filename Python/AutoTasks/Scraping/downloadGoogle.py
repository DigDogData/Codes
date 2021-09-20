#!/usr/bin/env python3

# downloadGoogle.py - Download Google images by keyword
# USAGE: py downloadGoogle.py <keyword> <limit>

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


# funtion to search google
def searchGoogle(keyword, limit, url, folderName, browser):

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # open keyword page in browser
    appendUrl = "&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi8-rSt-onzAhUGXM0KHbA6A3wQ_AUoAXoECAIQAw&biw=1794&bih=928"
    keyword_url = url + "/search?q=" + keyword + appendUrl
    browser.get(keyword_url)

    scrollToEnd(browser, 1)  # auto-scroll search page few times

    # find images to be scraped from page
    imgList = browser.find_elements(By.XPATH, '//img[contains(@class,"Q4LuWd")]')

    # loop through image thumbnails
    for i in range(int(limit)):
        thumbnail = imgList[i]
        try:
            thumbnail.click()  # load image sidebar
            time.sleep(2)
            # get image URL
            images = browser.find_elements(By.XPATH, '//img[contains(@class,"n3VNCb")]')
            for image in images:
                image_src = image.get_attribute("src")
                # get *correct* link (with 'https' and without 'gstatic.com')
                if "https" in image_src and "gstatic.com" not in image_src:
                    imgUrl = image.get_attribute("src")
            logging.info("Image Source '%s' ==>", imgUrl.split("/")[2])
            downloadImage(i, imgUrl, folderName, logging)
        except Exception as err:
            logging.error(str(err))
            continue  # skip to beginning of loop


def main():
    # get keyword from CLI
    if len(sys.argv) == 3:
        keyword = sys.argv[1]
        limit = sys.argv[2]
    else:
        sys.exit("USAGE: python googleSearch.py <keyword> <limit>")

    url = "https://www.google.com"
    folderName = "google"  # create ./google folder to store images
    os.makedirs(folderName, exist_ok=True)
    browser = startBrowser("firefox", headless=True)  # Brave is buggy
    searchGoogle(keyword, limit, url, folderName, browser)
    browser.quit()


if __name__ == "__main__":
    main()
