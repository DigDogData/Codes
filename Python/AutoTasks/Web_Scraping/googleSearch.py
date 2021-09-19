#!/usr/bin/env python3

# googleSearch.py - Search Google Image by keyword
# USAGE: py googleSearch.py <keyword>

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
    url = "https://www.google.com"
    browser = startBrowser("chrome", headless=False)  # Brave is buggy
    os.makedirs("google", exist_ok=True)  # create ./google folder (to store images)
    searchGoogle(url, browser)
    # browser.quit()


def searchGoogle(url, browser):

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # get keyword from CLI
    if len(sys.argv) == 2:
        keyword = sys.argv[1]
    else:
        sys.exit("USAGE: python googleSearch.py <keyword>")

    # open keyword page in browser
    appendUrl = "&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi8-rSt-onzAhUGXM0KHbA6A3wQ_AUoAXoECAIQAw&biw=1794&bih=928"
    keyword_url = url + "/search?q=" + keyword + appendUrl
    browser.get(keyword_url)

    # auto scroll down few times to expose more of page
    htmlElem = browser.find_element(By.TAG_NAME, "html")
    for __ in range(2):
        htmlElem.send_keys(Keys.END)
        time.sleep(5)  # pause between interactions

    # find images to be scraped from page
    imgList = browser.find_elements(By.CLASS_NAME, "isv-r PNCib MSM1fd BUooTd")
    # imgList = browser.find_elements(By.XPATH, '//img[contains(@class, "Q4LuWd")]')

    # loop through image thumbnails
    for i in range(len(imgList)):
        imgUrl = imgList[i]
        try:
            imgUrl.click()
            time.sleep(2)
            images = browser.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
            # for image in images:

            # continue
        except Exception:
            sys.exit()


if __name__ == "__main__":
    main()
