#!/usr/bin/env python3

# mclip2.py - Modified mclip.py code that uses 'shelve' module:
# save each piece of clipboard text under a keyword
# run code with <python mclip2.py save [keyword]>

import sys

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing


def main():

    # dictionary of texts with keys
    TEXT = {
        "agree": """Yes, I agree. That sounds fine to me.""",
        "busy": """Sorry, can we do this later this week or next week?""",
        "upsell": """Would you consider making this a monthly donation?""",
    }

    # run copyToClipboard
    copyToClipboard(TEXT)


def copyToClipboard(text):

    # sys.argv() is an array for command line arguments in python
    # sys.argv[0] is filename 'mclip.py', sys.argv[1] is 1st command line argument
    if len(sys.argv) < 2:
        print("Usage: python mclip.py [keyphrase] - copy phrase text")
        sys.exit()

    keyphrase = sys.argv[1]  # assign 1st CL argument to keyphrase

    if keyphrase in text:
        pyperclip.copy(text[keyphrase])
        print("Text for '" + keyphrase + "' copied to clipboard.")
    else:
        print("There is no text for '" + keyphrase + "'.")


if __name__ == "__main__":
    main()
