#!/usr/bin/env python3

# pigLatin.py - converts English text to Pig Latin text:
# if a word begins with a vowel, string 'yay' is added to its end;
# if it begins with consonant(s), consonant is moved to the end followed by 'ay'


def main():

    # Pig Latin strings to be added
    str1 = "ay"
    str2 = "yay"

    print("Enter the English message to translate to Pig Latin:")
    pigLatin = englishToPigLatin(input("> "), str1, str2)

    print(pigLatin)


def englishToPigLatin(message, str1, str2):

    VOWELS = ("a", "e", "i", "o", "u", "y")  # define tuple of vowels

    pigLatin = ""  # initialize string of words in Pig Latin

    for word in message.split():

        # we need to strip non-letters from start and end of this word,
        # so words like 'old.' translates to 'oldyay.' instead of 'old.yay':
        # separate non-letters at the start of this word
        prefixNonLetters = ""
        while len(word) > 0 and not word[0].isalpha():  # word[0] is not letter
            prefixNonLetters += word[0]  # store non-letter word[0]
            word = word[1:]  # strip word[0] from word

        # if the whole word is non-lettered (like '400'), append it to pigLatin
        # and skip to next word
        if len(word) == 0:
            pigLatin += prefixNonLetters + " "
            continue

        # separate non-letters at the end of this word
        suffixNonLetters = ""
        while not word[-1].isalpha():
            suffixNonLetters += word[-1]
            word = word[:-1]

        # remember if the word was in uppercase or title case (uppercase initial),
        # so as to restore it after translation
        wasUpper = word.isupper()
        wasTitle = word.istitle()

        word = word.lower()  # make the word lowercase for translation

        # separate consonants at the start of this word
        prefixConsonants = ""
        while len(word) > 0 and not word[0] in VOWELS:
            prefixConsonants += word[0]
            word = word[1:]

        # if the word did start with consonant(s), add Pig Latin ending to it,
        # so words like 'sweigart' trnslates to 'eigartsway'; else just add 'yay'
        if prefixConsonants != "":
            word += prefixConsonants + str1
        else:
            word += str2

        # set the translated word back to uppercase or title case
        if wasUpper:
            word = word.upper()
        if wasTitle:
            word = word.title()

        # add non-letters back to the start or end of the word
        pigLatin += prefixNonLetters + word + suffixNonLetters + " "

    return pigLatin


if __name__ == "__main__":
    main()
