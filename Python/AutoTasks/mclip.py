#!/usr/bin/env python3

# mclip.py - A multi-clipboard program
# run code with <python mclip.py [keyphrase]>

import sys
import pyperclip  # first install xclip with <sudo apt install xclip>

# dictionary of texts with keys
TEXT = {
    "agree": """Yes, I agree. That sounds fine to me.""",
    "busy": """Sorry, can we do this later this week or next week?""",
    "upsell": """Would you consider making this a monthly donation?""",
}

# command line arguments are stored in sys.argv:
# 1st item in sys.argv is filename 'mclip.py', 2nd item is keyphrase
if len(sys.argv) < 2:
    print("Usage: python mclip.py [keyphrase] - copy phrase text")
    sys.exit()

keyphrase = sys.argv[1]

if keyphrase in TEXT:
    pyperclip.copy(TEXT[keyphrase])
    print("Text for '" + keyphrase + "' copied to clipboard.")
else:
    print("There is no text for '" + keyphrase + "'.")
