#!/usr/bin/env python3

# miscSeleniumCodes.py - Example codes using selenium's webdriver module

# to use Brave browser, download binary file 'chromedriver' from
# https://sites.google.com/chromium.org/driver/ and add its path
# (chromedriver version must match Chromium version in Brave: Menu->About Brave)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# use Brave browser
driverPath = "/home/roy/Downloads/chromedriver"
bravePath = "/usr/bin/brave-browser"
options = webdriver.ChromeOptions()
options.binary_location = bravePath
# options.add_argument("user-data-dir=/home/roy/.config/BraveSoftware/Brave-Browser")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
browser = webdriver.Chrome(service=Service(driverPath), options=options)
browser.get("https://inventwithpython.com")
