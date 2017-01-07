class GameBoard(object):

    def __init__(self):
        import copy
        import collections
        import itertools

        self.spots = []
        #16 spots for game play plus one spot for winner
        for i in range(17):
            self.spots.append([])
        self.oasisIndexes = []
        self.desertIndexes = []
        self.spots[1] = ['yellow','green','white']
        self.spots[3] = ['orange','blue']

        self.runOutcomesSpots = copy.deepcopy(self.spots)
        self.runOutcomesAlreadyRolled = {"orange":False,"yellow":False,"green":False,"blue":False,"white":False}

        self.alreadyRolled = {"orange":False,"yellow":False,"green":False,"blue":False,"white":False}

    def findCurrentLocationOfPiece(self,pieceColor):
        initSpotIndexes = next(((i, color.index(pieceColor)) for i, color in enumerate(self.spots) if pieceColor in color), None)
        return initSpotIndexes

    def moveGamePiece(self,pieceColor,rollAmount,gameType):
        #gameType True if normal move; false if runOutcome move
        if gameType:
            spotsInUse = self.spots
            rolledInUse = self.alreadyRolled
        else:
            spotsInUse = self.runOutcomesSpots
            rolledInUse = self.runOutcomesAlreadyRolled

        self.alreadyRolled[pieceColor] = True
        # get current location
        initSpotIndexes = self.findCurrentLocationOfPiece(pieceColor)
        # save piece + camels on back to temp variable
        a = initSpotIndexes[0]
        b = initSpotIndexes[1]
        camelStack = self.spots[a][b:]
        # remove elements from initial spot list
        for camel in camelStack:
            self.spots[a].remove(camel)

        # add elements to final spot list
        newSpotIndex = a + rollAmount
        if newSpotIndex > 15:
            print("Game Has Been Won")
            self.spots[16].extend(camelStack)
        else:
            if newSpotIndex in self.oasisIndexes:
                self.spots[newSpotIndex+1].extend(camelStack)
            elif newSpotIndex in self.desertIndexes:
                camelStack.extend(self.spots[newSpotIndex-1])
                self.spots[newSpotIndex-1] = camelStack
            else:
                self.spots[newSpotIndex].extend(camelStack)

    def moveGameCard(self, cardType,spotIndex):
        # cardType is "desert" or "oasis"
        # spotIndex
        if cardType == "desert":
            self.desertIndexes.extend(spotIndex)
        elif cartType == "oasis":
            self.oasisIndexes.extend(spotIndex)
        else:
            print("please type either 'desert' or 'oasis'")

    def generateMoves(self):
        import itertools
        allColors = ["orange","yellow","green","blue","white"]
        piecesInPlay = []
        for element in allColors:
            if self.alreadyRolled[element]:
                piecesInPlay.append(element)
        allOrderOfColors = list(itertools.permutations(piecesInPlay))
        #generates [(0, 1, 2, 3, 4), (0, 1, 2, 4, 3), (0, 1, 3, 2, 4), (0, 1, 3, 4, 2), (0, 1, 4, 2, 3), (0, 1, 4, 3, 2)...]
        #allOrderOfColors = [[0,1,2,3,4],[0,1,2,3,4]]
        #allOrderOfColors = [(0, 1, 2, 3, 4), (0, 1, 2, 4, 3), (0, 1, 3, 2, 4), (0, 1, 3, 4, 2), (0, 1, 4, 2, 3)]
        allRolls = set(list(itertools.permutations([1,2,3]*5, len(piecesInPlay))))
        # [(1, 2, 3, 1, 2), (1, 2, 3, 1, 3), (1, 2, 3, 1, 1), (1, 2, 3, 1, 2)...]
        #allRolls = [[1,2,1,3,2],[1,2,1,3,2]]
        #allRolls = [(1, 2, 3, 1, 2), (1, 2, 3, 1, 3), (1, 2, 3, 1, 1), (1, 2, 3, 1, 2)]
        return allOrderOfColors, allRolls

    def runMovesAndRecordBoards(self, allOrderOfColors, allRolls):
        #input Moves
        allBoardStates = []
        q = 0
        for orderElement in allOrderOfColors:
            for rollElement in allRolls:
                self.runOutcomesSpots = copy.deepcopy(self.spots)
                for i in range(len(rollElement)):
                    self.runOutcomesSpots = moveAPiece(orderElement[i],rollElement[i],False)
                q += 1
                # print("local board")
                # print(local_game_board)
                allBoardStates.append(copy.deepcopy(local_game_board))
                # print("all boards")
                # print(allBoardStates)
            print("%d possibilities calculated" % q)
        #output List of game boardState
        return allBoardStates


    def flattenBoard(list_of_lists):
        #http://stackoverflow.com/questions/11264684/flatten-list-of-lists
        flattened = []
        for sublist in list_of_lists:
            for val in sublist:
                flattened.append(val)
        return flattened

    def getRank(allBoardStates):
        #flatten List of lists
        listOfRankedLists=[]
        for j in range(len(allBoardStates)):
            game_board = allBoardStates[j]
            localFlattened = flattenBoard(game_board)
            localFlattened.reverse()
            listOfRankedLists.append(localFlattened)
        return listOfRankedLists

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
