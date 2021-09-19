#!/usr/bin/env python3

# miscSeleniumCodes.py - Example codes using selenium's webdriver module

import sys
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from util import startBrowser

# *** make sure no other browser instance is open ***
# url = "https://inventwithpython.com"
# browser = startBrowser("firefox")
# browser.get(url)

# find element with class name 'cover-thumb'
# try:
#    elem = browser.find_element(By.CLASS_NAME, "cover-thumb")
#    print("Found <%s> element with that class name!" % (elem.tag_name))
# except Exception:
#    print("Was not able to find an element with that name.")

# click on page
# try:
#    linkElem = browser.find_element(By.LINK_TEXT, "Read Online for Free")
#    linkElem.click()  # follow 'Read Onine for Free' link
# except Exception:
#    print("Was not able to find this link.")

# fill out login info (*** log out first ***)
# (find out user ID and password element keys by inspecting URL)
# url = "https://github.com/login"
# browser = startBrowser("firefox")
# browser.get(url)
# loginToSite(browser, "login_field", "password")

# use special keys (works with firefox, not with brave)
# url = "https://nostarch.com"
# browser = startBrowser("brave")
# browser.get(url)
# htmlElem = browser.find_element(By.TAG_NAME, "html")
# htmlElem.send_keys(Keys.END)  # scroll to bottom
# time.sleep(2)
# htmlElem.send_keys(Keys.HOME)  # scroll to top
# time.sleep(2)

# browser buttons
url = "https://nostarch.com"
browser = startBrowser("brave")
browser.get(url)
# browser.back()
# browser.forward()
# browser.close()
# browser.quit()
for __ in range(10):
    browser.refresh()
    time.sleep(5)
