#Karan Vombatkere
#Settlers of Catan, 2020

import pygame
from hexTile import *
from hexLib import *

pygame.init()

#Class to handle catan board display
class catanBoardView():
    'Class definition for Catan board display'
    def __init__(self):
        # self.hexTileDict = {} #Dict to store all hextiles, with hexIndex as key
        # self.vertex_index_to_pixel_dict = {} #Dict to store the Vertices coordinates with vertex indices as keys
        # self.boardGraph = {} #Dict to store the vertex objects with the pixelCoordinates as keys
        # self.resourcesList = self.getRandomResourceList()


        #Use pygame to display the board
        self.edgeLength = 80 #Specify for hex size

        self.size = self.width, self.height = 1000, 800
        self.flat = Layout(layout_flat, Point(self.edgeLength, self.edgeLength), Point(self.width/2, self.height/2)) #specify Layout

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Settlers of Catan')
        self.font_resource = pygame.font.SysFont('cambria', 15)

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


        #Display the Ports
        for vCoord, vertexInfo in self.boardGraph.items():
            if(vertexInfo.port != False):
                portText = self.font_resource.render(vertexInfo.port + " PORT", False, (230,0,0))
                self.screen.blit(portText, (vCoord.x, vCoord.y)) 
            
        pygame.display.update()

        return None


    #Function to draw a road on the board
    def draw_road(self, edgeToDraw, roadColor):
        pygame.draw.line(self.screen, pygame.Color(roadColor), edgeToDraw[0], edgeToDraw[1], 10)


    #Function to draw a potential road on the board - thin
    def draw_possible_road(self, edgeToDraw, roadColor):
        roadRect = pygame.draw.line(self.screen, pygame.Color(roadColor), edgeToDraw[0], edgeToDraw[1], 5)
        return roadRect


    #Function to draw a settlement on the board at vertexToDraw
    def draw_settlement(self, vertexToDraw, color):
        newSettlement = pygame.Rect(vertexToDraw.x-10, vertexToDraw.y-10, 25, 25)
        pygame.draw.rect(self.screen, pygame.Color(color), newSettlement)


    #Function to draw a potential settlement on the board - thin
    def draw_possible_settlement(self, vertexToDraw, color):
        possibleSettlement = pygame.draw.circle(self.screen, pygame.Color(color), (int(vertexToDraw.x), int(vertexToDraw.y)), 20, 3)
        return possibleSettlement

    
    #Function to draw a settlement on the board at vertexToDraw
    def draw_city(self, vertexToDraw, color):
        pygame.draw.circle(self.screen, pygame.Color(color), (int(vertexToDraw.x), int(vertexToDraw.y)), 24)

    #Function to draw a potential settlement on the board - thin
    def draw_possible_city(self, vertexToDraw, color):
        possibleCity = pygame.draw.circle(self.screen, pygame.Color(color), (int(vertexToDraw.x), int(vertexToDraw.y)), 25, 5)
        return possibleCity
