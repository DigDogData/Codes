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


# main class to run Amazon signing in script
class AmazonAPI:

    # initializer
    def __init__(self, browser, base_url, action):
        self.browser = browser
        self.base_url = base_url
        self.action = action

    # function to enter OTP
    def enter_otp(self):
        otp_box = self.browser.find_element(By.XPATH, '//input[@id="auth-mfa-otpcode"]')
        otp_string = input("Enter OTP from phone: ")
        otp_box.send_keys(otp_string)
        time.sleep(2)
        return None

    # funtion to sign in to Amazon
    def sign_in(self):

        try:

            # load amazon.com
            self.browser.get(self.base_url)
            self.browser.set_page_load_timeout(30)
            time.sleep(2)

            # hover over 'Sign in' box
            logging.info("Signing into Amazon...")
            signin_hover = self.browser.find_element(
                By.XPATH, '//span[@id="nav-link-accountList-nav-line-1"]'
            )
            self.action.move_to_element(signin_hover).perform()
            time.sleep(1)

            # click 'Sign in' button #1
            signin_button1 = self.browser.find_element(
                By.XPATH,
                '//div[@id="nav-flyout-ya-signin"]//span[@class="nav-action-inner"]',
            )
            signin_button1.click()
            time.sleep(2)

            # enter sign-in information
            signin_elem = self.browser.find_element(By.XPATH, '//input[@id="ap_email"]')
            signin_elem.send_keys(amazonLogin("username"))
            time.sleep(2)

            # continue
            continue_elem = self.browser.find_element(
                By.XPATH, '//input[@id="continue"]'
            )
            continue_elem.click()
            time.sleep(2)

            # enter password information
            password_elem = self.browser.find_element(
                By.XPATH, '//input[@id="ap_password"]'
            )
            password_elem.send_keys(amazonLogin("password"))
            time.sleep(2)

            # click 'Sign in' button #2
            signin_button2 = self.browser.find_element(
                By.XPATH, '//input[@id="signInSubmit"]'
            )
            signin_button2.click()

            # enter OTP code
            self.enter_otp()

            # click OTP button
            otp_button = self.browser.find_element(
                By.XPATH, '//input[@id="auth-signin-button"]'
            )
            otp_button.click()
            logging.info("Signed in successfully.")
            time.sleep(2)

        except Exception as err:
            logging.error(str(err))
            sys.exit(1)

        return None


# run main function
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
    browser = startBrowser("brave", headless=False)
    action = ActionChains(browser)

    # execute code
    AmazonAPI(browser, base_url, action).sign_in()
    # browser.quit()
