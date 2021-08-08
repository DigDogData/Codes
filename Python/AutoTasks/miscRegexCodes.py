#!/usr/bin/env python3

# miscRegexCodes.py - example codes for character-based pattern matching
######################################################################################
#   \d                  Matches a numeric digit (from 0 to 9)
#   \D                  Matches a character that is NOT a (numeric) digit
#   \w                  Matches a word (letter, numeric digit, or underscore)
#   \W                  Matches a character that is NOT a letter, digit, or underscore
#   \s                  Matches a space (whitespace, tab, or newline character)
#   \S                  Matches a character that is NOT a space, tab, or newline
#   ?                   Matches 0 or 1 of preceding group
#   *                   Matches 0 or more of the preceding group
#   +                   Matches 1 or more of the preceding group
#   {n}                 Matches exactly n of the preceding group
#   {n,}                Matches n or more of the preceding group
#   {,m}                Matches 0 to m of the preceding group
#   {n,m}               Matches at least n and at most m of the preceding group
#   {n,m}? or *? or +?  Performs a non-greedy match of the preceding group
#   ^spam               Means the string must begin with 'spam'
#   spam$               Means the string must end with 'spam'
#   .                   Matches any 1 character except newline characters
#   [...]               Matches any character between the brackets
#   [^...]              Matches any character that is NOT between the brackets
######################################################################################

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

# case-insensitive matching (uses re.IGNORECASE or re.I)
noCaseRegex = re.compile(r".op", re.I)
text = "ROBOCOP is part man, part machine, all cop."
mo = noCaseRegex.findall(text)
print(mo)

# substituting with sub() method
namesRegex = re.compile(r"Agent \w+")
text = "Agent Alice gave the secret documents to Agent Bob."
mo = namesRegex.sub("******", text)  # replaces whole pattern
print(mo)
namesRegex = re.compile(r"Agent (\w)\w*")
text = "Agent Alice gave the secret documents to Agent Bob."
mo = namesRegex.sub(r"\1*****", text)  # replaces part of pattern ((\w) group)
print(mo)

# managing complex regex by ignoring inline comments (uses re.VERBOSE)
phoneRegex = re.compile(
    r"""(
        (\d{3}|\(\d{3}\))?              # area code
        (\s|-|\.)?                      # separator
        \d{3}                           # first 3 digits
        (\s|-|\.)                       # separator
        \d{4}                           # last 4 digits
        (\s*(ext|x|ext.)\s*\d{2,5})?    # extension
        )""",
    re.VERBOSE,
)

# combining mutiple arguments via piping (re.compile() takes only one 2nd argument)
someRegexValue = re.compile("foo", re.IGNORECASE | re.DOTALL | re.VERBOSE)
