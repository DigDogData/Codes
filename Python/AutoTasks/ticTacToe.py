##############################################
# Code to play Tic Tac Toe
##############################################

import random


# function to print board
def drawBoard(board):
    print("-------")
    print("|" + board["top-L"] + "|" + board["top-M"] + "|" + board["top-R"] + "|")
    print("+-+-+-+")
    print("|" + board["mid-L"] + "|" + board["mid-M"] + "|" + board["mid-R"] + "|")
    print("+-+-+-+")
    print("|" + board["low-L"] + "|" + board["low-M"] + "|" + board["low-R"] + "|")
    print("-------")


# function to randomly choose who goes first (player or computer)
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return "computer"
    else:
        return "player"


# function to choose player's letter ("X" or "O"):
# returns a list of player’s and computer's letter
def inputPlayerLetter():
    letter = ""
    while not (letter == "X" or letter == "O"):
        print("Do you want to be X or O?")
        letter = input().upper()

    # 1st & 2nd list elements are player’s and computer's letters
    if letter == "X":
        return ["X", "O"]
    else:
        return ["O", "X"]


# function returns True if player wants to play again, else returns False
def playAgain():
    print("Play again? (yes or no)")
    return input().lower().startswith("y")


def makeMove(board, letter, move):
    board[move] = letter


# function returns True if player has won ('bo' for board and 'le' for letter)
def isWinner(bo, le):
    return (
        (bo[7] == le and bo[8] == le and bo[9] == le)  # across the bottom
        or (bo[4] == le and bo[5] == le and bo[6] == le)  # across the middle
        or (bo[1] == le and bo[2] == le and bo[3] == le)  # across the top
        or (bo[7] == le and bo[4] == le and bo[1] == le)  # down the left
        or (bo[8] == le and bo[5] == le and bo[2] == le)  # down the middle
        or (bo[9] == le and bo[6] == le and bo[3] == le)  # down the right
        or (bo[7] == le and bo[5] == le and bo[3] == le)  # right diagonal
        or (bo[9] == le and bo[5] == le and bo[1] == le)  # left diagonal
    )


# function makes a duplicate of the board and returns the duplicate
def getBoardCopy(board):
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard


# function returns true if the passed move is free on the passed board
def isSpaceFree(board, move):
    return board[move] == " "


# function to let the player type in their move
def getPlayerMove(board):
    move = " "
    while move not in "1 2 3 4 5 6 7 8 9".split() or not isSpaceFree(board, int(move)):
        print("What is your next move? (1-9)")
        move = input()
    return int(move)


# define dictionery for empty board
theBoard = {
    "top-L": " ",
    "top-M": " ",
    "top-R": " ",
    "mid-L": " ",
    "mid-M": " ",
    "mid-R": " ",
    "low-L": " ",
    "low-M": " ",
    "low-R": " ",
}

turn = "X"
for i in range(9):
    drawBoard(theBoard)
    print("Turn for " + turn + ". Move on which space?")
    move = input()
    theBoard[move] = turn
    if turn == "X":
        turn = "O"
    else:
        turn = "X"
