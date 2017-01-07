
# five camels of different colors
# each camel can move between 1-3 spaces
# camels on same space are stacked on top of one another
# if a camel is on top of a camel being moved, it is moved as well
# camels on top are considered in front of camels below

# 1) input board
# 2) get expected results


# represent board as a list of lists
# each list is a space and then each list is a stack of camels
import copy
import collections
import itertools

# orange 0
# yellow 1
# green 2
# blue 3
# white 4

def initBoard():
    game_board = []
    for i in range(99):
        game_board.append([])
    game_board[0] = ["orange","yellow","green","blue","white"]
    game_board[1] = []
    game_board[2] = []
    game_board[3] = []
    game_board[4] = []
    game_board[5] = []
    game_board[6] = []
    game_board[7] = []
    game_board[8] = []

    #game_board[2] = [4,3]


    oasisIndexes = [99]
    desertIndexes = [99]

    return game_board, oasisIndexes, desertIndexes

def findCurrentLocationOfPiece(boardState, boardpiece):
    c = boardpiece #number of board piece
    initSpotIndexes = next(((i, color.index(c)) for i, color in enumerate(boardState) if c in color), None)
    return initSpotIndexes

def moveAPiece(game_board,oasisIndexes, desertIndexes,boardpiece,rollAmount):
    # get current location
    initSpotIndexes = findCurrentLocationOfPiece(game_board,boardpiece)
    # save piece + camels on back to temp variable
    a = initSpotIndexes[0]
    b = initSpotIndexes[1]
    camelStack = game_board[a][b:]
    # remove elements from initial spot list
    for camel in camelStack:
        game_board[a].remove(camel)

    # add elements to final spot list
    newSpotIndex = a + rollAmount
    if newSpotIndex in oasisIndexes:
        game_board[newSpotIndex+1].extend(camelStack)
    elif newSpotIndex in desertIndexes:
        camelStack.extend(game_board[newSpotIndex-1])
        game_board[newSpotIndex-1] = camelStack
    else:
        game_board[newSpotIndex].extend(camelStack)

    return game_board

def getRank(allBoardStates):
    #flatten List of lists
    listOfRankedLists=[]
    for j in range(len(allBoardStates)):
        game_board = allBoardStates[j]
        localFlattened = flattenBoard(game_board)
        localFlattened.reverse()
        listOfRankedLists.append(localFlattened)
    return listOfRankedLists

def flattenBoard(list_of_lists):
    #http://stackoverflow.com/questions/11264684/flatten-list-of-lists
    flattened = []
    for sublist in list_of_lists:
        for val in sublist:
            flattened.append(val)
    return flattened

def runMovesAndRecordBoards(initialGameBoard,oasisIndexes, desertIndexes, allOrderOfColors, allRolls):
    #input Moves
    allBoardStates = []
    q = 0
    for orderElement in allOrderOfColors:
        for rollElement in allRolls:
            local_game_board = copy.deepcopy(initialGameBoard)
            for i in range(len(rollElement)):
                local_game_board = moveAPiece(local_game_board,oasisIndexes, desertIndexes,orderElement[i],rollElement[i])
            q += 1
            # print("local board")
            # print(local_game_board)
            allBoardStates.append(copy.deepcopy(local_game_board))
            # print("all boards")
            # print(allBoardStates)
        print("%d possibilities calculated" % q)
    #output List of game boardState
    return allBoardStates

def generateMoves():
    piecesInPlay = ["orange","yellow","green","blue","white"]
    allOrderOfColors = list(itertools.permutations(piecesInPlay))
    #generates [(0, 1, 2, 3, 4), (0, 1, 2, 4, 3), (0, 1, 3, 2, 4), (0, 1, 3, 4, 2), (0, 1, 4, 2, 3), (0, 1, 4, 3, 2)...]
    #allOrderOfColors = [[0,1,2,3,4],[0,1,2,3,4]]
    #allOrderOfColors = [(0, 1, 2, 3, 4), (0, 1, 2, 4, 3), (0, 1, 3, 2, 4), (0, 1, 3, 4, 2), (0, 1, 4, 2, 3)]
    allRolls = set(list(itertools.permutations([1,2,3]*5, len(piecesInPlay))))
    # [(1, 2, 3, 1, 2), (1, 2, 3, 1, 3), (1, 2, 3, 1, 1), (1, 2, 3, 1, 2)...]
    #allRolls = [[1,2,1,3,2],[1,2,1,3,2]]
    #allRolls = [(1, 2, 3, 1, 2), (1, 2, 3, 1, 3), (1, 2, 3, 1, 1), (1, 2, 3, 1, 2)]

    return allOrderOfColors, allRolls

def summarizeRanks(listOfRankedLists):
    firstPositionList = [item[0] for item in listOfRankedLists]
    firstCounter = collections.Counter(firstPositionList)
    print("First Place:")
    print(firstCounter)

    secondPositionList = [item[1] for item in listOfRankedLists]
    secondCounter = collections.Counter(secondPositionList)
    print("And Second Place:")
    print(secondCounter)

    return firstCounter, secondCounter

def makePlots(firstCounter,secondCounter):
    from collections import Counter
    import numpy as np
    import matplotlib.pyplot as plt


    labels, values = zip(*firstCounter.items())
    labels2, values2 = zip(*secondCounter.items())

    indexes = np.arange(len(labels))
    indexes2 = np.arange(len(labels2))
    width = 1

    # plt.bar(indexes, values, width)
    # plt.xticks(indexes + width * 0.5, labels)
    # plt.show()

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    #plt.xticks(indexes + width * 0.5, labels)
    ax1.bar(indexes, values, width)
    ax1.set_title('First Place')



    #plt.xticks(indexes2 + width * 0.5, labels2)
    ax2.bar(indexes2, values2, width)
    ax2.set_title('Second Place')
    plt.show()


#Main
initialGameBoard, oasisIndexes, desertIndexes = initBoard()
a = flattenBoard(initialGameBoard)
print(a)


allOrderOfColors, allRolls = generateMoves()
# print(initialGameBoard)
# print(allOrderOfColors)
# print(allRolls)
allBoardStates = runMovesAndRecordBoards(initialGameBoard, oasisIndexes, desertIndexes, allOrderOfColors, allRolls)

#game_board = moveAPiece(game_board,4,1)
#print(game_board)

# print(allBoardStates)
listOfRankedLists = getRank(allBoardStates)
#print(listOfRankedLists)
firstCounter, secondCounter = summarizeRanks(listOfRankedLists)
makePlots(firstCounter,secondCounter)
# print(b)
