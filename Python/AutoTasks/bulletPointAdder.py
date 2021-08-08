#!/usr/bin/env python3

# bulletPointAdder.py - Adds bullet points to a list of texts on clipboard
# (example code that uses clipboard as IO)

try:
    import pyperclip  # first install xclip with <sudo apt install xclip>
except ImportError:
    print("Install pyperclip module")
    pass  # if pyperclip is not installed, do nothing


def main():

    # copy text from file 'Lists.txt' to clipboard and paste here
    TEXT = pyperclip.paste()

    addBulletPoints(TEXT)
    print("Modified text copied to clipboard")


def addBulletPoints(text):

    # separate lines and add stars
    lines = text.split("\n")
    for i in range(len(lines)):
        lines[i] = "* " + lines[i]

    text = "\n".join(lines)
    pyperclip.copy(text)  # copy text back to clipboard


if __name__ == "__main__":
    main()
