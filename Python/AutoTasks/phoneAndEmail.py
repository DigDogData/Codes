#!/usr/bin/env python3

# phoneAndEmail.py - Finds phone numbers and email addresses on the clipboard
# (to test, copy entire content of the page https://nostarch.com/contactus to
# clipboard with Ctrl-A+Ctrl-C and run this code)

import re  # import regex module

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing


# main() function
def main():

    # paste clipboard text
    TEXT = str(pyperclip.paste())

    # get matched output
    output = getPhoneEmail(TEXT)

    # copy results to the clipboard
    if len(output) > 0:
        textout = "\n".join(output)
        pyperclip.copy(textout)
        print("Copied to clipboard:")
        print(textout)
    else:
        print("No phone number of email addresses found.")


# getPhoneEmail() function
def getPhoneEmail(text):

    # creat phone regex
    phoneRegex = re.compile(
        r"""(
            (\d{3}|\(\d{3}\))?              # (optional) area code w/o parentheses
            (\s|-|\.)?                      # (optional) separator: space/'-'/'.'
            (\d{3})                         # first 3 digits
            (\s|-|\.)                       # separator
            (\d{4})                         # last 4 digits
            (\s*(ext|x|ext.)\s*(\d{2,5}))?  # extension followed by 2-5 digits w/o space
            )""",
        re.VERBOSE,
    )

    # create email regex
    emailRegex = re.compile(
        r"""(
            [a-zA-Z0-9._%+-]+    # username: letters/digits/'.'/'_'/'%'/'+'/'-'
            @                    # @ symbol
            [a-zA-Z0-9.-]+       # domain name: letters/numbers/'.'/'-'
            (\.[a-zA-Z]{2,4})    # dot-something: 2-4 letters
            )""",
        re.VERBOSE,
    )

    # find matches in text
    matches = []
    for groups in phoneRegex.findall(text):
        phoneNum = "-".join([groups[1], groups[3], groups[5]])
        if groups[8] != "":
            phoneNum += " x" + groups[8]  # add extension
        matches.append(phoneNum)
    for groups in emailRegex.findall(text):
        matches.append(groups[0])  # groups[0] matches entire regex

    return matches


# main() function call
if __name__ == "__main__":
    main()
