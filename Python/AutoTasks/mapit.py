#!/usr/bin/env python3

# mapit.py - Launches a map in the browser using address from command line / clipboard
# Example : <mapit 870 Valencia St, San Francisco, CA 94110>

import sys
import webbrowser

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing

if len(sys.argv) > 1:
    # get address from command line
    address = " ".join(sys.argv[1:])
else:
    # get address from clipboard
    address = pyperclip.paste()

webbrowser.open("https://www.google.com/maps/place/" + address)
