#Karan Vombatkere
#Summer 2020

#Imports
from board import *
from player import *
import numpy as np

#Class definition for an AI player
class AI_Player(player):
    
    #Update AI player flag and resources
    def updateAI(self): 
        self.isAI = True
        self.setupResources = [] #List to keep track of setup resources
        self.resources = {'ORE':0, 'BRICK':4, 'WHEAT':2, 'WOOD':4, 'SHEEP':2} #Dictionary that keeps track of resource amounts
        print("Added new AI Player:", self.name)


    #Function to build an initial settlement - just choose random spot for now
    def initial_setup(self, board):
        #Build random settlement
        possibleVertices = board.get_setup_settlements(self)

        #Simple heuristic for choosing initial spot
        diceRoll_expectation = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1, None:0}
        vertexValues = []

        #Get the adjacent hexes for each hex
        for v in possibleVertices.keys():
            vertexNumValue = 0
            resourcesAtVertex = []
            #For each adjacent hex get its value and overall resource diversity for that vertex
            for adjacentHex in board.boardGraph[v].adjacentHexList:
                resourceType = board.hexTileDict[adjacentHex].resource.type
                if(resourceType not in resourcesAtVertex):
                    resourcesAtVertex.append(resourceType)
                numValue = board.hexTileDict[adjacentHex].resource.num
                vertexNumValue += diceRoll_expectation[numValue] #Add to total value of this vertex

            #basic heuristic for resource diversity
            vertexNumValue += len(resourcesAtVertex)*2
            for r in resourcesAtVertex:
                if(r != 'DESERT' and r not in self.setupResources):
                    vertexNumValue += 2.5 #Every new resource gets a bonus
            
            vertexValues.append(vertexNumValue)


        vertexToBuild_index = vertexValues.index(max(vertexValues))
        vertexToBuild = list(possibleVertices.keys())[vertexToBuild_index]

        #Add to setup resources
        for adjacentHex in board.boardGraph[vertexToBuild].adjacentHexList:
            resourceType = board.hexTileDict[adjacentHex].resource.type
            if(resourceType not in self.setupResources and resourceType != 'DESERT'):
                self.setupResources.append(resourceType)

        self.build_settlement(vertexToBuild, board)


        #Build random road
        possibleRoads = board.get_setup_roads(self)
        randomEdge = np.random.randint(0, len(possibleRoads.keys()))
        self.build_road(list(possibleRoads.keys())[randomEdge][0], list(possibleRoads.keys())[randomEdge][1], board)

    
    def move(self, board):
        print("AI Player {} playing...".format(self.name))
        #Trade resources if there are excessive amounts of a particular resource
        self.trade()
        #Build a settlements, city and few roads
        possibleVertices = board.get_potential_settlements(self)
        if(possibleVertices != {} and (self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0)):
            randomVertex = np.random.randint(0, len(possibleVertices.keys()))
            self.build_settlement(list(possibleVertices.keys())[randomVertex], board)

        #Build a City
        possibleVertices = board.get_potential_cities(self)
        if(possibleVertices != {} and (self.resources['WHEAT'] >= 2 and self.resources['ORE'] >= 3)):
            randomVertex = np.random.randint(0, len(possibleVertices.keys()))
            self.build_city(list(possibleVertices.keys())[randomVertex], board)

        #Build a couple roads
        for i in range(2):
            if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0):
                possibleRoads = board.get_potential_roads(self)
                randomEdge = np.random.randint(0, len(possibleRoads.keys()))
                self.build_road(list(possibleRoads.keys())[randomEdge][0], list(possibleRoads.keys())[randomEdge][1], board)

        #Draw a Dev Card with 1/3 probability
        devCardNum = np.random.randint(0, 3)
        if(devCardNum == 0):
            self.draw_devCard(board)
        
        return

    #Wrapper function to control all trading
    def trade(self):
        for r1, r1_amount in self.resources.items():
            if(r1_amount >= 6): #heuristic to trade if a player has more than 5 of a particular resource
                for r2, r2_amount in self.resources.items():
                    if(r2_amount < 1):
                        self.trade_with_bank(r1, r2)
                        break

    #Function to basic trade 4:1 with bank
    def trade_with_bank(self, r1, r2):
        if(self.resources[r1] >= 4):
            self.resources[r1] -= 4
            self.resources[r2] += 1
            print("Traded 4 {} for 1 {}".format(r1, r2))
        else:
            print("Insufficient resource {} to trade 4:1 with Bank".format(r1))


    #Function to find best action - based on gamestate
    def get_action(self):
        return

    #Function to execute the player's action
    def execute_action(self):
        return




