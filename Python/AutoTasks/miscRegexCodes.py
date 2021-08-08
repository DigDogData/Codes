#!/usr/bin/env python3

# miscRegexCodes.py - example codes for character-based pattern matching

import re  # import regex module

# '\d+' to match 1+ digits, followed by '\s' to match space/tab/newline,
# followed by '\w+' to match 1+ letters/digits/underscores
xmasRegex = re.compile(r"\d+\s\w+")
text = "I have order for 12 drummers, 11 pipers, 10 lords, 9 ladies, 8 maids, \
        7 swans, 6 geese, 5 rings, 4 birds, 3 hens, 2 doves, 1 partridge to be \
        delivered to my home on street number 2522"
print(xmasRegex.findall(text))

# create your own shorthand character class for vowels
vowelRegex = re.compile(r"[aeiouAEIOU]")
print(vowelRegex.findall(text))

# create your own shorthand character class for consonants
# (add '\d', '\s', ',', '.' to strip digits, space and punctuations)
consonantRegex = re.compile(r"[^aeiouyAEIOUY\d\s,.]")
print(consonantRegex.findall(text))

# create your own shorthand character class for all letters and numbers
allRegex = re.compile(r"[a-zA-Z0-9]")
print(allRegex.findall(text))

# expression matching at the start of text (uses '^')
beginsWithString = re.compile(r"^I have")
print(beginsWithString.search(text))

# expression matching at the end of text (uses '$')
endsWithNumber = re.compile(r"\d+$")
print(endsWithNumber.search(text))

# expression matching at the start+end of text (uses '^' and '$')
wholeStringIsNum = re.compile(r"^\d+$")
text2 = "1234567890"
print(wholeStringIsNum.search(text2))

# wildcard character matching (uses '.' followed by pattern)
atRegex = re.compile(r".at")
text2 = "The cat in the hat sat on the flat mat and ate the rat to satiate himself"
print(atRegex.findall(text2))

# match anything (uses '.*') =>
# '.' matches any single character except newline, '*' matches 0+ preceding character
nameRegex = re.compile(r"First name: (.*), Last name: (.*)")
text2 = "First name: Manojit, Last name: Roy"
mo = nameRegex.search(text2)
print(mo.group(1) + " " + mo.group(2))

# match anything in non-greedy mode (uses '.*?' to match only 1st instance)
greedyRegex = re.compile(r"<.*>")
nongreedyRegex = re.compile(r"<.*?>")
text2 = "<To serve man> for dinner.>"
mo = greedyRegex.search(text2)
print(mo.group())
mo = nongreedyRegex.search(text2)
print(mo.group())

# match anything including newline (uses re.DOTALL)
noNewlineRegex = re.compile(".*")  # match anything except newline
newlineRegex = re.compile(".*", re.DOTALL)  # match including newline
text2 = "Serve the public trust.\nProtect the innocent.\nUphold the law."
mo = noNewlineRegex.search(text2)
print(mo.group())
mo = newlineRegex.search(text2)
print(mo.group())
