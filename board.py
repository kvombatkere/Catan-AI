#Karan Vombatkere
#May 2020

#Imports
from string import *
import numpy as np
from hexTile import *
from hexLib import *
from player import *
import networkx as nx
#import matplotlib.pyplot as plt
import pygame

pygame.init()

###Class to implement Catan board
##Use a graph representation for the board
class catanBoard(hexTile, Vertex):
    'Class Definition for Catan Board '
    #Object Creation - creates a random board configuration with hexTiles
    #Takes
    def __init__(self):
        self.hexTileDict = {} #Dict to store all hextiles, with hexIndex as key
        self.vertexList = [] #List to store the Vertices coordinates
        self.boardGraph = {} #Dict to store the vertex objects with the pixelCoordinates as keys
        self.resourcesList = self.getRandomResourceList()
        self.edgeLength = 80 #Specify for hex size

        #Use pygame to display the board
        self.size = self.width, self.height = 1000, 800
        self.flat = Layout(layout_flat, Point(self.edgeLength, self.edgeLength), Point(self.width/2, self.height/2)) #specify Layout

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Catan')
        self.font_resource = pygame.font.SysFont('cambria', 15)

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
            self.hexTileDict[hexIndex_i] = newHexTile
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
        for hexTile in self.hexTileDict.values():
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
                for existingVertex in self.boardGraph.keys():
                    if(existingVertex == v):
                        self.boardGraph[v].adjacentHexList.append(hexIndx)

            else:#Create new vertex if it doesn't exist
                #print('Adding Vertex:', v)
                newVertex = Vertex(v, hexIndx)
                self.vertexList.append(v)
                self.boardGraph[v] = newVertex

    
    #Function to add adges to graph given all vertices
    def updateGraphEdges(self):
        for v1 in self.boardGraph.keys():
            for v2 in self.boardGraph.keys():
                if(self.vertexDistance(v1, v2) == self.edgeLength):
                    self.boardGraph[v1].edgeList.append(v2)


    @staticmethod
    def vertexDistance(v1, v2):
        dist = ((v1.x - v2.x)**2 + (v1.y - v2.y)**2)**0.5
        return round(dist)


    def printGraph(self):
        print(len(self.boardGraph))
        for node in self.boardGraph.keys():
            print(node, len(self.boardGraph[node].edgeList), self.boardGraph[node].adjacentHexList)
            
    #Function to Display Catan Board Info
    def displayBoardInfo(self):
        for tile in self.hexTileList.values():
            tile.displayHexInfo()
        return None


    #Function to display the initial board
    def displayInitialBoard(self):
        #Dictionary to store RGB Color values
        colorDict_RGB = {"BRICK":(255,51,51), "ORE":(128, 128, 128), "WHEAT":(255,255,51), "WOOD":(0,153,0), "SHEEP":(51,255,51), "DESERT":(255,255,204)}
        pygame.draw.rect(self.screen, pygame.Color('royalblue2'), (0,0,self.width,self.height)) #blue background

        #Render each hexTile
        for hexTile in self.hexTileDict.values():
            hexTileCorners = polygon_corners(self.flat, hexTile.hex)

            hexTileColor_rgb = colorDict_RGB[hexTile.resource.type]
            pygame.draw.polygon(self.screen, pygame.Color(hexTileColor_rgb[0],hexTileColor_rgb[1], hexTileColor_rgb[2]), hexTileCorners, self.width==0)
            #print(hexTile.index, hexTileCorners)

            hexTile.pixelCenter = hex_to_pixel(self.flat, hexTile.hex) #Get pixel center coordinates of hex
            if(hexTile.resource.type != 'DESERT'): #skip desert text/number
                resourceText = self.font_resource.render(str(hexTile.resource.type) + " (" +str(hexTile.resource.num) + ")", False, (0,0,0))
                self.screen.blit(resourceText, (hexTile.pixelCenter.x -25, hexTile.pixelCenter.y)) #add text to hex

        pygame.display.update()

        #startTime = pygame.time.get_ticks()
        #runTime = 0
        #runTime = pygame.time.get_ticks() - startTime

        return None

    #Function to display the main catanBoard
    #def displayMainBoard(self):


    #Function to draw a road on the board
    def draw_road(self, edgeToDraw, roadColor):
        pygame.draw.line(self.screen, pygame.Color(roadColor), edgeToDraw[0], edgeToDraw[1], 10)

    #Function to draw a road on the board
    def draw_possible_road(self, edgeToDraw, roadColor):
        roadRect = pygame.draw.line(self.screen, pygame.Color(roadColor), edgeToDraw[0], edgeToDraw[1], 3)
        return roadRect

    #Function to draw a settlement on the board at vertexToDraw
    def draw_settlement(self, vertexToDraw, color):
        newSettlement = pygame.Rect(vertexToDraw[0]-10, vertexToDraw[1]-10, 25, 25)
        pygame.draw.rect(self.screen, pygame.Color(color), newSettlement)


    #Function to get available settlements for colonisation for a particular player
    def get_settleable_vertices(self, player):
        return None

    #Function to get the list of potential roads a player can build.
    #Return these roads as tuples of vertex pairs
    def get_potential_roads(self, player):
        colonisableRoads = []
        colonisableRoadRects = []
        #Check potential roads from each road the player already has
        for existingRoad in player.buildGraph['ROADS']:
            for vertex_i in existingRoad: #Iterate over both vertices of this road
                #Check neighbors from this vertex
                for indx, v_i in enumerate(self.boardGraph[vertex_i].edgeList):
                    if(self.boardGraph[vertex_i].edgeState[indx] == False): #Edge currently does not have a road
                        colonisableRoads.append((vertex_i, v_i))
        
        for road in colonisableRoads:    
            roadRect = self.draw_possible_road(road, player.color)
            colonisableRoadRects.append(roadRect)
    
        return colonisableRoadRects, colonisableRoads
    
    #Function to update boardGraph with Road by player
    def updateBoardGraph_road(self, v_coord1, v_coord2, player):
        #Update edge from first vertxex v1
        for indx, v in enumerate(self.boardGraph[v_coord1].edgeList):
            if(v == v_coord2):
                self.boardGraph[v_coord1].edgeState[indx] = True
        
        #Update edge from second vertxex v2
        for indx, v in enumerate(self.boardGraph[v_coord2].edgeList):
            if(v == v_coord1):
                self.boardGraph[v_coord2].edgeState[indx] = True
        
        #self.draw_road([v_coord1, v_coord2], player.color) #Draw the settlement


    #Function to update boardGraph with settlement on vertex v
    def updateBoardGraph_settlement(self, v_coord, player):
        self.boardGraph[v_coord].state['Player'] = player 
        self.boardGraph[v_coord].state['Settlement'] = True
        self.boardGraph[v_coord].isColonised = True 

        #self.draw_settlement(v_coord, player.color) #Draw the settlement


    #Function to get a hexTile with a particular number
    def getHexResourceRolled(self, diceRollNum):
        hexesRolled = [] #Empty list to store the hex index rolled (min 1, max 2)
        for hexTile in self.hexTileDict.values():
            if hexTile.resource.num == diceRollNum:
                hexesRolled.append(hexTile.index)

        return hexesRolled