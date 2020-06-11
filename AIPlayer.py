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
        print("Added new AI Player:", self.name)


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

    
    def move(self, board):
        print("AI Player making random moves...")
        
        #Build a few random roads, settlements and cities
        for i in range(4):
            possibleRoads = board.get_potential_roads(self)
            randomEdge = np.random.randint(0, len(possibleRoads.keys()))
            self.build_road(list(possibleRoads.keys())[randomEdge][0], list(possibleRoads.keys())[randomEdge][1], board)

        #Build a couple settlements
        for i in range(2):
            possibleVertices = board.get_potential_settlements(self)
            if(possibleVertices != {}):
                randomVertex = np.random.randint(0, len(possibleVertices.keys()))
                self.build_settlement(list(possibleVertices.keys())[randomVertex], board)

        #Build a City
        possibleVertices = board.get_potential_cities(self)
        if(possibleVertices != {}):
            randomVertex = np.random.randint(0, len(possibleVertices.keys()))
            self.build_city(list(possibleVertices.keys())[randomVertex], board)

        #Draw a Dev Card
        self.draw_devCard(board)
        
        return


    #Function to find best action - based on gamestate
    def get_action(self):
        return

    #Function to execute the player's action
    def execute_action(self):
        return




