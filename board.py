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
        self.vertexList = [] #List to store the Vertices coordinates
        self.boardGraph = [] #List to store the vertex objects
        self.resourcesList = self.getRandomResourceList()
        self.edgeLength = 80 #Specify for hex size

        #Use pygame to display the board
        self.size = width, height = 1000, 800
        self.flat = Layout(layout_flat, Point(self.edgeLength, self.edgeLength), Point(width/2, height/2)) #specify Layout

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

        #Create the vertex graph
        self.generateVertexGraph()

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


    #Function to generate the entire board graph
    def generateVertexGraph(self):
        for hexTile in self.hexTileList:
            hexTileCorners = polygon_corners(self.flat, hexTile.hex) #Get vertices of each hex
            #Create vertex graph with this list of corners
            self.updateVertexGraph(hexTileCorners, hexTile.index)

        #Once all hexTiles have been added  get edges
        self.updateGraphEdges()


    #Function to update a graph of the board with each vertex as a node
    def updateVertexGraph(self, vertexCoordList, hexIndx):
        for v in vertexCoordList:
            #Check if vertex already exists - update adjacentHexList if it does
            if v in self.vertexList:
                for existingVertex in self.boardGraph:
                    if(existingVertex.pixelCoordinates == v):
                        existingVertex.adjacentHexList.append(hexIndx)

            else:#Create new vertex if it doesn't exist
                #print('Adding Vertex:', v)
                newVertex = Vertex(v, hexIndx)
                self.vertexList.append(v)
                self.boardGraph.append(newVertex)

    
    #Function to add adges to graph given all vertices
    def updateGraphEdges(self):
        for v1 in self.boardGraph:
            for v2 in self.boardGraph:
                if(self.vertexDistance(v1, v2) == self.edgeLength):
                    v1.edgeList.append(v2)


    @staticmethod
    def vertexDistance(v1, v2):
        dist = ((v1.pixelCoordinates.x - v2.pixelCoordinates.x)**2 + (v1.pixelCoordinates.y - v2.pixelCoordinates.y)**2)**0.5
        return round(dist)


    def printGraph(self):
        print(len(self.boardGraph))
        for node in self.boardGraph:
            print(node.pixelCoordinates, len(node.edgeList), node.adjacentHexList)
            
    #Function to Display Catan Board Info
    def displayBoardInfo(self):
        for tile in self.hexTileList:
            tile.displayHexInfo()
        return None


    #Function to display the board
    def displayBoard(self):
        #Dictionary to store RGB Color values
        colorDict = {"BRICK":(255,51,51), "ORE":(128, 128, 128), "WHEAT":(255,255,51), "WOOD":(0,153,0), "SHEEP":(51,255,51), "DESERT":(255,255,204)}
        
        size = width, height = 1000, 800
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Catan')
        font_resource = pygame.font.Font(pygame.font.get_default_font(), 15)

        startTime = pygame.time.get_ticks()
        runTime = 0
        
        while runTime < 2000:
            #Render each hexTile
            for hexTile in self.hexTileList:
                hexTileCorners = polygon_corners(self.flat, hexTile.hex)

                hexTileColor_rgb = colorDict[hexTile.resource.type]
                pygame.draw.polygon(screen, pygame.Color(hexTileColor_rgb[0],hexTileColor_rgb[1], hexTileColor_rgb[2]), hexTileCorners, width==0)
                #print(hexTile.index, hexTileCorners)

                hexTile.pixelCenter = hex_to_pixel(self.flat, hexTile.hex) #Get pixel center coordinates of hex
                if(hexTile.resource.type != 'DESERT'): #skip desert text/number
                    resourceText = font_resource.render(str(hexTile.resource.type) + " (" +str(hexTile.resource.num) + ")", False, (0,0,0))
                    screen.blit(resourceText, (hexTile.pixelCenter.x -25, hexTile.pixelCenter.y)) #add text to hex

            pygame.display.update()
            runTime = pygame.time.get_ticks() - startTime

        return None
        



