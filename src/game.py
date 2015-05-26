# game.py
# This module handles gameplay.

import os
import ui
import actions
import ai
import time
import loadsave

def playGame(saveData = None, fromLoad = False):
    os.system("clear")
    ui.printIntro()
    
    gameOver = False
    playerAttackResult = None
    aiAttackResult = None
    
    # Data
    if not fromLoad: # If True, then this is a new game
        count = 0 # No of moves it took for the player to win... if he wins ;)
        playerBoard = [] 
        aiBoard = [] # This is hidden from the player
        aiTracker = [] # This is what the player sees as the AI's board
        
        shipSizes = [5, 4, 3, 3, 2] # sizes of the ships for both players

        playerHP = 17
        aiHP = 17

        # Initialize boards
        actions.initializeBoard(playerBoard)
        actions.initializeBoard(aiBoard)
        actions.initializeBoard(aiTracker)
     
        os.system('clear')
        ui.printBoard(playerBoard, "Player")
        ui.printBoard(aiTracker, "AI")

        ai.autoPlaceShips(aiBoard, shipSizes)
        print("The AI has prepared its ships. It is now your turn to do so.")

        response = input("Do you want the computer to place the ships for you? (y or n) ").strip()
        if response == 'y':
            ai.autoPlaceShips(playerBoard, shipSizes)
        else:
            # Manual placement of ships. 
            isOk = 'n'
            while isOk != 'y':
                for i in shipSizes:
                    os.system('clear')
                    ui.printBoard(playerBoard, "Player")
                    ui.printBoard(aiTracker, "AI")
                    
                    print("Follow the instructions in placing your ships")
                    
                    data = ui.getShipData(i)
                    
                    if data == 'q':
                        return None
                    
                    while not actions.isSafeToPlaceShip(playerBoard, data):
                        print("You cannot place a ship there. It will either be out of bounds or intersect with other ships.")
                        data = ui.getShipData(i)
                    
                    actions.placeShip(playerBoard, data)
                    
                isOk = input("Is this layout what you want? (y or n) ")
                if isOk == 'n':
                    playerBoard = []
                    actions.initializeBoard(playerBoard)
                
    else: # We will load data from a previous game
        count = saveData['count']
        playerBoard = saveData['playerBoard'] 
        aiBoard = saveData['aiBoard'] 
        aiTracker = saveData['aiTracker']
        playerHP = saveData['playerHP']
        aiHP = saveData['aiHP']
    
    # Game loop
    while not gameOver:
        os.system('clear')
        ui.printBoard(playerBoard, "Player")
        ui.printBoard(aiTracker, "AI")
        
        ui.printGameStatus(playerHP, aiHP, playerAttackResult, aiAttackResult)
        
        position = ui.getPosition()
        
        # Save data and quit
        if position == 'q':
            gameData = {}
            gameData['playerHP'] = playerHP
            gameData['aiHP'] = aiHP
            gameData['playerBoard'] = playerBoard
            gameData['aiBoard'] = aiBoard
            gameData['aiTracker'] = aiTracker
            gameData['count'] = count

            loadsave.saveToFile("game_data.json", gameData)
            input("Game data saved. Press enter to continue.")
            
            return None #No result. 
        
        #Player did not enter a valid position
        while position == None:
	        position = ui.getPosition()
        
        # Player attack
        playerAttackResult = actions.attackPosition(aiBoard, position, aiTracker)
        
        while playerAttackResult == None:
	        print("You have attacked that position before.")
	        position = ui.getPosition()
	        while position == None:
		        position = ui.getPosition()
		        
	        playerAttackResult = actions.attackPosition(aiBoard, position, aiTracker)
        
        os.system('clear')
        ui.printBoard(playerBoard, "Player")
        ui.printBoard(aiTracker, "AI")
        
        ui.printGameStatus(playerHP, aiHP, playerAttackResult, aiAttackResult)
        	
        print("The AI will now attack")
        time.sleep(0.8)
        aiAttackResult = ai.autoAttackPosition(playerBoard)
        
        count += 1
        
        if playerAttackResult: # player hit the ai  
            aiHP -= 1
            if aiHP == 0:
                gameOver = True	
        
        if aiAttackResult: # ai hit the player
            playerHP -= 1
            if playerHP == 0:
                gameOver = True	

    os.system('clear')
    ui.printBoard(playerBoard, "Player")
    ui.printBoard(aiBoard, "AI")
    
    # Check who wins
    if playerHP == 0:
        print("You lost to a computer :(")
        return 0 #lost
    else:
        print("You won! :D")
        return count #win
