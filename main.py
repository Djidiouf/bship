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

#we try to clear the terminal at the begining of each turn
def clear():
    if os.name == ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        os.system('clear')


#we initialize the board and fill it with water O
board = []
for x in range(5):
    board.append(["O"] * 5)

#we enhance the graphics by getting rig of that list-style
def print_board(board):
    for row in board:
        print ("  ".join(row))

#we define the number of turns of the game
turns_number = 4

# 1
#It's now the main thing, greetings to everybody!
print("---===[[[ BSHIP ]]]===---")
print("---Une idée braisnchat---")
print("BIG AI: Where is my bship? You have only %d turns." % turns_number)
print("")


# 2
#here we set the coordinates of the AI bship
def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

#cheat
print("#DEBUG: Row: %d | Col: %d" % (ship_row, ship_col))



def another_turn(turn):
    if turn == 3:
        print("BIG AI: You ran out of guess posibilities")
        print("BIG AI: Game Over")
        return False
    else:
        return True

# 3
#MAIN LOOP STRANGERS
for turn in range(turns_number):
    clear()
    print("BIG AI: Turn", turn +1, "on", turns_number)
    #we show the board to our players
    print("")
    print_board(board)

    guess_row = int(input("Guess Row:"))
    guess_col = int(input("Guess Col:"))


    if guess_row == ship_row and guess_col == ship_col:
        #success
        print("")
        print("PLAYER: %d, %d" % (guess_row, guess_col))
        print("BIG AI: Congratulations! You sunk my battleship!")
        break
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
            #out of perimeter
            print("")
            print("PLAYER: %d, %d" % (guess_row, guess_col))
            print("BIG AI: Oops, that's not even in the ocean.")
        elif(board[guess_row][guess_col] == "X"):
            #already guess
            print("")
            print("PLAYER: %d, %d" % (guess_row, guess_col))
            print("BIG AI: You guessed that one already.")
        else:
            #this guess miss
            print("")
            print("PLAYER: %d, %d" % (guess_row, guess_col))
            print("BIG AI: You missed my battleship!")
            board[guess_row][guess_col] = "X"

    if another_turn(turn) == False:
        break

    print("-------------------------")





