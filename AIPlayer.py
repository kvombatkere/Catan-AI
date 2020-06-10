#Karan Vombatkere
#Summer 2020

#Imports
from board import *
from player import *
import numpy as np

#Class definition for an AI player
class AI_Player(player):
    
    def updateAI(self):
        self.isAI = True
        print("Updated new AI Player:", self.name)


    #Function to build an initial settlement - just choose random spot for now
    def initial_setup(self, board):
        #Build random settlement
        possibleVertices = board.get_setup_settlements(self)
        randomVertex = np.random.randint(0, len(possibleVertices.keys()))
        self.build_settlement(list(possibleVertices.keys())[randomVertex], board)

        #Build random road
        possibleRoads = board.get_setup_roads(self)
        randomEdge = np.random.randint(0, len(possibleRoads.keys()))
        self.build_road(list(possibleRoads.keys())[randomEdge][0], list(possibleRoads.keys())[randomEdge][1], board)


    #Function to find best action - based on gamestate
    def get_action(self):
        return

    #Function to execute the player's action
    def execute_action(self):
        return




