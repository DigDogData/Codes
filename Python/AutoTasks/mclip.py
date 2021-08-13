#!/usr/bin/env python3

# mclip.py - A multi-clipboard program (example that uses clipboard as IO)
# Usage: python mclip.py <keyword> - Copy keyword text to clipboard

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
        print("Usage: python mclip.py [keyword] - copy phrase text")
        sys.exit()

    keyword = sys.argv[1]  # assign 1st CL argument to keyword

    if keyword in text:
        pyperclip.copy(text[keyword])
        print("Text for '" + keyword + "' copied to clipboard.")
    else:
        print("There is no text for '" + keyword + "'.")


if __name__ == "__main__":
    main()
