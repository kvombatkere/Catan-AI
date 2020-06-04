#Karan Vombatkere
#May 2020

#Imports
# 
from board import *
from player import *
import queue
import numpy as np
import sys, pygame

#Test Code
class catanGame():
    #Create new gameboard
    def __init__(self):
        self.board = catanBoard()

        #Game State variables
        self.gameOver = False 
        
        #Initialize blank player queue and initial set up of roads + settlements
        self.playerQueue = queue.Queue()
        self.build_initial_settlements()

        #Display initial board
        self.displayGameScreen(None, None)

        self.font_diceRoll = pygame.font.SysFont('cambria', 25) #dice font

        #Run test functions to view board and vertex graph
        self.board.printGraph()

        #Add functionality to add the number of players (3-4)
        #Add functionality to set up first 2 settlements and roads
    

    #Function to initialize 3 players + build initial settlements for players - hardcoded for testing
    def build_initial_settlements(self):
        #Initialize players with 2 settlements and roads
        player1 = player("A", 'black')
        player2 = player("B", 'darkslateblue')
        player3 = player("C", 'magenta4')
        self.playerQueue.put(player1)
        self.playerQueue.put(player2)
        self.playerQueue.put(player3)

        #Build initial settlements and roads hardcoded for now
        v1a = Point(x=580.0, y=400.0)
        v1b = Point(x=460.0, y=469.28)
        player1.build_settlement(v1a, self.board)
        player1.build_road(v1a, Point(x=660.0, y=400.0) , self.board)

        player1.build_settlement(v1b, self.board)
        player1.build_road(v1b, Point(x=540.0, y=469.28) , self.board)


        v2a = Point(x=460.0, y=330.72)
        v2b = Point(x=340.0, y=400.0)
        player2.build_settlement(v2a, self.board)
        player2.build_road(v2a, Point(x=420.0, y=261.44) , self.board)

        player2.build_settlement(v2b, self.board)
        player2.build_road(v2b, Point(x=300.0, y=469.28) , self.board)

        v3a = Point(x=540.0, y=192.15)
        v3b = Point(x=460.0, y=607.85)
        player3.build_settlement(v3a, self.board)
        player3.build_road(v3a, Point(x=580.0, y=261.44) , self.board)

        player3.build_settlement(v3b, self.board)
        player3.build_road(v3b, Point(x=540.0, y=607.85) , self.board)


    #Function to render basic gameplay buttons
    def displayGameButtons(self):
        #Basic GamePlay Buttons
        self.font_button = pygame.font.SysFont('cambria', 12)
        diceRollText = self.font_button.render("ROLL DICE", False, (0,0,0))
        buildRoadText = self.font_button.render("ROAD", False, (0,0,0))       
        buildSettleText = self.font_button.render("SETTLE", False, (0,0,0))
        buildCityText = self.font_button.render("CITY", False, (0,0,0))
        endTurnText = self.font_button.render("END TURN", False, (0,0,0))

        self.rollDice_button = pygame.Rect(20, 20, 80, 40)
        self.buildRoad_button = pygame.Rect(20, 70, 80, 40)
        self.buildSettlement_button = pygame.Rect(20, 120, 80, 40)
        self.buildCity_button = pygame.Rect(20, 170, 80, 40)
        self.endTurn_button = pygame.Rect(20, 220, 80, 40)

        pygame.draw.rect(self.board.screen, pygame.Color('darkgreen'), self.rollDice_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.buildRoad_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.buildSettlement_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.buildCity_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('burlywood'), self.endTurn_button) 

        self.board.screen.blit(diceRollText,(30, 30)) 
        self.board.screen.blit(buildRoadText,(30,80)) 
        self.board.screen.blit(buildSettleText,(30,130))
        self.board.screen.blit(buildCityText, (30,180))
        self.board.screen.blit(endTurnText,(30,230))


    #Function to display the gameState board - use to display intermediate build screens
    #gameScreenState specifies which type of screen is to be shown
    def displayGameScreen(self, gameScreenState, player):
        #First display all initial hexes and regular buttons
        self.board.displayInitialBoard()
        self.displayGameButtons()

        #Loop through and display all existing buildings from players build graphs
        for player_i in list(self.playerQueue.queue): #Build Settlements and roads of each player
            for existingRoad in player_i.buildGraph['ROADS']:
                self.board.draw_road(existingRoad, player_i.color)
            
            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                self.board.draw_settlement(settlementCoord, player_i.color)

            for cityCoord in player_i.buildGraph['CITIES']:
                self.board.draw_city(cityCoord, player_i.color)
        
        if(gameScreenState == 'ROAD'): #Show screen with potential roads
            potential_road_dict = self.board.get_potential_roads(player)
            return potential_road_dict

        if(gameScreenState == 'SETTLE'): #Show screen with potential settlements
            potentialVertexDict = self.board.get_potential_settlements(player)
            return potentialVertexDict

        if(gameScreenState == 'CITY'): 
            potentialVertexDict = self.board.get_potential_cities(player)
            return potentialVertexDict

        #TO-DO Add screens for robber and trades


    #Function to roll dice 
    def rollDice(self):
        dice_1 = np.random.randint(1,7)
        dice_2 = np.random.randint(1,7)
        diceRoll = dice_1 + dice_2
        print("Dice Roll = ", diceRoll, "{", dice_1, dice_2, "}")

        #Reset blue background and show dice roll
        pygame.draw.rect(self.board.screen, pygame.Color('royalblue2'), (100, 20, 50, 50)) #blue background
        diceNum = self.font_diceRoll.render(str(diceRoll), False, (0,0,0))
        self.board.screen.blit(diceNum,(110, 20)) 

        return diceRoll

    #Function to update resources for all players
    def update_playerResources(self, diceRoll):
        #First get the hex or hexes corresponding to diceRoll
        hexResourcesRolled = self.board.getHexResourceRolled(diceRoll)
        print('Resources rolled this turn:', hexResourcesRolled)

        #Check for each player, each settlement the player has
        for player_i in list(self.playerQueue.queue):
            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                for adjacentHex in self.board.boardGraph[settlementCoord].adjacentHexList: #check each adjacent hex to a settlement
                    if(adjacentHex in hexResourcesRolled): #This player gets a resource
                        resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                        player_i.resources[resourceGenerated] += 1
                        print("Player {} collects resource: {}".format(player_i.name, resourceGenerated))

            print("Player: {}, Resources: {}, Points: {}".format(player_i.name, player_i.resources, player_i.victoryPoints))
            print(player_i.buildGraph['SETTLEMENTS'], player_i.roadsLeft)
        return None

    #Function to control build-road action with display
    def buildRoad_display(self, currentPlayer):
        #Get all spots the player can build a road and display thin lines
        roadsPossibleDict = self.displayGameScreen('ROAD', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked - whether a road is built or not

        while(mouseClicked == False):
            for e in pygame.event.get(): 
                if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                    for road, roadRect in roadsPossibleDict.items():
                        if(roadRect.collidepoint(e.pos)): 
                            currentPlayer.build_road(road[0], road[1], self.board)
                    
                    mouseClicked = True

    #Function to control build-setttlment action with display
    def buildSettlement_display(self, currentPlayer):
        #Get all spots the player can build a road and display thin lines
        verticesPossibleDict = self.displayGameScreen('SETTLE', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked - whether a road is built or not

        while(mouseClicked == False):
            for e in pygame.event.get(): 
                if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                    for vertex, vertexRect in verticesPossibleDict.items():
                        if(vertexRect.collidepoint(e.pos)): 
                            currentPlayer.build_settlement(vertex, self.board)
                    
                    mouseClicked = True

    #Function to control the build-city action with display
    def buildCity_display(self, currentPlayer):
        #Get all spots the player can build a road and display thin lines
        verticesPossibleDict = self.displayGameScreen('CITY', currentPlayer) 
        pygame.display.update()

        mouseClicked = False #Get player actions until a mouse is clicked - whether a road is built or not

        while(mouseClicked == False):
            for e in pygame.event.get(): 
                if(e.type == pygame.MOUSEBUTTONDOWN): #Exit this loop on mouseclick
                    for vertex, vertexRect in verticesPossibleDict.items():
                        if(vertexRect.collidepoint(e.pos)): 
                            currentPlayer.build_city(vertex, self.board)
                    
                    mouseClicked = True


    #Function that runs the main game loop with all players and pieces
    def playCatan(self):
        #self.board.displayBoard() #Display updated board

        #While gameOver = False
        while (self.gameOver == False):

            #Loop for each player's turn -> iterate through the 
            for currPlayer in self.playerQueue.queue:
                print("Current Player:", currPlayer.name)

                turnOver = False #boolean to keep track of turn
                diceRolled = False  #Boolean for dice roll status
                while(turnOver == False):

                    for e in pygame.event.get(): #Get player actions/in-game events
                        #print(e)
                        if e.type == pygame.QUIT:
                            sys.exit(0)

                        #Check mouse click in rollDice
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.rollDice_button.collidepoint(e.pos)):
                                if(diceRolled == False): #Only roll dice once
                                    diceNum = self.rollDice()
                                    diceRolled = True

                                    #Code to update player resources with diceNum
                                    self.update_playerResources(diceNum)

                        #Check if player wants to build road
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.buildRoad_button.collidepoint(e.pos)):
                                #Code to check if road is legal and build
                                if(diceRolled == True): #Can only build after rolling dice
                                    self.buildRoad_display(currPlayer)
                                    self.displayGameScreen(None, None)#Update back to original gamescreen


                        #Check if player wants to build settlement
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.buildSettlement_button.collidepoint(e.pos)):
                                if(diceRolled == True): #Can only build settlement rolling dice
                                    self.buildSettlement_display(currPlayer)
                                    self.displayGameScreen(None, None)#Update back to original gamescreen

                        #Check if player wants to build city
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.buildCity_button.collidepoint(e.pos)):
                                if(diceRolled == True): #Can only build settlement rolling dice
                                    self.buildCity_display(currPlayer)
                                    self.displayGameScreen(None, None)#Update back to original gamescreen


                        #Check if player wants to end turn
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.endTurn_button.collidepoint(e.pos)):
                                if(diceRolled == True): #Can only end turn after rolling dice
                                    print("Ending Turn!")
                                    turnOver = True

                        #Update the display
                        #self.displayGameScreen(None, None)
                        pygame.display.update()   
                    
                
            #Player.action() -> Update player graph and Vertex graph
            
            #Proceed to nextplayer turn
        

#Initialize new game and run
newGame = catanGame()
newGame.playCatan()