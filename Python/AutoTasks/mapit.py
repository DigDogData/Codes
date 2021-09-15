#!/usr/bin/env python3

# mapit.py - Launches a map in the browser using address from command line/clipboard
# Example : <python mapit.py 870 Valencia St, San Francisco, CA 94110>

import sys
import webbrowser

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing

if len(sys.argv) > 1:  # argument is more than 'mapit.py'
    # get address from command line
    address = " ".join(sys.argv[1:])
else:
    # get address from clipboard
    address = pyperclip.paste()

url = "https://www.google.com/maps/place/" + address
webbrowser.open(url)  # ignore console error messages (debian bug)
# webbrowser.open_new(url)
# webbrowser.open_new_tab(url)
