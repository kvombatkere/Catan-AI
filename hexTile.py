#Karan Vombatkere
#May 2020

#IMPORTS
import collections

##Class to implement Catan board Hexagonal Tile
Point = collections.namedtuple("Point", ["x", "y"])
Resource = collections.namedtuple("Resource", ["type", "num"])

class hexTile():
    'Class Definition for Catan Board Hexagonal Tile'

    #Object Creation - specify the resource, num, center and neighbor list
    #Center is a point and neighborList is a list of hexTiles
    #hexIndex is a number from 0-18 specifying the Hex's position
    def __init__(self, hexIndex, hexResource, center, neighborList=None):
        self.resource = hexResource
        self.coord = center
        self.index = hexIndex
        self.neighborList = neighborList

    #Function to update hex neighbors
    def updateNeighbors(self):
        return None


    #Function to Display Hex Info
    def displayHexInfo(self):
        print('Index:{}; Resource:{}; Center:{}'.format(self.index, self.resource, self.coord))
        return None
        

    #Function to display Hex Neighbors
    def displayHexNeighbors(self):
        print('Neighbors:')
        for neighbor in self.neighborList:
            neighbor.displayHexInfo()

        return None

    

#Test Code
# testHex = hexTile(0, Resource('Ore', 8), Point(2,3), [hexTile(2, Resource('Wheat', 11), Point(5,6)), hexTile(3, Resource('Brick', 11), Point(7,4))])
# testHex.displayHexInfo()
# testHex.displayHexNeighbors()