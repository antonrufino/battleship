# battleship.py
# This is the main module and the script that must be run 
# by the user. 

import os
import ui
import game
import loadsave

# In the case that the user won, this checks if the user has a new high score. 
def processGameResult(result):
    if result != None:
        if result > 0:
            print("It took you ", result, "moves!")
            username = input("What's your name? This might be a new high score. ")
            highScores = loadsave.loadFromFile("high_scores.json")
            
            if username in highScores:
                if highScores[username] > result:
                    print("It's a new high score! Congratulations")
                    highScores[username] = result
                else: 
                    print("It's not a new high score. You current high score is", highScores[username])
            else:
                print("It's you first game. Of course it's a high score :D")
                highScores[username] = result
            
            loadsave.saveToFile("high_scores.json", highScores)
        input("Press enter to continue... ")

#Main loop

choice = 0
while choice != 5:
    os.system('clear')
    ui.printMenu()
    
    try: # did user enter a number? 
        choice = int(input("Enter your choice: "))
    except ValueError: # i guess not :(
        print("Not a valid choice.")
        input("Press enter to continue... ")
        
    if choice == 1:
        result = game.playGame()
        processGameResult(result)                 
    elif choice == 2:
        saveData = loadsave.loadFromFile("game_data.json")
        
        if len(saveData) > 0: #is there save data?  
            result = game.playGame(saveData, True)
            processGameResult(result)
        else:
            print("No saved game.")
            input("Press enter to continue...")
    elif choice == 3:
        os.system("clear")
        highScores = loadsave.loadFromFile("high_scores.json")
        ui.printHighScores(highScores)
        input("Press enter to return to main menu... ")
    elif choice == 4:
        os.system("clear")
        ui.printCredits()
    elif choice == 5: 
        break
    else: 
        print("Not a valid choice.")
        input("Press enter to continue... ")
