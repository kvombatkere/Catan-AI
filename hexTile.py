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
    def __init__(self, hexResource, center, neighborList=None):
        self.resource = hexResource
        self.coord = center
        self.neighborList = neighborList

    #Function to update hex neighbors
    def updateNeighbors(self):
        


    #Function to Display Hex Info
    def displayHexInfo(self):
        print('Resource:{}; Center:{}'.format(self.resource, self.coord))
        return None
        

    #Function to display Hex Neighbors
    def displayHexNeighbors(self):
        print('Neighbors:')
        for neighbor in self.neighborList:
            neighbor.displayHexInfo()

        return None

    

#Test Code
# testHex = hexTile(Resource('Ore', 8), Point(2,3), [hexTile(Resource('Wheat', 11), Point(5,6)), hexTile(Resource('Brick', 11), Point(7,4))])
# testHex.displayHexInfo()
# testHex.displayHexNeighbors()