#Karan Vombatkere
#May 2020

#Imports
from string import *
import numpy as np
from hexTile import *
#import pygame

###Class to implement Catan board
##Use a graph representation for the board
class catanBoard():
    'Class Definition for Catan Board '
    #Object Creation - creates a random board configuration with hexTiles
    #Takes
    def __init__(self):
        self.HexTileList = [] #Dictionary to store all hextiles
        self.resourcesList = self.getRandomResourceList()

        #Get a random permutation of indices 0-18 to use with the resource list
        randomIndices = np.random.permutation([i for i in range(len(self.resourcesList))])
        print(randomIndices)

        #Generate the hexes and the graphs with the Centers and Resources defined
        for rand_i in randomIndices:
            #Get the list of neighbors for this hexTile
            newHexTile = hexTile(self.resourcesList[rand_i], Point(2,3)
        #Define the central Hex
        #hex0 = hexTile()

        return None

    #Function to add a hexTile - specified from parent Hex and 
    def addHexTile(self, parentHex, location):
        return None

    #Function to generate a random permutation of resources
    def getRandomResourceList(self):
        #Define Resources as a dict
        Resource_Dict = {'DESERT':1, 'ORE':3, 'BRICK':3, 'WHEAT':4, 'WOOD':4, 'SHEEP':4}
        #Get a random permutation of the numbers
        NumberList = np.random.permutation([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
        numIndex = 0

        resourceList = [] 
        for r in Resource_Dict.keys():
            numberofResource = Resource_Dict[r]
            if(r != 'DESERT'):
                for n in range(numberofResource):
                    resourceList.append(Resource(r, NumberList[numIndex]))
                    numIndex += 1
            else:
                resourceList.append(Resource(r, None))

        print(resourceList)

        return resourceList

    #Function to Display Hex Info
    def displayBoard(self):
        return None
    


#Test Code
testBoard = catanBoard()

