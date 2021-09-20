#!/usr/bin/env python3

# googleSearch.py - Search Google Image by keyword
# USAGE: py googleSearch.py <keyword>

import sys
import time
import os
from selenium.webdriver.common.by import By
from util import startBrowser
from util import printLog


def main():
    url = "https://www.google.com"
    os.makedirs("google", exist_ok=True)  # create ./google folder (to store images)
    browser = startBrowser("firefox", headless=False)  # Brave is buggy
    searchGoogle(url, browser)
    # browser.quit()


# function to auto scroll down 'num' times to expose more of page
def scrollToEnd(browser, num):
    for __ in range(num):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # pause between interactions


# function to download ans save images
def downloadImage(browser, url):



def searchGoogle(url, browser):

    # get keyword from CLI
    if len(sys.argv) == 2:
        keyword = sys.argv[1]
    else:
        sys.exit("USAGE: python googleSearch.py <keyword>")

    # open keyword page in browser
    appendUrl = "&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi8-rSt-onzAhUGXM0KHbA6A3wQ_AUoAXoECAIQAw&biw=1794&bih=928"
    keyword_url = url + "/search?q=" + keyword + appendUrl
    browser.get(keyword_url)

    scrollToEnd(browser, 2)

    # find images to be scraped from page
    imgList = browser.find_elements(By.XPATH, '//img[contains(@class,"Q4LuWd")]')

    # loop through image thumbnails
    # for i in range(len(imgList)):
    for i in range(1):
        thumbnail = imgList[i]
        try:
            thumbnail.click()
            time.sleep(2)
            images = browser.find_elements(By.XPATH, '//img[contains(@class,"n3VNCb")]')
            # of the two results, only the correct one has 'https' in its link
            for image in images:
                if image.get_attribute("src") and "https" in image.get_attribute("src"):
                    imgUrl = image.get_attribute("src")
        except Exception as err:
            print(err)
            continue


if __name__ == "__main__":
    main()
