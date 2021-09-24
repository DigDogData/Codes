#!/usr/bin/env python3

# imgurDownload.py - Download Imgur images by keyword (uses selenium)
# USAGE: py imgurDownload.py <search_term> <limit>

import sys
import time
import os
import requests
import logging
from selenium.webdriver.common.by import By
from util import startBrowser


# class to download images
class ImgurAPI:

    # initializer
    def __init__(self, browser, base_url, search_term, limit, folder_name, scroll_num):
        self.browser = browser
        self.base_url = base_url
        self.search_term = search_term
        self.limit = limit
        self.folder_name = folder_name
        self.scroll_num = scroll_num

    # function to auto-scroll few times to expose more of page
    def scroll_to_end(self):
        for __ in range(self.scroll_num):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(5)
        return None

    # function to print image count for search_term
    def show_image_count(self):
        img_count_elem = self.browser.find_elements(
            By.XPATH, '//span[contains(@class,"sorting-text-align")]//i'
        )
        img_count = img_count_elem[0].get_attribute("innerHTML")
        print("------------------------------------------")
        print("There are %s images about '%s'." % (img_count, self.search_term))
        print("Downloading first %s images..." % self.limit)
        print("------------------------------------------")
        return None

    # function to download and save image (uses requests)
    def download_image(self, image_url):

        try:
            image_res = requests.get(image_url, timeout=10)
            try:
                image_res.raise_for_status()
                image_name = os.path.basename(image_url)
                image_file = open(os.path.join(self.folder_name, image_name), "wb")
                for chunk in image_res.iter_content(100000):
                    image_file.write(chunk)
                image_file.close()
                logging.info("Image '%s' saved.", image_name)

            except Exception as err:  # if there is connection error
                logging.error("Connection Error: " + str(err))
                pass

        except Exception as err:  # if there is other error (e.g. timeout)
            logging.error("Image Download Error: " + str(err))
            pass

        return None

    # function to search Imgur
    def search_imgur(self):

        try:
            logging.info("Searching '%s'...", self.search_term)

            # load imgur.com
            self.browser.get(self.base_url)
            self.browser.set_page_load_timeout(30)
            time.sleep(2)

            # enter search_term in search box
            search_box = self.browser.find_element(
                By.XPATH, '//input[contains(@class,"Searchbar")]'
            )
            search_box.send_keys(self.search_term)
            time.sleep(2)

            # click search button
            search_button = self.browser.find_element(
                By.XPATH,
                '//button[contains(@class,"Searchbar")]',
            )
            search_button.click()
            time.sleep(2)

            # auto-scroll search page few times
            self.scroll_to_end()

            # find list of images to be scraped from page
            img_list = self.browser.find_elements(
                By.XPATH, '//a[contains(@class,"image-list-link")]'
            )
            page_urls = [
                url.get_attribute("href") for url in img_list
            ]  # get all page URLs

            # loop through image thumbnails and load image page
            for i in range(int(self.limit)):
                page_url = page_urls[i]
                logging.info("Source URL(#%s): %s" % (i + 1, page_url))
                try:
                    self.browser.get(page_url)  # load imnage source page
                    time.sleep(2)

                    # get image URL(s)
                    images = self.browser.find_elements(
                        By.XPATH, '//img[contains(@class,"image-placeholder")]'
                    )
                    if len(images) > 0:
                        for image in images:
                            img_url = image.get_attribute("src")
                            self.download_image(img_url)
                    else:
                        logging.warning("There is no image in this page.")

                except Exception as err:
                    logging.error(str(err))
                    continue  # skip to beginning of loop

        except Exception as err:
            logging.error(str(err))
            sys.exit(1)

        return None


if __name__ == "__main__":

    # get keyword from CLI
    if len(sys.argv) == 3:
        search_term = sys.argv[1]
        limit = sys.argv[2]
    else:
        sys.exit("USAGE: python imgurDownload.py <search_term> <limit>")

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # initialize variables
    base_url = "https://imgur.com"
    folder_name = "imgur"  # create ./imgur folder to store images
    os.makedirs(folder_name, exist_ok=True)
    browser = startBrowser("firefox", headless=True)
    scroll_num = 2

    # execute code
    ImgurAPI(
        browser, base_url, search_term, limit, folder_name, scroll_num
    ).search_imgur()
    browser.quit()
