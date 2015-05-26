# actions.py
# The actions module contains the functions that handle important 
# actions by players during the game. 

# Used to set the boards to its initial (empty) state
def initializeBoard(board):
    for i in range(10):
        board.append([]);
        for j in range (10):
            board[i].append("~")

# Processes an attack for both players. Returns True if the shot hits;
# False otherwise. The trackingBoard parameter is optional and is used only for 
# the AI Tracking Board (the AI's board that the player sees)
def attackPosition(board, position, trackingBoard = None): 
	if trackingBoard == None:
		trackingBoard = board
	
	if board[position['row']][position['col']] == "~":
		board[position['row']][position['col']] = "*"
		trackingBoard[position['row']][position['col']] = "*"
		return False
	elif board[position['row']][position['col']].isdigit(): 
		board[position['row']][position['col']] = "X"
		trackingBoard[position['row']][position['col']] = "X"
		return True
	else:
		return None		    

# Used to check if it is safe to place a ship at a position.
# It is considered save to place a ship iff the ship will be within the
# bounsds of the board and it does not intersect with another ship. 
def isSafeToPlaceShip(board, data):
    if data['orientation'] == "h":
        if data['position']['col'] + data['size'] - 1 > 9:
            return False
        else:
            for i in range(data['size']):
                row = data['position']['row']
                col = data['position']['col'] + i
                
                if board[row][col].isdigit():
                    return False
        
        return True
    else:
        if data['position']['row'] + data['size'] - 1 > 9:
            return False
        else:
            for i in range(data['size']):
                row = data['position']['row'] + i
                col = data['position']['col']
                
                if board[row][col].isdigit():
                    return False
        
        return True
        
# Places a ship on the board. This function does not
# change what is on the screen. 
def placeShip(board, data):
    if data['orientation'] == "h":
        for i in range(data['size']):
            row = data['position']['row']
            col = data['position']['col'] + i
            
            board[row][col] = str(data['size'])
    else:
        for i in range(data['size']):
            row = data['position']['row'] + i
            col = data['position']['col']
        
            board[row][col] = str(data['size'])
