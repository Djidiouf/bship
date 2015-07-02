#-------------------------------------------------------------------------------
# Name:         bship
# Purpose:      a game without limits
#
# Author:       Djidiouf
#
# Created:      2015-06-29
# Licence:      bchat-licence
#-------------------------------------------------------------------------------

#import
from random import randint #used with random_row and random_col
import os #use with clear function

#we try to clear the terminal at the beginning of each turn
def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posif':
        os.system('clear')
    else:
        print("NOTICE: OS unknown, an attempt to clear the window cannot be made")

#we present the game
def print_header():
    print("               ===[[[ BSHIP ]]]===               ")
    print("----------------Une idee braisnchat----------------")
    print("BIG AI: Where is my bship? You have only %d turns." % turns_number)
    #cheat
    print("#DEBUG: Row: %d | Col: %d" % (ship_row, ship_col))
    print("                            __ ___ _ __ _ _ _      ")
    print("                           / - /_ ___ __ - -       ")
    print("                __________||_||____                ")
    print("~~~~~~~~~~~~~~~~\_________________/~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")

#we initialize the board and fill it with water O
board = []
for x in range(6):
    board.append(["."] * 6)
board[0][0] = "+"
board[0][1] = "1"
board[0][2] = "2"
board[0][3] = "3"
board[0][4] = "4"
board[0][5] = "5"
board[1][0] = "1"
board[2][0] = "2"
board[3][0] = "3"
board[4][0] = "4"
board[5][0] = "5"
#we enhance the graphics by getting rig of that list-style
def print_board(board):
    for row in board:
        print ("  ".join(row))

#we define the number of turns of the game
turns_number = 4

#here we set the coordinates of the AI bship
def random_row(board):
    return randint(1, len(board) - 1)

def random_col(board):
    return randint(1, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)


#It's now the main thing, greetings to everybody!
clear()
print_header()
print_board(board)


def another_turn(turn):
    if turn == 3:
        #failed because run out of turn
        print("BIG AI: You ran out of guess possibilities")
        print("BIG AI: Game Over")
        return False
    else:
        return True

# 3
#MAIN LOOP STRANGERS
for turn in range(turns_number):
    print("")
    print("BIG AI: Turn", turn +1, "on", turns_number)
    print("")
    guess_row = int(input("Guess Row:"))
    guess_col = int(input("Guess Col:"))


    if guess_row == ship_row and guess_col == ship_col:
        #success
        board[ship_row][ship_col] = "ù"
        clear()
        print_header()
        print_board(board)
        print("PLAYER: %d, %d" % (guess_row, guess_col))
        print("BIG AI: Congratulations! You sunk my battleship!")
        break
    else:
        if guess_row <= 0 or guess_row >= 6 or guess_col <= 0 or guess_col >= 6:
            #out of perimeter
            clear()
            print_header()
            print_board(board)
            print("")
            print("PLAYER: %d, %d" % (guess_row, guess_col))
            print("BIG AI: Oops, that's not even in the ocean.")
        elif board[guess_row][guess_col] == "x" or board[guess_row][guess_col] == "X":
            #already guess
            board[guess_row][guess_col] = "X"
            clear()
            print_header()
            print_board(board)
            print("")
            print("PLAYER: %d, %d" % (guess_row, guess_col))
            print("BIG AI: You guessed that one already.")
        else:
            #this guess miss
            board[guess_row][guess_col] = "x"
            clear()
            print_header()
            print_board(board)
            print("")
            print("PLAYER: %d, %d" % (guess_row, guess_col))
            print("BIG AI: You missed my battleship!")

    if another_turn(turn) == False:
        break

    print("-------------------------")





