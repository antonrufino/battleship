import random
import actions

# Attack data
initialHit = {}
possibleHorizontalPositions = []
possibleVerticalPositions = []
orientation = None

def createRandomPosition():
    position = {}
    position['row'] = random.randint(0, 9)
    position['col'] = random.randint(0, 9)

    return position

def createRandomShipData(size):
    data = {}
    data['size'] = size

    if random.randint(0, 1):
        data['orientation'] = 'h'
    else:
        data['orientation'] = 'v'

    data['position'] = createRandomPosition()

    return data

def autoPlaceShips(board, shipSizes):
    for i in shipSizes:
        data = createRandomShipData(i)
        while not actions.isSafeToPlaceShip(board, data):
            data = createRandomShipData(i)

        actions.placeShip(board, data)

#Added proximity as an argument for testing purposes.
def autoAttackPosition(board, trackingBoard = None):
    global orientation
    global initialHit

    if orientation == None:
        position = createRandomPosition()

        attackResult = actions.attackPosition(board, position, trackingBoard)
        while attackResult == None:
            position = createRandomPosition()
            attackResult = actions.attackPosition(board, position, trackingBoard)

        if attackResult:
            initialHit = position
            generatePossiblePositions(board, initialHit)
            orientation = 'h'
            return True
        else:
            return False
    elif orientation == 'h':
        if len(possibleHorizontalPositions) == 0:
            orientation = 'v'
            return autoAttackPosition(board)

        target = possibleHorizontalPositions.pop()
        attackResult = actions.attackPosition(board, target, trackingBoard)

        if attackResult:
            generatePossiblePositions(board, target)
            return True
        else:
            return False
    elif orientation == 'v':
        if len(possibleVerticalPositions) == 0:
            orientation = None
            return autoAttackPosition(board)

        target = possibleVerticalPositions.pop()
        attackResult = actions.attackPosition(board, target, trackingBoard)

        if attackResult:
            generatePossiblePositions(board, target)
            return True
        else:
            return False

def isPossiblePosition(board, row, col):
    if row < 0 or row > 9:
        return False
    elif col < 0 or col > 9:
        return False
    elif board[row][col] == "X" or board[row][col] == "*":
        return False
    else:
        return True

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
