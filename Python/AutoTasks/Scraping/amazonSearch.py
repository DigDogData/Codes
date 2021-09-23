#!/usr/bin/env python3

# searchAmazon.py - Search Amazon prices by searchTerm 'wet cat food'
# (filtered by brand name 'Purina Friskies' and price range of $0 - $25)

import sys
import time
import logging
from selenium.webdriver.common.by import By
from util import startBrowser


class AmazonAPI:

    # initializer
    def __init__(self, browser, base_url, search_term, filters):
        self.browser = browser
        self.base_url = base_url
        self.search_term = search_term
        self.brand = filters["brand"]
        self.min_price = filters["min_price"]
        self.max_price = filters["max_price"]

    # function to run AmazonAPI
    def run(self):
        self.search_amazon()
        links = self.get_product_links()
        self.get_product_info(links)
        return None

    # function to search Amazon
    def search_amazon(self):

        try:
            logging.info(
                "Searching '%s' ('%s', $%s-$%s)",
                self.search_term,
                self.brand,
                self.min_price,
                self.max_price,
            )

            # load amazon.com
            self.browser.get(self.base_url)
            time.sleep(2)

            # enter searchTerm in search box
            search_box = self.browser.find_element(
                By.XPATH, '//input[@id="twotabsearchtextbox"]'
            )
            search_box.send_keys(self.search_term)
            time.sleep(2)

            # click search button
            search_button = self.browser.find_element(
                By.XPATH, '//input[@id="nav-search-submit-button"]'
            )
            search_button.click()
            time.sleep(2)

            # click filter name 'Purina Friskies'
            filter_box = self.browser.find_element(
                By.XPATH, '//span[text()="' + self.brand + '"]'
            )
            filter_box.click()
            time.sleep(2)

            # enter price range
            lowprice_box = self.browser.find_element(
                By.XPATH, '//input[@id="low-price"]'
            )
            lowprice_box.send_keys(self.min_price)
            highprice_box = self.browser.find_element(
                By.XPATH, '//input[@id="high-price"]'
            )
            highprice_box.send_keys(self.max_price)
            time.sleep(2)

            # click 'Go' button form price range
            go_button = self.browser.find_element(
                By.XPATH, '//input[contains(@class,"a-button-input")]'
            )
            go_button.click()
            time.sleep(2)

        except Exception as err:
            logging.error(str(err))
            sys.exit(1)

        return None

    # function to get links for products
    def get_product_links(self):
        page_urls = []

        try:
            k = 1
            last_page = False
            while not last_page:  # loop through last page of product list

                # get links from current page
                item_elems = self.browser.find_elements(
                    By.XPATH, '//a[contains(@class,"s-no-outline")]'
                )
                for i in range(len(item_elems)):
                    page_urls.append(item_elems[i].get_attribute("href"))
                logging.info("Page #%s scanned", k)
                time.sleep(2)

                # click 'Next' button to go to next page
                try:
                    next_button = self.browser.find_element(
                        By.XPATH, '//a[contains(text(),"Next")]'
                    )
                    next_button.click()
                    k += 1
                    time.sleep(2)
                except Exception:
                    last_page = True  # reached last page
                    pass

            logging.info("Total %s items found in %s pages.", len(page_urls), k)

        except Exception as err:
            logging.error(str(err))
            sys.exit(1)

        return page_urls

    # function to collect product info from each product page
    def get_product_info(self, page_urls):

        # loop through page url list and go to each product page
        # for i in range(len(page_urls)):
        for i in range(1):
            page_url = page_urls[i]
            logging.info("Scanning producet page #%s", i + 1)
            try:
                self.browser.get(page_url)
                time.sleep(2)

                # get product name, vendor name, price
                product_name = self.browser.find_element(
                    By.XPATH, '//span[@id="productTitle"]'
                )
                vendor_name = self.browser.find_element(
                    By.XPATH, '//a[@id="bylineInfo"]'
                )
                price = self.browser.find_element(
                    By.XPATH, '//span[@id="priceblock_ourprice"]'
                )
                time.sleep(2)

            except Exception as err:
                logging.error(str(err))
                continue


if __name__ == "__main__":

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # initialize variables
    base_url = "https://www.amazon.com"
    search_term = "wet cat food"
    brand = "Purina Friskies"
    min_price = 0
    max_price = 25
    filters = {
        "brand": brand,
        "min_price": min_price,
        "max_price": max_price,
    }
    browser = startBrowser("brave", headless=False)

    # execute code
    amaz = AmazonAPI(browser, base_url, search_term, filters)
    amaz.run()
    # browser.quit()
