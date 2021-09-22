#!/usr/bin/env python3

# searchAmazon.py - Search Amazon prices by keyphrase
# (uses ActionChains to perfom mouse hover action)

import sys
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from util import startBrowser
from loginData import amazonLogin


# funtion to sign into Amazon
def signinToAmazon(url, browser, action):

    try:
        # load amazon.com
        logging.info("Signing into Amazon...")
        browser.get(url)
        time.sleep(2)

        # hover over 'Sign in' box
        signinHover = browser.find_element(
            By.XPATH, '//span[@id="nav-link-accountList-nav-line-1"]'
        )
        action.move_to_element(signinHover).perform()
        time.sleep(1)

        # click 'Sign in' button #1
        signinButton1 = browser.find_element(
            By.XPATH,
            '//div[@id="nav-flyout-ya-signin"]//span[@class="nav-action-inner"]',
        )
        signinButton1.click()
        time.sleep(2)

        # enter sign-in information
        signinElem = browser.find_element(By.XPATH, '//input[@id="ap_email"]')
        signinElem.send_keys(amazonLogin("username"))
        time.sleep(2)

        # continue
        continueElem = browser.find_element(By.XPATH, '//input[@id="continue"]')
        continueElem.click()
        time.sleep(2)

        # enter password information
        passwordElem = browser.find_element(By.XPATH, '//input[@id="ap_password"]')
        passwordElem.send_keys(amazonLogin("password"))
        time.sleep(2)

        # click 'Sign in' button #2
        signinButton2 = browser.find_element(By.XPATH, '//input[@id="signInSubmit"]')
        signinButton2.click()

        # click 'Enter OTP' button
        time.sleep(20)  # pause long enough to enter OTP from phone
        otpButton = browser.find_element(By.XPATH, '//input[@id="auth-signin-button"]')
        otpButton.click()
        logging.info("Signed in successfully.")
        time.sleep(2)

    except Exception as err:
        logging.error(str(err))
        sys.exit(1)


# function to search Amazon
def searchAmazon(keyphrase, browser):

    try:
        # search for keyphrase
        searchBox = browser.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')
        searchBox.send_keys(keyphrase)
        time.sleep(2)

        # click search button
        searchButton = browser.find_element(
            By.XPATH, '//input[@id="nav-search-submit-button"]'
        )
        searchButton.click()
        logging.info("Search executed successfully.")
        time.sleep(2)

    except Exception as err:
        logging.error(str(err))
        sys.exit(1)


def main():
    # get keyphrase from CLI
    if len(sys.argv) == 2:
        keyphrase = sys.argv[1]
    else:
        sys.exit("USAGE: python searchAmazon.py <keyphrase>")

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    url = "https://www.amazon.com"
    browser = startBrowser("brave", headless=False)  # Brave is buggy
    action = ActionChains(browser)
    signinToAmazon(url, browser, action)
    searchAmazon(keyphrase, browser)
    # browser.quit()


if __name__ == "__main__":
    main()
