#!/usr/bin/env python3

# multiplicationQuiz.py - 10 multiplication quiz questions for user

import random
import time

try:
    import pyinputplus as pyip
except ImportError:
    print("Install pyinputplus module")
    pass  # do nothing


def main():
    numberOfQuestions = 10
    correctAnswers = runQuiz(numberOfQuestions)
    print("Score: %s / %s" % (correctAnswers, numberOfQuestions))


def runQuiz(numQ):
    correctCount = 0
    for questionNumber in range(numQ):

        # pick two single-digit random numbers
        num1 = random.randint(0, 9)
        num2 = random.randint(0, 9)

        # create a #Qn: N x N = prompt for the user
        prompt = "#Q%s: %s x %s = " % (questionNumber + 1, num1, num2)

        try:
            # right answers are handled by allowRegexes: '%s' is replaced by num1*num2,
            # '^' and '$' ensure answer begins and ends with correct number;
            # wrong answers are handled by blockRegexes: if user response does not
            # match correct answer, '.*' ensures any other answer is rejected
            pyip.inputStr(
                prompt,
                allowRegexes=["^%s$" % (num1 * num2)],
                blockRegexes=[(".*", "Incorrect!")],
                timeout=10,
                limit=3,
            )
        except pyip.TimeoutException:
            print("Out of time!")
        except pyip.RetryLimitException:
            print("Out of tries!")
        else:
            # this block runs if no exceptions were raised in the try block
            print("Correct!")
            correctCount += 1

        time.sleep(1)  # brief pause to let the user see the result

    return correctCount


if __name__ == "__main__":
    main()
