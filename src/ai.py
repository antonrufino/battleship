# ai.py
# This is the game's AI module. It handles all actions taken by 
# the AI.

'''
THE AI'S STRATEGY FOR WINNING

The AI will randomly select a tile from one of the spots those marked 
with an X below. This increases the probability of hitting a ship.
(The idea was by Carl Caracas, the code for the doing so however is my creation. 
Promise, honest to.) 

~ X ~ X ~ X
X ~ X ~ X ~
~ X ~ X ~ X
X ~ X ~ X ~
~ X ~ X ~ X
X ~ X ~ X ~

Upon hitting a ship, it will target those tiles horizontally adjacent
to the initial hit in the next turns. If there is no hit, it will then target
the vertically adjacent tiles. It will continue to do this until the ship has been sunk. 
It will then return to attacking randomly as described above. 
'''
import random
import actions

# Attack data
initialHit = {} # This stores the position of the first hit on a ship
possibleHorizontalPositions = [] # This stores the possible horizontal positions of other parts of a ship after the initial hit
possibleVerticalPositions = [] # This stores the possible vertical positions of other parts of a ship after the initial hit
orientation = None # This stores the orientation of the enemy ship.
shotCount = 0 

# Creates a random position for use by the AI
def createRandomPosition():
    global shotCount    
    
    position = {}
    position['row'] = random.randint(0, 9)
    position['col'] = random.randint(0, 9)
    
    # There are cases where the AI will use up all the tiles it can
    # target (as describe in its strategy) which can result in an infinite loop.
    # The if-else statement below prevents that from happening. 
    if shotCount < 50:
        while position['row'] % 2 != position['col'] % 2:
            position['col'] = random.randint(0, 9)
    else: 
        while position['row'] % 2 == position['col'] % 2:
            position['col'] = random.randint(0, 9)
            
    return position

# This creates random ship data for a ship of a given size. 
# The ship data represents a ship and its relevant properties
# like orientation and its position. This is used in placing the ships. 
def createRandomShipData(size):
    data = {}
    data['size'] = size
    
    if random.randint(0, 1):
        data['orientation'] = 'h'
    else:
        data['orientation'] = 'v'
            
    data['position'] = createRandomPosition()
    
    return data

# Generates a random placement of ships. This is also used
# when the player chooses the auto place ships option at the 
# start of the game. 
def autoPlaceShips(board, shipSizes):
    for i in shipSizes:
        data = createRandomShipData(i)
        while not actions.isSafeToPlaceShip(board, data):
            data = createRandomShipData(i)
        
        actions.placeShip(board, data)   
 
# This handles attacking by the AI        
def autoAttackPosition(board, trackingBoard = None):
    global orientation
    global initialHit
    global shotCount
    
    if orientation == None: # In this case, no ship has been spotted yet
        position = createRandomPosition()
        
        attackResult = actions.attackPosition(board, position, trackingBoard)
        while attackResult == None:
            position = createRandomPosition()
            attackResult = actions.attackPosition(board, position, trackingBoard)  
        
        shotCount += 1
                    
        if attackResult: # A ship has been hit   
            initialHit = position
            generatePossiblePositions(board, initialHit)
            orientation = 'h' # Tells the AI that horizontal positions will be checked. 
            return True
        else: # Shot missed       
            return False
    elif orientation == 'h': # If this is True, the AI will target horizontal positions   
        # If True, it is not possible that the other parts of the ship are beside the initial hit.
        # The AI will target the vertical positions instead. 
        if len(possibleHorizontalPositions) == 0: # 
            orientation = 'v'
            return autoAttackPosition(board)
            
        target = possibleHorizontalPositions.pop() # Choose one of the possible positions       
        attackResult = actions.attackPosition(board, target, trackingBoard)
        
        # Prevents infinite loops
        if target['row'] % 2 == target['col'] % 2:
            shotCount += 1
            
        if attackResult:
            generatePossiblePositions(board, target) # Updates list to target position next to successful shot
            return True
        else:        
            return False
    elif orientation == 'v': # If this is True, the AI will target vertical position
        # Since execution will only reach this point if the horizontal positions have been checked, 
        # then if this condition is true, it means that there are no more possible positions for the other parts
        # of the ship and that the ship has been sunk. The AI will return to random targeting. 
        if len(possibleVerticalPositions) == 0: 
            orientation = None           
            return autoAttackPosition(board)
                
        target = possibleVerticalPositions.pop()
        attackResult = actions.attackPosition(board, target, trackingBoard)
        
        if target['row'] % 2 == target['col'] % 2:
            shotCount += 1
            
        if attackResult:
            generatePossiblePositions(board, target)
            return True
        else:        
            return False

# Checks if it is possible for part of a ship to be on
# a given tile. 
def isPossiblePosition(board, row, col):
    if row < 0 or row > 9:
        return False
    elif col < 0 or col > 9:
        return False
    elif board[row][col] == "X" or board[row][col] == "*":
        return False
    else:
        return True

# Generates list of possible positions for other parts of an enemy ship. 
def generatePossiblePositions(board, position):
    checkRow = True
    checkCol = True
    
    if orientation == 'h':
        checkRow = False
    elif orientation == 'v':
        checkCol = False
    
    if checkRow:
        if isPossiblePosition(board, position['row'] - 1, position['col']):
            possiblePosition = {}
            possiblePosition['row'] = position['row'] - 1  
            possiblePosition['col'] = position['col']
            
            possibleVerticalPositions.append(possiblePosition)
            
        if isPossiblePosition(board, position['row'] + 1, position['col']):
            possiblePosition = {}
            possiblePosition['row'] = position['row'] + 1  
            possiblePosition['col'] = position['col']
            
            possibleVerticalPositions.append(possiblePosition)
            
    if checkCol:
        if isPossiblePosition(board, position['row'], position['col'] - 1):
            possiblePosition = {}
            possiblePosition['row'] = position['row']  
            possiblePosition['col'] = position['col'] - 1 
            
            possibleHorizontalPositions.append(possiblePosition)
            
        if isPossiblePosition(board, position['row'], position['col'] + 1):
            possiblePosition = {}
            possiblePosition['row'] = position['row']  
            possiblePosition['col'] = position['col'] + 1
        
            possibleHorizontalPositions.append(possiblePosition)   
