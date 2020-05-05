#Karan Vombatkere
#May 2020

##Class to implement Catan board Hexagonal Tile

class hexTile():
    'Class Definition for Catan Board Hexagonal Tile'

    #Object Creation
    def __init__(self, resourceName, num):
        self.resource = resourceName
        self.num = num

    #Function to Display Hex Info
    def displayHexInfo(self):
        print(self.resource, self.num)
    

#Test Code
testHex = hexTile('Ore', 8)
testHex.displayHexInfo()