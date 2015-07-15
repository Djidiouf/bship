# -------------------------------------------------------------------------------
# Name:         bship
# Purpose:      a game without limits
#
# Author:       Djidiouf
#
# Created:      2015-06-29
# Licence:      bchat-licence
# -------------------------------------------------------------------------------

# import
from random import randint  # used with random_row and random_col
import os  # use with clear function


# we try to clear the terminal at the beginning of each turn
def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posif':
        os.system('clear')
    else:
        print("NOTICE: OS unknown, an attempt to clear the window cannot be made")


# function to transform a char to an int
def char_to_int(input):
    if len(input) > 1:
        return 0
    else:
        input = input.lower()
        output = ord(input) - 96
        return output


# function to transform an int to a char
def int_to_char(input):
    input = input + 96
    output = chr(input)
    output = output.upper()
    return output


### GAMEPLAY VARIABLES --------------------
turns_number = 10  # we define the number of turns of the game
grid_size = 6  # we define the size of the board (MAX 11)
ships_number = 1  # number of ships on each side


### GRID INITIALIZATION -------------------
def grid_init(grid, grid_size):
    for x in range(grid_size):
        grid.append(["."] * grid_size)
    # we put column and row headers
    col_header = {0: '+', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}
    row_header = {0: '+', 1: ' 1', 2: ' 2', 3: ' 3', 4: ' 4', 5: ' 5', 6: ' 6', 7: ' 7', 8: ' 8', 9: ' 9', 10: '10'}

    for i in range(grid_size):
        grid[0][0] = " +"
        grid[0][i] = col_header[i]  # col
        grid[i][0] = row_header[i]  # row


### GAME HEADER ---------------------------
def print_header():
    print("               ===[[[ BSHIP ]]]===               ")
    print("----------------Une idee braisnchat----------------")
    print("ENEMY : Where is my bship? You have only: %d turns." % turns_number)
    print("LEGEND: x=miss , X=double-miss , O=ship, Q=ship-hit")
    print("Tracking=Player's Ship         Primary=Enemy's Ship")
    print("---------------------------------------------------")
    # cheat
    print(">>> DEBUG >>>")
    print("Bships of the enemy: ", enemy_ships)
    print("--Enemy Grid--")
    print_grid(enemy_grid)
    print("<<< DEBUG <<<")
    # print("                            __ ___ _ __ _ _ _      ")
    # print("                           / - /_ ___ __ - -       ")
    # print("                __________||_||____                ")
    # print("~~~~~~~~~~~~~~~~\_________________/~~~~~~~~~~~~~~~~")
    print("")


### GRIDS -------------------------
# we initialize our three grids and fill them with water and nice headers.
# TRACKING GRID
tracking_grid = []
grid_init(tracking_grid, grid_size)

# PRIMARY GRID
primary_grid = []
grid_init(primary_grid, grid_size)

# ENEMY GRID
# this one is not displayed to the player
enemy_grid = []
grid_init(enemy_grid, grid_size)


# we enhance the graphics of board in input and get rig of that list-style
def print_grid(grid):
    for row in grid:
        print("  ".join(row))


### AI BSHIPS ------------------------------
# here we set the coordinates of the AI bships
def random_col(grid):
    return randint(1, len(grid[0]) - 1)


def random_row(grid):
    return randint(1, len(grid) - 1)


enemy_ships = []

for i in range(ships_number):
    # we also want to avoid duplicates
    while True:
        enemy_ship_col = random_col(primary_grid)
        enemy_ship_row = random_row(primary_grid)
        random_col_row = (enemy_ship_col, enemy_ship_row)

        if (enemy_ship_col, enemy_ship_row) not in enemy_ships:
            enemy_ships.append((enemy_ship_col, enemy_ship_row))

            # we assign the enemy's bship on the enemy_grid
            enemy_grid[enemy_ship_row][enemy_ship_col] = 'O'

            break


# are we running out of guess allowed?
def another_turn(turn):
    if turn == turns_number - 1:
        # failed because run out of turn
        print("BIG AI: You ran out of guess possibilities")
        print("BIG AI: Game Over")
        return False
    else:
        return True




# Display the two grids updated
def print_grids_presentation():
    clear()
    print_header()
    print("--Tracking Grid--")
    print_grid(tracking_grid)
    print("")
    print("==Primary  Grid==")
    print_grid(primary_grid)

# Display the guess made by the player and the enemy
def print_guess():
    print("")
    print("PLAYER: %s:%d" % (int_to_char(player_guess_col), player_guess_row))
    print("ENEMY : %s:%d" % (int_to_char(enemy_guess_col), enemy_guess_row))

# Display notifications
def notif_total_win():
    print("ENEMY : NOOOO! You sunk all my battleships! (on turn %s)" % (turn + 1))
def notif_partial_win():
    print("ENEMY : NO! You sunk one of my battleship! (on turn %s)" % (turn + 1))
def notif_miss_twice():
    print("ENEMY : You guessed that one already.")
def notif_miss():
    print("ENEMY : You missed my battleship!")

def print_notifications(number):
    notifications = {
        'total_win' : notif_total_win,
        'partial_win' : notif_partial_win,
        'already_miss' : notif_miss_twice,
        'miss' : notif_miss,
    }
    result = notifications.get(number, 'Error')
    return result()



### MAIN #############################################################################
# It's now the main thing, greetings to everybody!
clear()
print_header()

### PLAYER SHIP -------------------------------
print("--Tracking Grid--")
print_grid(tracking_grid)
print("")

###we ask for player ship position
print("Where are your ship?")
# PLAYER SHIP COL
while True:
    player_ship_col = input("Player Ship Col:")  # format AaZz
    if player_ship_col.isalpha() and char_to_int(player_ship_col) < grid_size:
        break
    else:
        print("--- Please, type a letter inferior to %s" % int_to_char(grid_size))
player_ship_col = char_to_int(player_ship_col)

# PLAYER SHIP ROW
while True:
    player_ship_row = int(input("Player Ship Row:"))  # format 0-9
    if type(player_ship_row) == int and player_ship_row < grid_size:
        break
    else:
        print("--- Please, type a number inferior to %d" % grid_size)
tracking_grid[player_ship_row][player_ship_col] = "O"


### MAIN LOOP -------------------------------
print_grids_presentation()

for turn in range(turns_number):
    print("")
    print("BIG AI: Turn", turn + 1, "on", turns_number)
    print("")

    ###PLAYER GUESS ---------------------------------
    ###we ask for position to guess to the player
    print("Where do you launch at your missile?")
    # COL GUESS
    while True:
        player_guess_col = input("Guess Col:")  # format AaZz
        if player_guess_col.isalpha() and char_to_int(player_guess_col) < grid_size:
            break
        else:
            print("--- Please, type a letter inferior to %s" % int_to_char(grid_size))
    player_guess_col = char_to_int(player_guess_col)

    # ROW GUESS
    while True:
        player_guess_row = int(input("Guess Row:"))  # format 0-9
        if type(player_guess_row) == int and player_guess_row < grid_size:
            break
        else:
            print("--- Please, type a number inferior to %d" % grid_size)

    # we add those two guess in a tuple
    player_guess = (player_guess_col, player_guess_row)
    print("player guess =", player_guess)

    ###ENEMY GUESS ---------------------------------
    enemy_guess_col = random_col(tracking_grid)
    enemy_guess_row = random_row(tracking_grid)

    ###TURN RESOLUTION ######################################
    ##PLAYER TURN RESOLUTION ------------
    notif_msg = 0

    if player_guess in enemy_ships:
        # success
        primary_grid[player_guess_row][player_guess_col] = "Q"
        # we retrieve the index of the tuple guessed and delete it
        enemy_ships.pop(enemy_ships.index(player_guess))
        notif_msg = 'partial_win'

        # if enemy_ships is empty , there is nothing more to do
        if len(enemy_ships) == 0:
            print_grids_presentation()
            print_guess()
            print_notifications('total_win')
            break
    else:
        if primary_grid[player_guess_row][player_guess_col] == "x" or primary_grid[player_guess_row][player_guess_col] == "X":
            # already guess
            primary_grid[player_guess_row][player_guess_col] = "X"
            notif_msg = 'already_miss'
        else:
            # this guess miss
            primary_grid[player_guess_row][player_guess_col] = "x"
            notif_msg = 'miss'

    print_grids_presentation()
    print_guess()
    print_notifications(notif_msg)

    ##ENEMY TURN RESOLUTION ------------
    if enemy_guess_row == player_ship_row and enemy_guess_col == player_ship_col:
        # success
        tracking_grid[player_ship_row][player_ship_col] = "Q"
        print_grids_presentation()
        print_guess()
        print("ENEMY : HAHAHA! I sunk your battleship! (on turn %s)" % (turn + 1))
        break
    else:
        if tracking_grid[enemy_guess_row][enemy_guess_col] == "x" or tracking_grid[enemy_guess_row][enemy_guess_col] == "X":
            # already guess
            tracking_grid[enemy_guess_row][enemy_guess_col] = "X"
            print_grids_presentation()
            print_guess()
            print("ENEMY : I guessed that one already.")
        else:
            # this guess miss
            tracking_grid[enemy_guess_row][enemy_guess_col] = "x"
            print_grids_presentation()
            print_guess()
            print("ENEMY : I missed your battleship!")

    if another_turn(turn) == False:
        break

    print("---------------------------------------------------")
