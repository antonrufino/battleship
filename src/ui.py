# ui.py
# This module handles asking for input from the user and printing data 
# and other text. 

import time

def printMenu():

    # ASCII art made using FIGlet. 
    print(" ____        _   _   _           _     _               _   ___  ")
    print("| __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __   __   _/ | / _ \ ") 
    print("|  _ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \  \ \ / / || | | |")
    print("| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |  \ V /| || |_| |")
    print("|____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/    \_/ |_(_)___/ ")
    print("                                        |_|                     ")
    
    print("[1] New Game")
    print("[2] Load Game")
    print("[3] High Scores")
    print("[4] Credits")
    print("[5] Exit")

def printCredits():
    print("Battleship v1.0")
    print("Battleship AI v2.0 \"Archer\"")
    print()
    print("This game was made by Manuel Antonio P. Rufino")
    print("In partial fulfillment of the requirements of CMSC 11")
    print()
    print("My sincerest thanks go to those who helped in testing the game and giving suggestions.")
    print()
    input("Press enter to return to main menu...\n")
    
# Prints a board (2x2 list) with a label
def printBoard(board, label):
    print(label)
    
    print("  0 1 2 3 4 5 6 7 8 9")
    for i in range(10):
        print(i, " ".join(board[i]))
    
    print()    

# Asks for a position from the user.        
def getPosition():
    data = input("Enter row and column of target separated by a space (e.g. 5 0). Enter 'q' to quit the game ").strip()
    
    if data == 'q': # Player chose to quit
        return 'q'
    
    data = data.split(" ")
    
    position = {}
    
    if len(data) != 2: # Player didn't use the write format.
        print("Write only row and column.")
        return None
        
    try: # Ensures that only valid numbers are entered. 
        position['row'] = int(data[0])
        position['col'] = int(data[1])
        
        if position['row'] < 0 or position['row'] > 9:
            print("Only numbers from 0 to 9 are allowed.")
            return None
        elif position['col'] < 0 or position['col'] > 9:
            print("Only numbers from 0 to 9 are allowed.")
            return None
    except ValueError:
        print("Only numbers are allowed.")
        return None
    
    return position
    
    
def getShipData(shipSize):
    print("This ship is of size", shipSize)
    
    data = {}
    
    data["size"] = shipSize
    
    data['orientation'] = input("Should ship be vertical or horizontal? (v or h) ").strip()
    while data['orientation'] != 'v' and data['orientation'] != 'h':
        print("Enter v or h only.")
        data['orientation'] = input("Should ship be vertical or horizontal? (v or h) ").strip() 
    
    data['position'] = getPosition()
    
    if data['position'] == 'q':
        return 'q'
    
    while data['position'] == None:
        data['position'] = getPosition()
    
    return data
    
def printIntro():
    print("Initializing game boards...")
    time.sleep(1.5)
    print("COMPLETE")
    
    print("Initializing Battleship AI \"Archer\"...")
    time.sleep(1.5)
    print("COMPLETE")
    time.sleep(1)

def printGameStatus(playerHP, aiHP, playerAttackResult, aiAttackResult):
    print("LEGEND")
    print("~ - Untargeted Tile")
    print("* - Miss")
    print("X - Hit")
    print("5, 4, 3, or 2 - Your ships")
    print()
    
    print("GAME STATUS")
    print("Player HP:", playerHP)
    print("AI HP:", aiHP)
    print()
    
    if playerAttackResult == True:
        print("You were able to hit a ship.")
    elif playerAttackResult == False:
        print("You missed.")
    if aiAttackResult == True:
        print("The AI hit one of your ships.")
    elif aiAttackResult == False:
        print("The AI missed.")
    
    print("It is your turn to attack.")
    
def printHighScores(highScores):
    print("HIGH SCORES\n")
    for k, v in highScores.items():
        print(k, v)
