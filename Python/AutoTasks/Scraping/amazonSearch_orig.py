#!/usr/bin/env python3

# searchAmazon.py - Search Amazon prices by searchTerm 'wet cat food'
# (filtered by brand name 'Purina Friskies' and price range of $0 - $25)

import sys
import time
import logging
from selenium.webdriver.common.by import By
from util import startBrowser


# function to search Amazon
def searchAmazon(browser, url, searchTerm, filterTerm, minPrice, maxPrice):

    try:
        # load amazon.com
        browser.get(url)
        time.sleep(2)

        # enter searchTerm in search box
        logging.info(
            "Searching '%s' ('%s', $%s-$%s)...",
            searchTerm,
            filterTerm,
            minPrice,
            maxPrice,
        )
        searchBox = browser.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')
        searchBox.send_keys(searchTerm)
        time.sleep(2)

        # click search button
        searchButton = browser.find_element(
            By.XPATH, '//input[@id="nav-search-submit-button"]'
        )
        searchButton.click()
        time.sleep(2)

        # click filter name 'Purina Friskies'
        filterBox = browser.find_element(
            By.XPATH, '//span[text()="' + filterTerm + '"]'
        )
        filterBox.click()
        time.sleep(2)

        # enter price range
        lowPriceBox = browser.find_element(By.XPATH, '//input[@id="low-price"]')
        lowPriceBox.send_keys(minPrice)
        highPriceBox = browser.find_element(By.XPATH, '//input[@id="high-price"]')
        highPriceBox.send_keys(maxPrice)
        time.sleep(2)

        # click 'Go' button form price range
        goButton = browser.find_element(
            By.XPATH, '//input[contains(@class,"a-button-input")]'
        )
        goButton.click()
        time.sleep(2)

    except Exception as err:
        logging.error(str(err))
        sys.exit(1)


# function to get links for products
def getProductLinks(browser):
    pageUrls = []

    try:
        k = 1
        lastPage = False
        while not lastPage:  # loop through last page of product list

            # get links from current page
            itemElems = browser.find_elements(
                By.XPATH, '//a[contains(@class,"s-no-outline")]'
            )
            for i in range(len(itemElems)):
                pageUrls.append(itemElems[i].get_attribute("href"))
            logging.info("Page #%s scanned...", k)
            time.sleep(2)

            # click 'Next' button to go to next page
            try:
                nextButton = browser.find_element(
                    By.XPATH, '//a[contains(text(),"Next")]'
                )
                nextButton.click()
                k += 1
                time.sleep(2)
            except Exception:
                lastPage = True  # reached last page
                pass

        logging.info("Total %s items found in %s pages.", len(pageUrls), k)

    except Exception as err:
        logging.error(str(err))
        sys.exit(1)


# function to collect price data


def main():

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    url = "https://www.amazon.com"
    searchTerm = "wet cat food"
    filterTerm = "Purina Friskies"
    minPrice = 0
    maxPrice = 25
    browser = startBrowser("firefox", headless=False)  # Brave is buggy
    searchAmazon(browser, url, searchTerm, filterTerm, minPrice, maxPrice)
    getProductLinks(browser)
    # browser.quit()


if __name__ == "__main__":
    main()
