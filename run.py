from camelCupGame import GameBoard

pieceLocations = [ (1,['blue','orange']),
                    (2,['white','yellow']),
                    (3,['green']),
                    (15,[]),
                    (16,[]) ]
game_board = GameBoard(pieceLocations)
game_board.alreadyRolled = {"orange":False,
                            "yellow":False,
                            "green":False,
                            "blue":False,
                            "white":False}




game_board.moveGamePiece('yellow',2)
game_board.moveGamePiece('green',1)
game_board.moveGameCard('desert',3)


game_board.runMovesAndRecordBoards()
#print(game_board.allBoardStates)
game_board.getRank()
#print(game_board.listOfRankedLists)
firstPlaceList, secondPlaceList = game_board.summarizeRanks()

#------------------ Pie Chart
import matplotlib.pyplot as plt

# Data to plot
labels = [element[0].upper() for element in firstPlaceList]
sizes = [element[1] for element in firstPlaceList]
colors = [element[0] for element in firstPlaceList]
explode = (0.1, 0, 0, 0, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=90)

plt.axis('equal')
plt.show()
#------------------- end Pie Chart


# print(firstCounter)
# print(secondCounter)
