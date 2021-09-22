#!/usr/bin/env python3

# amazonSignin.py - Sign into amazon.com
# (uses ActionChains to perfom mouse hover action)

import sys
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from util import startBrowser
from loginData import amazonLogin


# funtion to sign into Amazon
def signinToAmazon(browser, url, action):

    try:
        # load amazon.com
        browser.get(url)
        time.sleep(2)

        # hover over 'Sign in' box
        logging.info("Signing into Amazon...")
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

        # enter OTP code
        otpBox = browser.find_element(By.XPATH, '//input[@id="auth-mfa-otpcode"]')
        otpString = input("Enter OTP from phone: ")
        otpBox.send_keys(otpString)
        time.sleep(2)

        # click OTP button
        otpButton = browser.find_element(By.XPATH, '//input[@id="auth-signin-button"]')
        otpButton.click()
        logging.info("Signed in successfully.")
        time.sleep(2)

    except Exception as err:
        logging.error(str(err))
        sys.exit(1)


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
    browser = startBrowser("brave", headless=False)  # Brave is buggy
    action = ActionChains(browser)
    signinToAmazon(browser, url, action)
    # browser.quit()


if __name__ == "__main__":
    main()
