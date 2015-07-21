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
def char_to_int(x):
    if len(x) > 1:
        return 0
    else:
        x = x.lower()
        output = ord(x) - 96
        return output


# function to transform an int to a char
def int_to_char(x):
    x = x + 96
    output = chr(x)
    output = output.upper()
    return output


### GAMEPLAY VARIABLES --------------------
turns_number = 10  # we define the number of turns of the game
grid_size = 6  # we define the size of the board (MAX 11)
ships_number = 2  # number of ships on each side

enemy_ships = []  # Coordinates of Enemy's ships
player_ships = []  # Coordinates of Player's ships

enemy_guess_tried = [] # Coordinates tried by the Enemy


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
    print("Bships of the enemy : ", enemy_ships)
    print("Bships of the player: ", player_ships)
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
    print("ENEMY : NO! You sunk one of my battleships! (on turn %s)" % (turn + 1))


def notif_player_miss():
    print("ENEMY : You missed my battleship!")


def notif_total_lose():
    print("ENEMY : HAHAHA! I sunk all your battleships! (on turn %s)" % (turn + 1))


def notif_partial_lose():
    print("ENEMY : YEAH! I sunk one of your battleships! (on turn %s)" % (turn + 1))


def notif_enemy_miss():
    print("ENEMY : I missed your battleship!")


def print_notifications(msg):
    notifications = {
        'total_win': notif_total_win,
        'partial_win': notif_partial_win,
        'player_miss': notif_player_miss,
        'total_lose': notif_total_lose,
        'partial_lose': notif_partial_lose,
        'enemy_miss': notif_enemy_miss,
    }
    result = notifications.get(msg, lambda: 'Error')
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
print("Where are your %i ship(s)?" % (ships_number))

for i in range(ships_number):
    # we also want to avoid duplicates
    while True:
        # PLAYER SHIP COL
        while True:
            try:
                player_ship_col = input("Player Ship Col:")  # format AaZz
                if len(player_ship_col) == 1 and player_ship_col.isalpha() and char_to_int(player_ship_col) < grid_size:
                    break
                else:
                    print("--- Please, type a letter inferior to %s" % int_to_char(grid_size))
            except ValueError:
                print("--- Please, type a letter inferior to %s" % int_to_char(grid_size))
                continue
        player_ship_col = char_to_int(player_ship_col)

        # PLAYER SHIP ROW
        while True:
            try:
                player_ship_row = int(input("Player Ship Row:"))  # format 0-9
                if player_ship_row < grid_size:
                    break
                else:
                    print("--- Please, type a number inferior to %d" % grid_size)
            except ValueError:
                print("--- Please, type a number inferior to %d" % grid_size)
                continue

        if (player_ship_col, player_ship_row) not in player_ships:
            player_ships.append((player_ship_col, player_ship_row))

            # we assign the player's bship on the player_grid
            tracking_grid[player_ship_row][player_ship_col] = 'O'
            break

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
        try:
            player_guess_col = input("Guess Col:")  # format AaZz
            if len(player_guess_col) == 1 and player_guess_col.isalpha() and char_to_int(player_guess_col) < grid_size:
                break
            else:
                print("--- Please, type a letter inferior to %s" % int_to_char(grid_size))
        except ValueError:
            print("--- Please, type a letter inferior to %s" % int_to_char(grid_size))
            continue
    player_guess_col = char_to_int(player_guess_col)

    # ROW GUESS
    while True:
        try:
            player_guess_row = int(input("Guess Row:"))  # format 0-9
            if player_guess_row < grid_size:
                break
            else:
                print("--- Please, type a number inferior to %d" % grid_size)
        except ValueError:
            print("--- Please, type a number inferior to %d" % grid_size)
            continue

    # we add those two guess in a tuple
    player_guess = (player_guess_col, player_guess_row)
    print("player guess =", player_guess)

    ###ENEMY GUESS ---------------------------------
    #the enemy need to guess coordinates that he never guessed before
    while True:
        try:
            enemy_guess_col = random_col(tracking_grid)
            enemy_guess_row = random_row(tracking_grid)
            if (enemy_guess_col, enemy_guess_row) not in enemy_guess_tried:
                # we log those coordinates for future purpose
                enemy_guess_tried.append((enemy_guess_col, enemy_guess_row))
                # we assign those to the current guess
                enemy_guess = (enemy_guess_col, enemy_guess_row)
                break
        except ValueError:
            continue

    print("ENEMY: --- I tried : ", enemy_guess_tried)


    ###TURN RESOLUTION ######################################
    ##PLAYER TURN RESOLUTION ------------
    notif_msg_player_turn = 0
    notif_msg_enemy_turn = 0

    if player_guess in enemy_ships:
        # player success
        primary_grid[player_guess_row][player_guess_col] = "Q"
        # we retrieve the index of the tuple guessed and delete it
        enemy_ships.pop(enemy_ships.index(player_guess))
        notif_msg_player_turn = 'partial_win'

        # if enemy_ships is empty , there is nothing more to do
        if len(enemy_ships) == 0:
            print_grids_presentation()
            print_guess()
            print_notifications('total_win')
            break
    else:
        # this guess miss
        primary_grid[player_guess_row][player_guess_col] = "x"
        notif_msg_player_turn = 'player_miss'

    ##ENEMY TURN RESOLUTION ------------
    if enemy_guess in player_ships:
        # enemy success
        tracking_grid[enemy_guess_row][enemy_guess_col] = "Q"
        # we retrieve the index of the tuple guessed and delete it
        player_ships.pop(player_ships.index(enemy_guess))
        notif_msg_enemy_turn = 'partial_lose'

        # if player_ships is empty , there is nothing more to do
        if len(player_ships) == 0:
            print_grids_presentation()
            print_guess()
            print_notifications(notif_msg_player_turn)
            print_notifications('total_lose')
            break
    else:
        # this guess miss
        tracking_grid[enemy_guess_row][enemy_guess_col] = "x"
        notif_msg_enemy_turn = 'enemy_miss'

    print_grids_presentation()
    print_guess()
    print_notifications(notif_msg_player_turn)
    print_notifications(notif_msg_enemy_turn)

    if another_turn(turn) == False:
        break

    print("---------------------------------------------------")
