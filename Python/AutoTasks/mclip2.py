#!/usr/bin/env python3

# mclip2.py - Saves/loads pieces of text to/from clipboard
# Usage: python mclip2.py save <keyword> - Saves clipboard to file
#        python mclip2.py <keyword> - Loads keyword to clipboard
#        python mclip2.py list - loads all keywords to clipboard

import sys
import shelve

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing


def main():

    mclip2Shelf = shelve.open("PyData/mclip2")  # file to save/load clipboard
    fileToClipboard(mclip2Shelf)  # run code
    mclip2Shelf.close()


def fileToClipboard(file):

    # save clipboard to file (if 2 command line arguments)
    if len(sys.argv) == 3 and sys.argv[1].lower() == "save":
        file[sys.argv[2]] = pyperclip.paste()

    # list/load clipboard content (if only 1 command line argument)
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == "list":
            pyperclip.copy(str(list(file.keys())))  # list content
        elif sys.argv[1] in file:
            pyperclip.copy(file[sys.argv[1]])  # load keyword if exists


if __name__ == "__main__":
    main()
