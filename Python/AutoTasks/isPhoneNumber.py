#!/usr/bin/env python3

# isPhoneNumber.py - finds US/Canada phone number from text by pattern matching

import re  # import regex module

message = "415-555-1011 is my home, 415-555-3254 my cell, (415) 555-9999 my office."

# grouped pattern matching ('()' groups area code and number separately)
regexPattern = re.compile(r"(\d{3})-(\d{3}-\d{4})")  # regex object
mo = regexPattern.search(message)
areaCode, mainNumber = mo.groups()  # groups() method returns separate groups
print("Home area Code: " + areaCode)
print("Home main number: " + mainNumber)
print("Home full number: " + mo.group())  # group() method returns whole pattern

regexPattern = re.compile(r"(\(\d{3}\)) (\d{3}-\d{4})")
mo = regexPattern.search(message)
areaCode, mainNumber = mo.groups()
print("Office area Code: " + areaCode)
print("Office main number: " + mainNumber)
print("Office full number: " + mo.group())

# findall() finds all instances of same pattern
regexPattern = re.compile(r"\d{3}-\d{3}-\d{4}")  # ungrouped pattern matching
mo = regexPattern.findall(message)
print(mo)

# piped matching + findall() to find all instances of different patterns
regexPattern = re.compile(r"\d{3}-\d{3}-\d{4}|\(\d{3}\) \d{3}-\d{4}")
mo = regexPattern.findall(message)
print(mo)
