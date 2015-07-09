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

#function to transform a char to an int
def char_to_int(input):
    if len(input) > 1:
        return 0
    else:
        input = input.lower()
        output = ord(input) - 96
        return output

#function to transform an int to a char
def int_to_char(input):
    input = input + 96
    output = chr(input)
    output = output.upper()
    return output

### TURN -----------------------------------
#we define the number of turns of the game
turns_number = 10



### GAME HEADER ---------------------------
def print_header():
    print("               ===[[[ BSHIP ]]]===               ")
    print("----------------Une idee braisnchat----------------")
    print("BIG AI: Where is my bship? You have only %d turns." % turns_number)
    print("LEGEND: x=miss , X=double-miss , o=ship, ø=ship-hit")
    print("---------------------------------------------------")
    #cheat
    #print("#DEBUG: Col: %s | Row: %i" % (int_to_char(ship_col), ship_row))
    print("                            __ ___ _ __ _ _ _      ")
    print("                           / - /_ ___ __ - -       ")
    print("                __________||_||____                ")
    print("~~~~~~~~~~~~~~~~\_________________/~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")


### BOARD ---------------------------------
#we initialize the board and fill it with water O
tracking_grid = []

#we define the size of the board
board_size = 6
for x in range(board_size):
    tracking_grid.append(["."] * board_size)

#we put column and row headers
alpha = {0:'+',1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I'}
for i in range(board_size):
    tracking_grid[0][0] = "+"
    tracking_grid[0][i] = alpha[i] #col
    tracking_grid[i][0] = str(i) #row

#we enhance the graphics by getting rig of that list-style
def print_board(board):
    for row in board:
        print ("  ".join(row))



### AI BSHIPS ------------------------------
#here we set the coordinates of the AI bship
def random_col(board):
    return randint(1, len(board[0]) - 1)
def random_row(board):
    return randint(1, len(board) - 1)

ship_col = random_col(tracking_grid)
ship_row = random_row(tracking_grid)


def another_turn(turn):
    if turn == turns_number-1:
        #failed because run out of turn
        print("BIG AI: You ran out of guess possibilities")
        print("BIG AI: Game Over")
        return False
    else:
        return True

#we display the guess made by the player
def print_player_guess():
    print("")
    print("PLAYER: %s:%d" % (int_to_char(guess_col), guess_row))


### MAIN -----------------------------------
#It's now the main thing, greetings to everybody!
clear()
print_header()
print_board(tracking_grid)




# 3
#MAIN LOOP STRANGERS
for turn in range(turns_number):
    print("")
    print("BIG AI: Turn", turn +1, "on", turns_number)
    print("")

    ###we ask for position to guess to the player
    #COL GUESS
    while True:
        guess_col = input("Guess Col:")   #format AaZz
        if guess_col.isalpha():
            break
        else:
            print("--- Plese, type a letter")
    guess_col = char_to_int(guess_col)

    #ROW GUESS
    while True:
        try:
            guess_row = int(input("Guess Row:"))  #format 0-9
            if type(guess_row) == int:
                break
        except ValueError:
            print("--- Please, type a number")
            continue

    if guess_row == ship_row and guess_col == ship_col:
        #success
        tracking_grid[ship_row][ship_col] = "ø"
        clear()
        print_header()
        print_board(tracking_grid)
        print_player_guess()
        print("BIG AI: NOOOO! You sunk my battleship! (on turn %s)" % (turn+1))
        break
    else:
        if guess_row <= 0 or guess_row >= board_size or guess_col <= 0 or guess_col >= board_size:
            #out of perimeter
            clear()
            print_header()
            print_board(tracking_grid)
            print_player_guess()
            print("BIG AI: Oops, that's not even in the ocean.")
        elif tracking_grid[guess_row][guess_col] == "x" or tracking_grid[guess_row][guess_col] == "X":
            #already guess
            tracking_grid[guess_row][guess_col] = "X"
            clear()
            print_header()
            print_board(tracking_grid)
            print_player_guess()
            print("BIG AI: You guessed that one already.")
        else:
            #this guess miss
            tracking_grid[guess_row][guess_col] = "x"
            clear()
            print_header()
            print_board(tracking_grid)
            print_player_guess()
            print("BIG AI: You missed my battleship!")

    if another_turn(turn) == False:
        break

    print("-------------------------")
