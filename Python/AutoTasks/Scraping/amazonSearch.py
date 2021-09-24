#!/usr/bin/env python3

# searchAmazon.py - Search Amazon prices by searchTerm 'wet cat food'
# (filtered by brand name 'Purina Friskies' and price range of $0 - $25)

import sys
import time
import re
import logging
import pandas as pd
from math import nan
from selenium.webdriver.common.by import By
from util import startBrowser


# class to save search data to file
class SaveData:
    def __init__(self, filename, product_list):
        self.filename = filename
        self.product_list = product_list
        logging.info("Saving data...")
        df = pd.DataFrame(self.product_list)
        df.to_csv(self.filename)
        logging.info("Done.")


# main class to run Amazon search
class AmazonAPI:

    # initializer
    def __init__(self, browser, base_url, search_term, filters):
        self.browser = browser
        self.base_url = base_url
        self.search_term = search_term
        self.brand = filters["brand"]
        self.min_price = filters["min_price"]
        self.max_price = filters["max_price"]

    # function to run methods defined below
    def run(self):
        self.search_amazon()
        page_links = self.get_product_links()
        product_list = self.get_product_info(page_links)
        return product_list

    # function to convert price string to float
    def convert_price(self, price):
        price = re.compile(r"\d+\.\d{2}").search(price)[0]
        return float(price)

    # function to convert rate string to float
    def convert_rate(self, rate):
        rate = re.compile(r"\d+\.\d{2}").search(rate)[0]
        return float(rate)

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
            self.browser.set_page_load_timeout(30)
            time.sleep(2)

            # enter search_term in search box
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
                    By.XPATH,
                    '//span[@class="rush-component"]//a[contains(@class,"s-no-outline")]',
                )
                for i in range(len(item_elems)):
                    page_urls.append(item_elems[i].get_attribute("href"))
                logging.info("Search result page #%s scanned", k)

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

            logging.info("(Total %s items found in %s pages.)", len(page_urls), k)

        except Exception as err:
            logging.error(str(err))
            sys.exit(1)

        return page_urls

    # function to collect product info from each product page
    def get_product_info(self, page_urls):

        # loop through page url list and go to each product page
        product_list = []
        for i in range(len(page_urls)):
            page_url = page_urls[i]
            try:
                self.browser.get(page_url)
                self.browser.set_page_load_timeout(30)
                time.sleep(2)

                # get product name
                product_name = self.browser.find_element(
                    By.XPATH, '//span[@id="productTitle"]'
                ).text

                # get price
                try:
                    price_str = self.browser.find_element(
                        By.XPATH, '//span[@id="priceblock_ourprice"]'
                    ).text
                    price = self.convert_price(price_str)  # convert string to float
                except Exception:
                    price = nan  # price info not available
                    pass

                # get price/lb
                try:
                    rate_str = self.browser.find_element(
                        By.XPATH,
                        '//td[@class="a-span12"]//span[@class="a-size-small a-color-price"]',
                    ).text
                    rate = self.convert_rate(rate_str)  # convert string to float
                except Exception:
                    rate = nan  # price/lb info not available
                    pass

                # collect product info
                product_info = {
                    "name": product_name,
                    "price": price,
                    "price_per_lb": rate,
                }
                product_list.append(product_info)
                logging.info("Product page #%s scanned", i + 1)

            except Exception as err:
                logging.error(str(err))
                continue

        return product_list


# run main code
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
    browser = startBrowser("chrome", headless=True)
    fp = open("amazon.csv", "w")

    # execute code
    data = AmazonAPI(browser, base_url, search_term, filters).run()
    SaveData(fp, data)
    browser.quit()
    fp.close()
