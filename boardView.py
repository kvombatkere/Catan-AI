#Karan Vombatkere
#Settlers of Catan, 2020

import pygame
from hexTile import *
from hexLib import *

pygame.init()

#Class to handle catan board display
class catanBoardView():
    'Class definition for Catan board display'
    def __init__(self, catanBoardObject):
        # self.hexTileDict = {} #Dict to store all hextiles, with hexIndex as key
        # self.vertex_index_to_pixel_dict = {} #Dict to store the Vertices coordinates with vertex indices as keys
        # self.boardGraph = {} #Dict to store the vertex objects with the pixelCoordinates as keys
        # self.resourcesList = self.getRandomResourceList()

        self.board = catanBoardObject

        #Use pygame to display the board
        self.edgeLength = 80 #Specify for hex size

        self.size = self.width, self.height = 1000, 800
        self.flat = Layout(layout_flat, Point(self.edgeLength, self.edgeLength), Point(self.width/2, self.height/2)) #specify Layout

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Settlers of Catan')
        self.font_resource = pygame.font.SysFont('cambria', 15)

        self.font_button = pygame.font.SysFont('cambria', 12)
        self.font_diceRoll = pygame.font.SysFont('cambria', 25) #dice font
        self.font_Robber = pygame.font.SysFont('arialblack', 50) #robber font

        return None


    #Function to display the initial board
    def displayInitialBoard(self):
        #Dictionary to store RGB Color values
        colorDict_RGB = {"BRICK":(255,51,51), "ORE":(128, 128, 128), "WHEAT":(255,255,51), "WOOD":(0,153,0), "SHEEP":(51,255,51), "DESERT":(255,255,204)}
        pygame.draw.rect(self.screen, pygame.Color('royalblue2'), (0,0,self.width,self.height)) #blue background

        #Render each hexTile
        for hexTile in self.board.hexTileDict.values():
            hexTileCorners = polygon_corners(self.flat, hexTile.hex)

            hexTileColor_rgb = colorDict_RGB[hexTile.resource.type]
            pygame.draw.polygon(self.screen, pygame.Color(hexTileColor_rgb[0],hexTileColor_rgb[1], hexTileColor_rgb[2]), hexTileCorners, self.width==0)
            #print(hexTile.index, hexTileCorners)

            hexTile.pixelCenter = hex_to_pixel(self.flat, hexTile.hex) #Get pixel center coordinates of hex
            if(hexTile.resource.type != 'DESERT'): #skip desert text/number
                resourceText = self.font_resource.render(str(hexTile.resource.type) + " (" +str(hexTile.resource.num) + ")", False, (0,0,0))
                self.screen.blit(resourceText, (hexTile.pixelCenter.x -25, hexTile.pixelCenter.y)) #add text to hex


        #Display the Ports
        for vCoord, vertexInfo in self.board.boardGraph.items():
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

    
    #Function to draw the possible spots for a robber
    def draw_possible_robber(self, vertexToDraw):
        possibleRobber = pygame.draw.circle(self.screen, pygame.Color('black'), (int(vertexToDraw.x), int(vertexToDraw.y)), 50, 5)
        return possibleRobber



    #Function to render basic gameplay buttons
    def displayGameButtons(self):
        #Basic GamePlay Buttons
        diceRollText = self.font_button.render("ROLL DICE", False, (0,0,0))
        buildRoadText = self.font_button.render("ROAD", False, (0,0,0))       
        buildSettleText = self.font_button.render("SETTLE", False, (0,0,0))
        buildCityText = self.font_button.render("CITY", False, (0,0,0))
        endTurnText = self.font_button.render("END TURN", False, (0,0,0))
        devCardText = self.font_button.render("DEV CARD", False, (0,0,0))
        playDevCardText = self.font_button.render("PLAY DEV CARD", False, (0,0,0))

        self.rollDice_button = pygame.Rect(20, 10, 80, 40)
        self.buildRoad_button = pygame.Rect(20, 70, 80, 40)
        self.buildSettlement_button = pygame.Rect(20, 120, 80, 40)
        self.buildCity_button = pygame.Rect(20, 170, 80, 40)
        self.devCard_button = pygame.Rect(20, 220, 80, 40)
        self.playDevCard_button = pygame.Rect(20, 270, 80, 40)
        self.endTurn_button = pygame.Rect(20, 330, 80, 40)

        pygame.draw.rect(self.screen, pygame.Color('darkgreen'), self.rollDice_button) 
        pygame.draw.rect(self.screen, pygame.Color('gray33'), self.buildRoad_button) 
        pygame.draw.rect(self.screen, pygame.Color('gray33'), self.buildSettlement_button) 
        pygame.draw.rect(self.screen, pygame.Color('gray33'), self.buildCity_button)
        pygame.draw.rect(self.screen, pygame.Color('gray33'), self.devCard_button)
        pygame.draw.rect(self.screen, pygame.Color('gray33'), self.playDevCard_button) 
        pygame.draw.rect(self.screen, pygame.Color('burlywood'), self.endTurn_button) 

        self.screen.blit(diceRollText,(30, 20)) 
        self.screen.blit(buildRoadText,(30,80)) 
        self.screen.blit(buildSettleText,(30,130))
        self.screen.blit(buildCityText, (30,180))
        self.screen.blit(devCardText, (30,230))
        self.screen.blit(playDevCardText, (30,280))
        self.screen.blit(endTurnText,(30,340))



    #Function to display robber
    def displayRobber(self):
        #Robber text
        robberText = self.font_Robber.render("R", False, (0,0,0))
        #Get the coordinates for the robber
        for hexTile in self.board.hexTileDict.values():
            if(hexTile.robber):
                robberCoords = hexTile.pixelCenter

        self.screen.blit(robberText, (int(robberCoords.x) -20, int(robberCoords.y)-35)) 



    #Function to display the gameState board - use to display intermediate build screens
    #gameScreenState specifies which type of screen is to be shown
    def displayGameScreen(self, gameScreenState, player):
        #First display all initial hexes and regular buttons
        self.displayInitialBoard()
        self.displayGameButtons()
        self.displayRobber()

        #Loop through and display all existing buildings from players build graphs
        for player_i in list(self.playerQueue.queue): #Build Settlements and roads of each player
            for existingRoad in player_i.buildGraph['ROADS']:
                self.draw_road(existingRoad, player_i.color)
            
            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                self.draw_settlement(settlementCoord, player_i.color)

            for cityCoord in player_i.buildGraph['CITIES']:
                self.draw_city(cityCoord, player_i.color)
        
        if(gameScreenState == 'ROAD'): #Show screen with potential roads
            if(self.gameSetup):
                potentialRoadDict = self.board.get_setup_roads(player)
            else:
                potentialRoadDict = self.board.get_potential_roads(player)
            return potentialRoadDict

        if(gameScreenState == 'SETTLE'): #Show screen with potential settlements
            if(self.gameSetup):
                potentialVertexDict = self.board.get_setup_settlements(player)
            else:
                potentialVertexDict = self.board.get_potential_settlements(player)
            return potentialVertexDict

        if(gameScreenState == 'CITY'): 
            potentialVertexDict = self.board.get_potential_cities(player)
            return potentialVertexDict

        if(gameScreenState == 'ROBBER'):
            potentialRobberDict = self.board.get_robber_spots()
            print("Move Robber")
            return potentialRobberDict

        if(gameScreenState == 'ROB_PLAYER'):
            potentialPlayersDict = self.board.get_players_to_rob(player) #Note here player is actually hexIndex
            return potentialPlayersDict

        #TO-DO Add screens for trades


    #Function to display dice roll
    def displayDiceRoll(self, diceNums):
        #Reset blue background and show dice roll
        pygame.draw.rect(self.board.screen, pygame.Color('royalblue2'), (100, 20, 50, 50)) #blue background
        diceNum = self.font_diceRoll.render(str(diceNums), False, (0,0,0))
        self.board.screen.blit(diceNum,(110, 20)) 
        
        return None

    
    #Function to control build-road action with display
    def buildRoad_display(self, currentPlayer):
        #Get all spots the player can build a road and display thin lines
        roadsPossibleDict = self.displayGameScreen('ROAD', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked
        while(mouseClicked == False):
            if(self.gameSetup):#during gameSetup phase only exit if road is built
                for e in pygame.event.get(): 
                    if e.type == pygame.QUIT:
                            sys.exit(0)
                    if(e.type == pygame.MOUSEBUTTONDOWN):
                        for road, roadRect in roadsPossibleDict.items():
                            if(roadRect.collidepoint(e.pos)): 
                                currentPlayer.build_road(road[0], road[1], self.board)
                                mouseClicked = True

            else: 
                for e in pygame.event.get(): 
                    if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                        for road, roadRect in roadsPossibleDict.items():
                            if(roadRect.collidepoint(e.pos)): 
                                currentPlayer.build_road(road[0], road[1], self.board)
                        
                        mouseClicked = True
                        

    #Function to control build-setttlment action with display
    def buildSettlement_display(self, currentPlayer):
        #Get all spots the player can build a settlement and display thin circles
        verticesPossibleDict = self.displayGameScreen('SETTLE', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked

        while(mouseClicked == False):
            if(self.gameSetup): #during gameSetup phase only exit if settlement is built
                for e in pygame.event.get(): 
                    if e.type == pygame.QUIT:
                            sys.exit(0)
                    if(e.type == pygame.MOUSEBUTTONDOWN):
                        for vertex, vertexRect in verticesPossibleDict.items():
                            if(vertexRect.collidepoint(e.pos)): 
                                currentPlayer.build_settlement(vertex, self.board)
                                mouseClicked = True
            else:
                for e in pygame.event.get(): 
                    if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                        for vertex, vertexRect in verticesPossibleDict.items():
                            if(vertexRect.collidepoint(e.pos)): 
                                currentPlayer.build_settlement(vertex, self.board)
                        
                        mouseClicked = True

    #Function to control the build-city action with display
    def buildCity_display(self, currentPlayer):
        #Get all spots the player can build a city and display circles
        verticesPossibleDict = self.displayGameScreen('CITY', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked - whether a city is built or not

        while(mouseClicked == False):
            for e in pygame.event.get(): 
                if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                    for vertex, vertexRect in verticesPossibleDict.items():
                        if(vertexRect.collidepoint(e.pos)): 
                            currentPlayer.build_city(vertex, self.board)
                    
                    mouseClicked = True

    #Function to control the move-robber action with display
    def moveRobber_display(self, currentPlayer):
        #Get all spots the player can move robber to and show circles
        possibleRobberDict = self.displayGameScreen('ROBBER', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked - whether a road is built or not

        while(mouseClicked == False):
            for e in pygame.event.get(): 
                if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                    for hexIndex, robberCircleRect in possibleRobberDict.items():
                        if(robberCircleRect.collidepoint(e.pos)): 
                            #Add code to choose which player to rob depending on hex clicked on
                            playerToRob = self.choosePlayerToRob_display(hexIndex)

                            #Move robber to that hex and rob
                            currentPlayer.move_robber(hexIndex, self.board, playerToRob) #Player moved robber to this hex
                            mouseClicked = True #Only exit out once a correct robber spot is chosen

    
    #Function to control the choice of player to rob with display
    #Returns the choice of player to rob
    def choosePlayerToRob_display(self, hexIndex):
        #Get all spots the player can move robber to and show circles
        possiblePlayerDict = self.displayGameScreen('ROB_PLAYER', hexIndex)
        pygame.display.update()

        #If dictionary is empty return None
        if(possiblePlayerDict == {}):
            return None

        mouseClicked = False #Get player actions until a mouse is clicked - whether a road is built or not
        while(mouseClicked == False):
            for e in pygame.event.get(): 
                if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                    for playerToRob, playerCircleRect in possiblePlayerDict.items():
                        if(playerCircleRect.collidepoint(e.pos)): 
                            return playerToRob

        