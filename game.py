from board import *

#Test Code
class catanGame():
    #Create new gameboard
    def __init__(self):
        self.board = catanBoard()   
        
        #Run test functions to view board and vertex graph
        self.board.printGraph()
        self.board.displayBoard()
        


newGame = catanGame()