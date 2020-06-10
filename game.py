#Karan Vombatkere
#Summer 2020

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
        print("Initializing Catan...")
        self.board = catanBoard()

        #Game State variables
        self.gameOver = False
        self.maxPoints = 8
        self.numPlayers = 0

        while(self.numPlayers not in [3,4]): #Only accept 3 and 4 player games
            try:
                self.numPlayers = int(input("Enter Number of Players (3 or 4):"))
            except:
                print("Please input a valid number")

        print("Initializing game with {} players...".format(self.numPlayers))
        print("Note that Player 1 goes first, Player 2 second and so forth.")
        
        #Initialize blank player queue and initial set up of roads + settlements
        self.playerQueue = queue.Queue(self.numPlayers)
        self.gameSetup = True #Boolean to take care of setup phase

        self.font_button = pygame.font.SysFont('cambria', 12)
        self.font_diceRoll = pygame.font.SysFont('cambria', 25) #dice font
        self.font_Robber = pygame.font.SysFont('arialblack', 50) #robber font


        #Functiont to go through initial set up
        self.build_initial_settlements()

        #Display initial board
        self.displayGameScreen(None, None)
    
        #Run functions to view board and vertex graph
        #self.board.printGraph()
    

    #Function to initialize players + build initial settlements for players
    def build_initial_settlements(self):
        #Initialize new players with names and colors
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']
        for i in range(self.numPlayers):
            playerNameInput = input("Enter Player {} name: ".format(i+1))
            newPlayer = player(playerNameInput, playerColors[i])
            self.playerQueue.put(newPlayer)

        playerList = list(self.playerQueue.queue)

        self.displayGameScreen(None, None) #display the initial gameScreen

        #Build Settlements and roads of each player forwards
        for player_i in playerList: 
            self.buildSettlement_display(player_i)
            self.displayGameScreen(None, None)

            self.buildRoad_display(player_i)
            self.displayGameScreen(None, None)

        #Build Settlements and roads of each player reverse
        playerList.reverse()
        for player_i in playerList: 
            self.buildSettlement_display(player_i)
            self.displayGameScreen(None, None)

            #Initial resource generation
            #check each adjacent hex to latest settlement
            for adjacentHex in self.board.boardGraph[player_i.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    player_i.resources[resourceGenerated] += 1
                    print("Player {} collects 1 {} from Settlement".format(player_i.name, resourceGenerated))

            self.buildRoad_display(player_i)
            self.displayGameScreen(None, None)

        self.gameSetup = False

    #Function to render basic gameplay buttons
    def displayGameButtons(self):
        #Basic GamePlay Buttons
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

    #Function to display robber
    def displayRobber(self):
        #Robber text
        robberText = self.font_Robber.render("R", False, (0,0,0))
        #Get the coordinates for the robber
        for hexTile in self.board.hexTileDict.values():
            if(hexTile.robber):
                robberCoords = hexTile.pixelCenter

        self.board.screen.blit(robberText, (robberCoords.x -20,robberCoords.y-35)) 


    #Function to display the gameState board - use to display intermediate build screens
    #gameScreenState specifies which type of screen is to be shown
    def displayGameScreen(self, gameScreenState, player):
        #First display all initial hexes and regular buttons
        self.board.displayInitialBoard()
        self.displayGameButtons()
        self.displayRobber()

        #Loop through and display all existing buildings from players build graphs
        for player_i in list(self.playerQueue.queue): #Build Settlements and roads of each player
            for existingRoad in player_i.buildGraph['ROADS']:
                self.board.draw_road(existingRoad, player_i.color)
            
            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                self.board.draw_settlement(settlementCoord, player_i.color)

            for cityCoord in player_i.buildGraph['CITIES']:
                self.board.draw_city(cityCoord, player_i.color)
        
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
    def update_playerResources(self, diceRoll, currentPlayer):
        if(diceRoll != 7): #Collect resources if not a 7
            #First get the hex or hexes corresponding to diceRoll
            hexResourcesRolled = self.board.getHexResourceRolled(diceRoll)
            #print('Resources rolled this turn:', hexResourcesRolled)

            #Check for each player
            for player_i in list(self.playerQueue.queue):
                #Check each settlement the player has
                for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                    for adjacentHex in self.board.boardGraph[settlementCoord].adjacentHexList: #check each adjacent hex to a settlement
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False): #This player gets a resource if hex is adjacent and no robber
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 1
                            print("Player {} collects 1 {} from Settlement".format(player_i.name, resourceGenerated))
                
                #Check each City the player has
                for cityCoord in player_i.buildGraph['CITIES']:
                    for adjacentHex in self.board.boardGraph[cityCoord].adjacentHexList: #check each adjacent hex to a settlement
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False): #This player gets a resource if hex is adjacent and no robber
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 2
                            print("Player {} collects 2 {} from City".format(player_i.name, resourceGenerated))

                print("Player:{}, Resources:{}, Points: {}".format(player_i.name, player_i.resources, player_i.victoryPoints))
                print("RoadsLeft:{}, SettlementsLeft:{}, CitiesLeft:{}, MaxRoadLength: {}\n".format(player_i.roadsLeft, player_i.settlementsLeft, player_i.citiesLeft,player_i.maxRoadLength))
        
        else:
            self.moveRobber_display(currentPlayer)
            self.displayGameScreen(None, None)#Update back to original gamescreen

            #TO-DO: Add stealing functionality for robber

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

    #Function that runs the main game loop with all players and pieces
    def playCatan(self):
        #self.board.displayBoard() #Display updated board

        while (self.gameOver == False):

            #Loop for each player's turn -> iterate through the player queue
            for currPlayer in self.playerQueue.queue:
                if(self.gameOver):
                    startTime = pygame.time.get_ticks()
                    runTime = 0
                    while(runTime < 10000): #10 second delay prior to quitting
                        runTime = pygame.time.get_ticks() - startTime

                    break

                print("---------------------------------------------------------------------------")
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
                                    self.update_playerResources(diceNum, currPlayer)

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
                                    turnOver = True  #Update flag to nextplayer turn

                        #Update the display
                        #self.displayGameScreen(None, None)
                        pygame.display.update()

                    #Check if game is over
                    if currPlayer.victoryPoints >= self.maxPoints:
                        self.gameOver = True
                        self.turnOver = True
                        print("====================================================")
                        print("PLAYER {} WINS!".format(currPlayer.name))
                        print("Exiting game in 10 seconds...")
                        break
                    
                
        

#Initialize new game and run
newGame = catanGame()
newGame.playCatan()