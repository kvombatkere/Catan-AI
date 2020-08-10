#Karan Vombatkere
#Summer 2020

#Imports
from board import *
from player import *
from AIPlayer import *
import queue
import numpy as np
import sys, pygame
import matplotlib.pyplot as plt

#Test Code
class catanGame():
    #Create new gameboard
    def __init__(self):
        print("Initializing Catan...")
        self.board = catanBoard()

        #Game State variables
        self.gameOver = False
        self.maxPoints = 10
        self.numPlayers = 0

        #Dictionary to keep track of dice statistics
        self.diceStats = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
        self.diceStats_list = []

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
        #self.displayGameScreen(None, None)
        #Run functions to view board and vertex graph
        #self.board.printGraph()
        self.playCatan()

        #Plot diceStats histogram
        plt.hist(self.diceStats_list, bins = 11)
        plt.show()

        return None
    

    #Function to initialize players + build initial settlements for players
    def build_initial_settlements(self):
        #Initialize new players with names and colors
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']
        for i in range(self.numPlayers):
            playerNameInput = input("Enter AI Player {} name: ".format(i+1))
            newPlayer = AI_Player(playerNameInput, playerColors[i])
            newPlayer.updateAI()
            self.playerQueue.put(newPlayer)

        playerList = list(self.playerQueue.queue)

        #Build Settlements and roads of each player forwards
        for player_i in playerList: 
            player_i.initial_setup(self.board)
            pygame.event.pump()
            self.displayGameScreen()
            pygame.time.delay(1000)


        #Build Settlements and roads of each player reverse
        playerList.reverse()
        for player_i in playerList: 
            player_i.initial_setup(self.board)
            pygame.event.pump()
            self.displayGameScreen()
            pygame.time.delay(1000)
            
            print("Player {} starts with {} resources".format(player_i.name, len(player_i.setupResources)))

            #Initial resource generation
            #check each adjacent hex to latest settlement
            for adjacentHex in self.board.boardGraph[player_i.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    player_i.resources[resourceGenerated] += 1
                    print("{} collects 1 {} from Settlement".format(player_i.name, resourceGenerated))
        
        pygame.time.delay(20000)
        self.gameSetup = False

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

        pygame.draw.rect(self.board.screen, pygame.Color('darkgreen'), self.rollDice_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.buildRoad_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.buildSettlement_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.buildCity_button)
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.devCard_button)
        pygame.draw.rect(self.board.screen, pygame.Color('gray33'), self.playDevCard_button) 
        pygame.draw.rect(self.board.screen, pygame.Color('burlywood'), self.endTurn_button) 

        self.board.screen.blit(diceRollText,(30, 20)) 
        self.board.screen.blit(buildRoadText,(30,80)) 
        self.board.screen.blit(buildSettleText,(30,130))
        self.board.screen.blit(buildCityText, (30,180))
        self.board.screen.blit(devCardText, (30,230))
        self.board.screen.blit(playDevCardText, (30,280))
        self.board.screen.blit(endTurnText,(30,340))

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
    def displayGameScreen(self):
        #First display all initial hexes and regular buttons
        self.board.displayInitialBoard()
        self.displayGameButtons()
        self.displayRobber()

        #Loop through and display all existing buildings from players build graphs
        for player_i in list(self.playerQueue.queue): #Build Settlements and roads of each player
            for existingRoad in player_i.buildGraph['ROADS']:
                #print("displaying roads for:", player_i.name)
                self.board.draw_road(existingRoad, player_i.color)
            
            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                #print("displaying buildings for:", player_i.name)
                self.board.draw_settlement(settlementCoord, player_i.color)

            for cityCoord in player_i.buildGraph['CITIES']:
                self.board.draw_city(cityCoord, player_i.color)
        
        pygame.display.update()
        return
        


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
                            print("{} collects 1 {} from Settlement".format(player_i.name, resourceGenerated))
                
                #Check each City the player has
                for cityCoord in player_i.buildGraph['CITIES']:
                    for adjacentHex in self.board.boardGraph[cityCoord].adjacentHexList: #check each adjacent hex to a settlement
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False): #This player gets a resource if hex is adjacent and no robber
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 2
                            print("{} collects 2 {} from City".format(player_i.name, resourceGenerated))

                print("Player:{}, Resources:{}, Points: {}".format(player_i.name, player_i.resources, player_i.victoryPoints))
                #print('Dev Cards:{}'.format(player_i.devCards))
                #print("RoadsLeft:{}, SettlementsLeft:{}, CitiesLeft:{}".format(player_i.roadsLeft, player_i.settlementsLeft, player_i.citiesLeft))
                print('MaxRoadLength:{}, LongestRoad:{}\n'.format(player_i.maxRoadLength, player_i.longestRoadFlag))
        
        else:
            if(currentPlayer.isAI):
                print("AI doesn't steal yet! :)")
            else:
                self.moveRobber_display(currentPlayer)
                self.displayGameScreen(None, None)#Update back to original gamescreen

    #function to check if a player has the longest road - after building latest road
    def check_longest_road(self, player_i):
        if(player_i.maxRoadLength >= 5): #Only eligible if road length is at least 5
            longestRoad = True
            for p in list(self.playerQueue.queue):
                if(p.maxRoadLength >= player_i.maxRoadLength and p != player_i): #Check if any other players have a longer road
                    longestRoad = False
            
            if(longestRoad and player_i.longestRoadFlag == False): #if player_i takes longest road and didn't already have longest road
                #Set previous players flag to false and give player_i the longest road points
                prevPlayer = ''
                for p in list(self.playerQueue.queue):
                    if(p.longestRoadFlag):
                        p.longestRoadFlag = False
                        p.victoryPoints -= 2
                        prevPlayer = 'from Player ' + p.name
    
                player_i.longestRoadFlag = True
                player_i.victoryPoints += 2

                print("Player {} takes Longest Road {}".format(player_i.name, prevPlayer))

    #function to check if a player has the largest army - after playing latest knight
    def check_largest_army(self, player_i):
        if(player_i.knightsPlayed >= 3): #Only eligible if at least 3 knights are player
            largestArmy = True
            for p in list(self.playerQueue.queue):
                if(p.knightsPlayed >= player_i.knightsPlayed and p != player_i): #Check if any other players have more knights played
                    largestArmy = False
            
            if(largestArmy and player_i.largestArmyFlag == False): #if player_i takes largest army and didn't already have it
                #Set previous players flag to false and give player_i the largest points
                prevPlayer = ''
                for p in list(self.playerQueue.queue):
                    if(p.largestArmyFlag):
                        p.largestArmyFlag = False
                        p.victoryPoints -= 2
                        prevPlayer = 'from Player ' + p.name
    
                player_i.largestArmyFlag = True
                player_i.victoryPoints += 2

                print("Player {} takes Largest Army {}".format(player_i.name, prevPlayer))



    #Function that runs the main game loop with all players and pieces
    def playCatan(self):
        #self.board.displayBoard() #Display updated board
        numTurns = 0
        while (self.gameOver == False):
            #Loop for each player's turn -> iterate through the player queue
            for currPlayer in self.playerQueue.queue:
                numTurns += 1
                print("---------------------------------------------------------------------------")
                print("Current Player:", currPlayer.name)

                turnOver = False #boolean to keep track of turn
                diceRolled = False  #Boolean for dice roll status
                
                #Update Player's dev card stack with dev cards drawn in previous turn and reset devCardPlayedThisTurn
                currPlayer.updateDevCards()
                currPlayer.devCardPlayedThisTurn = False

                while(turnOver == False):

                    #TO-DO: Add logic for AI Player to move
                    #TO-DO: Add option of AI Player playing a dev card prior to dice roll
                    
                    #Roll Dice and update player resources and dice stats
                    pygame.event.pump()
                    diceNum = self.rollDice()
                    diceRolled = True
                    self.update_playerResources(diceNum, currPlayer)
                    self.diceStats[diceNum] += 1
                    self.diceStats_list.append(diceNum)

                    currPlayer.move(self.board) #AI Player makes all its moves
                    #Check if AI player gets longest road and update Victory points
                    self.check_longest_road(currPlayer)
                    print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                    
                    self.displayGameScreen()#Update back to original gamescreen
                    pygame.time.delay(300)
                    turnOver = True
                    
                    #Check if game is over
                    if currPlayer.victoryPoints >= self.maxPoints:
                        self.gameOver = True
                        self.turnOver = True
                        print("====================================================")
                        print("PLAYER {} WINS IN {} TURNS!".format(currPlayer.name, numTurns))
                        print(self.diceStats)
                        print("Exiting game in 10 seconds...")
                        pygame.time.delay(30000)
                        break

                if(self.gameOver):
                    startTime = pygame.time.get_ticks()
                    runTime = 0
                    while(runTime < 10000): #10 second delay prior to quitting
                        runTime = pygame.time.get_ticks() - startTime

                    break
                    
                

#Initialize new game and run
newGame = catanGame()