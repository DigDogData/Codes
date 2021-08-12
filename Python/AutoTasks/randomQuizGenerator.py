#!/usr/bin/env python3

# randomQuizGenerator.py - Creates quizzes with questions and answers in
# random order, along with the answer key

import random


def main():
    runQuiz()


def runQuiz():
    # quiz data as dictionary: keys are states and values are capitals
    capitals = {
        "Alabama": "Montgomery",
        "Alaska": "Juneau",
        "Arizona": "Phoenix",
        "Arkansas": "Little Rock",
        "California": "Sacramento",
        "Colorado": "Denver",
        "Connecticut": "Hartford",
        "Delaware": "Dover",
        "Florida": "Tallahassee",
        "Georgia": "Atlanta",
        "Hawaii": "Honolulu",
        "Idaho": "Boise",
        "Illinois": "Springfield",
        "Indiana": "Indianapolis",
        "Iowa": "Des Moines",
        "Kansas": "Topeka",
        "Kentacky": "Frankfort",
        "Lousiana": "Baton Rouge",
        "Maine": "Augusta",
        "Maryland": "Annapolis",
        "Massachusetts": "Boston",
        "Michigan": "Lansing",
        "Minnesota": "Saint Paul",
        "Mississippi": "Jackson",
        "Missouri": "Jefferson City",
        "Montana": "Helena",
        "Nebraska": "Lincoln",
        "Nevada": "Carson City",
        "New Hampshire": "Concord",
        "New Jersey": "Trenton",
        "New Mexico": "Santa Fe",
        "New York": "Albany",
        "North Carolina": "Raleigh",
        "North Dakota": "Bismarck",
        "Ohio": "Columbus",
        "Oklahoma": "Oklahoma City",
        "Oregon": "Salem",
        "Pennsylvania": "Harrisburg",
        "Rhode Island": "Providence",
        "South Carolina": "Columbia",
        "South Dakota": "Pierre",
        "Tennessee": "Nashville",
        "Texas": "Austin",
        "Utah": "Salt Lake City",
        "Vermont": "Montpelier",
        "Virginia": "Richmond",
        "Washington": "Olympia",
        "West Virginia": "Charleston",
        "Wisconsin": "Madison",
        "Wyoming": "Cheyenne",
    }

    # generate 35 quiz files (for 35 students)
    for quizNum in range(35):

        # create quiz and answer key files
        quizFile = open(f"QuizFiles/capitalsquiz{quizNum + 1}.txt", "w")
        answerKeyFile = open(f"QuizFiles/capitalsquiz_answers{quizNum + 1}.txt", "w")

        # write out header for the quiz, to be filled by the student
        quizFile.write("Name:\n\nDate:\n\nPeriod:\n\n")
        quizFile.write((" " * 20) + f"State Capitals Quiz (Form {quizNum + 1})")
        quizFile.write("\n\n")

        # shuffle order of states
        states = list(capitals.keys())
        random.shuffle(states)

        # loop through all 50 states, making a question for each
        for questionNum in range(50):

            # get correct answer from dictionary
            correctAnswer = capitals[states[questionNum]]
            # get all possible wrong answers:
            # step 1) duplicate all values in capitals dictionary
            # step 2) delete the correct answer
            wrongAnswers = list(capitals.values())  # step 1
            del wrongAnswers[wrongAnswers.index(correctAnswer)]  # step 2
            wrongAnswers = random.sample(
                wrongAnswers, 3
            )  # choose 3 random wrong answers
            answerOptions = wrongAnswers + [
                correctAnswer
            ]  # choices = 3 wrongs + 1 right
            random.shuffle(answerOptions)

            # write question and answer options to the quiz file
            quizFile.write(
                f"{questionNum + 1}. What is the capital of {states[questionNum]}?\n"
            )
            for i in range(4):
                quizFile.write(f"     {'ABCD'[i]}. {answerOptions[i]}\n")
            quizFile.write("\n")

            # write answer key to a file
            answerKeyFile.write(
                f"{questionNum + 1}. {'ABCD'[answerOptions.index(correctAnswer)]}\n"
            )

        quizFile.close()
        answerKeyFile.close()


if __name__ == "__main__":
    main()
