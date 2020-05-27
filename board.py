#Karan Vombatkere
#May 2020

#Imports
from string import *
import numpy as np
from hexTile import *
from hexLib import *
import networkx as nx
#import matplotlib.pyplot as plt
import pygame

pygame.init()

###Class to implement Catan board
##Use a graph representation for the board
class catanBoard():
    'Class Definition for Catan Board '
    #Object Creation - creates a random board configuration with hexTiles
    #Takes
    def __init__(self):
        self.hexTileList = [] #List to store all hextiles
        self.resourcesList = self.getRandomResourceList()

        #Get a random permutation of indices 0-18 to use with the resource list
        randomIndices = np.random.permutation([i for i in range(len(self.resourcesList))])
        
        hexIndex_i = 0 #initialize hexIndex at 0
        #Neighbors are specified in adjacency matrix - hard coded

        #Generate the hexes and the graphs with the Index, Centers and Resources defined
        for rand_i in randomIndices:
            #Get the coordinates of the new hex, indexed by hexIndex_i
            hexCoords = self.getHexCoords(hexIndex_i)

            #Create the new hexTile with index and append + increment index
            newHexTile = hexTile(hexIndex_i, self.resourcesList[rand_i], hexCoords)
            self.hexTileList.append(newHexTile)
            hexIndex_i += 1

        return None

    def getHexCoords(self, hexInd):
        #Dictionary to store Axial Coordinates (q, r) by hexIndex
        coordDict = {0:Axial_Point(0,0), 1:Axial_Point(0,-1), 2:Axial_Point(1,-1), 3:Axial_Point(1,0), 4:Axial_Point(0,1), 5:Axial_Point(-1,1), 6:Axial_Point(-1,0), 7:Axial_Point(0,-2), 8:Axial_Point(1,-2), 9:Axial_Point(2,-2), 10:Axial_Point(2,-1),
                        11:Axial_Point(2,0), 12:Axial_Point(1,1), 13:Axial_Point(0,2), 14:Axial_Point(-1,2), 15:Axial_Point(-2,2), 16:Axial_Point(-2,1), 17:Axial_Point(-2,0), 18:Axial_Point(-1,-1)}
        return coordDict[hexInd]

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

        return resourceList

    #Function to generate a graph of the board
    def generateBoardGraph(self):
        self.boardGraph = {} #create a dictionary to store the graph


    #Function to Display Catan Board Info
    def displayBoardInfo(self):
        for tile in self.hexTileList:
            tile.displayHexInfo()
        return None

    #Use pygame to display the board
    def displayBoard(self):
        #Dictionary to store RGB Color values
        colorDict = {"BRICK":(255,51,51), "ORE":(128, 128, 128), "WHEAT":(255,255,51), "WOOD":(0,153,0), "SHEEP":(51,255,51), "DESERT":(255,255,204)}
        
        size = width, height = 1000, 800
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Catan')
        font_resource = pygame.font.Font(pygame.font.get_default_font(), 15)

        flat = Layout(layout_flat, Point(80.0, 80.0), Point(width/2, height/2)) #specify Layout

        startTime = pygame.time.get_ticks()
        runTime = 0
        
        while runTime < 10000:
            #Render each hexTile
            for hexTile in self.hexTileList:
                hexTileCorners = polygon_corners(flat, hexTile.hex)
                hexTileColor_rgb = colorDict[hexTile.resource.type]
                pygame.draw.polygon(screen, pygame.Color(hexTileColor_rgb[0],hexTileColor_rgb[1], hexTileColor_rgb[2]), hexTileCorners, width==0)

                hexTile.pixelCenter = hex_to_pixel(flat, hexTile.hex)
                resourceText = font_resource.render(str(hexTile.resource.type) + " (" +str(hexTile.resource.num) + ")", False, (0,0,0))
                screen.blit(resourceText, (hexTile.pixelCenter.x -25, hexTile.pixelCenter.y))
            
            pygame.display.update()
            runTime = pygame.time.get_ticks() - startTime
        



#Test Code
testBoard = catanBoard()
testBoard.displayBoardInfo()
testBoard.displayBoard()
