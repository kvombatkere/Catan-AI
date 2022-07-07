#Settlers of Catan
#Gameplay class with pygame

from board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
import queue
import numpy as np
import sys, pygame

#Catan gameplay class definition
class catanGame():
    #Create new gameboard
    def __init__(self):
        print("Initializing Settlers of Catan Board...")
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

        #Initialize boardview object
        self.boardView = catanGameView(self.board, self)

        #Run functions to view board and vertex graph
        #self.board.printGraph()

        #Functiont to go through initial set up
        self.build_initial_settlements()

        #Display initial board
        self.boardView.displayGameScreen()
    

    #Function to initialize players + build initial settlements for players
    def build_initial_settlements(self):
        #Initialize new players with names and colors
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']
        for i in range(self.numPlayers -1):
            playerNameInput = input("Enter Player {} name: ".format(i+1))
            newPlayer = player(playerNameInput, playerColors[i])
            self.playerQueue.put(newPlayer)

        test_AI_player = heuristicAIPlayer('Random-Greedy-AI', playerColors[i+1]) #Add the AI Player last
        test_AI_player.updateAI()
        self.playerQueue.put(test_AI_player)

        playerList = list(self.playerQueue.queue)

        self.boardView.displayGameScreen() #display the initial gameScreen
        print("Displaying Initial GAMESCREEN!")

        #Build Settlements and roads of each player forwards
        for player_i in playerList: 
            if(player_i.isAI):
                player_i.initial_setup(self.board)
            
            else:
                self.build(player_i, 'SETTLE')
                self.boardView.displayGameScreen()
                
                self.build(player_i, 'ROAD')
                self.boardView.displayGameScreen()
        
        #Build Settlements and roads of each player reverse
        playerList.reverse()
        for player_i in playerList: 
            if(player_i.isAI):
                player_i.initial_setup(self.board)
                self.boardView.displayGameScreen()

            else:
                self.build(player_i, 'SETTLE')
                self.boardView.displayGameScreen()

                self.build(player_i, 'ROAD')
                self.boardView.displayGameScreen()

            #Initial resource generation
            #check each adjacent hex to latest settlement
            for adjacentHex in self.board.boardGraph[player_i.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    player_i.resources[resourceGenerated] += 1
                    print("{} collects 1 {} from Settlement".format(player_i.name, resourceGenerated))

        self.gameSetup = False

        return


    #Generic function to handle all building in the game - interface with gameView
    def build(self, player, build_flag):
        if(build_flag == 'ROAD'): #Show screen with potential roads
            if(self.gameSetup):
                potentialRoadDict = self.board.get_setup_roads(player)
            else:
                potentialRoadDict = self.board.get_potential_roads(player)

            roadToBuild = self.boardView.buildRoad_display(player, potentialRoadDict)
            if(roadToBuild != None):
                player.build_road(roadToBuild[0], roadToBuild[1], self.board)

            
        if(build_flag == 'SETTLE'): #Show screen with potential settlements
            if(self.gameSetup):
                potentialVertexDict = self.board.get_setup_settlements(player)
            else:
                potentialVertexDict = self.board.get_potential_settlements(player)
            
            vertexSettlement = self.boardView.buildSettlement_display(player, potentialVertexDict)
            if(vertexSettlement != None):
                player.build_settlement(vertexSettlement, self.board) 

        if(build_flag == 'CITY'): 
            potentialCityVertexDict = self.board.get_potential_cities(player)
            vertexCity = self.boardView.buildSettlement_display(player, potentialCityVertexDict)
            if(vertexCity != None):
                player.build_city(vertexCity, self.board) 


    #Wrapper Function to handle robber functionality
    def robber(self, player):
        potentialRobberDict = self.board.get_robber_spots()
        print("Move Robber!")

        hex_i, playerRobbed = self.boardView.moveRobber_display(player, potentialRobberDict)
        player.move_robber(hex_i, self.board, playerRobbed)


    #Function to roll dice 
    def rollDice(self):
        dice_1 = np.random.randint(1,7)
        dice_2 = np.random.randint(1,7)
        diceRoll = dice_1 + dice_2
        print("Dice Roll = ", diceRoll, "{", dice_1, dice_2, "}")

        self.boardView.displayDiceRoll(diceRoll)

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
        
        #Logic for a 7 roll
        else:
            #Implement discarding cards
            #Check for each player
            for player_i in list(self.playerQueue.queue):
                if(currentPlayer.isAI):
                    print("AI discarding resources...")
                    #TO-DO
                else:
                    #Player must discard resources
                    player_i.discardResources()

            #Logic for robber
            if(currentPlayer.isAI):
                print("AI using heuristic robber...")
                currentPlayer.heuristic_move_robber(self.board)
            else:
                self.robber(currentPlayer)
                self.boardView.displayGameScreen()#Update back to original gamescreen


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

        while (self.gameOver == False):

            #Loop for each player's turn -> iterate through the player queue
            for currPlayer in self.playerQueue.queue:

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
                    if(currPlayer.isAI):
                        #Roll Dice
                        diceNum = self.rollDice()
                        diceRolled = True
                        self.update_playerResources(diceNum, currPlayer)

                        currPlayer.move(self.board) #AI Player makes all its moves
                        #Check if AI player gets longest road/largest army and update Victory points
                        self.check_longest_road(currPlayer)
                        self.check_largest_army(currPlayer)
                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                        
                        self.boardView.displayGameScreen()#Update back to original gamescreen
                        turnOver = True

                    else: #Game loop for human players
                        for e in pygame.event.get(): #Get player actions/in-game events
                            #print(e)
                            if e.type == pygame.QUIT:
                                sys.exit(0)

                            #Check mouse click in rollDice
                            if(e.type == pygame.MOUSEBUTTONDOWN):
                                #Check if player rolled the dice
                                if(self.boardView.rollDice_button.collidepoint(e.pos)):
                                    if(diceRolled == False): #Only roll dice once
                                        diceNum = self.rollDice()
                                        diceRolled = True
                                        
                                        self.boardView.displayDiceRoll(diceNum)
                                        #Code to update player resources with diceNum
                                        self.update_playerResources(diceNum, currPlayer)

                                #Check if player wants to build road
                                if(self.boardView.buildRoad_button.collidepoint(e.pos)):
                                    #Code to check if road is legal and build
                                    if(diceRolled == True): #Can only build after rolling dice
                                        self.build(currPlayer, 'ROAD')
                                        self.boardView.displayGameScreen()#Update back to original gamescreen

                                        #Check if player gets longest road and update Victory points
                                        self.check_longest_road(currPlayer)
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                #Check if player wants to build settlement
                                if(self.boardView.buildSettlement_button.collidepoint(e.pos)):
                                    if(diceRolled == True): #Can only build settlement after rolling dice
                                        self.build(currPlayer, 'SETTLE')
                                        self.boardView.displayGameScreen()#Update back to original gamescreen
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                #Check if player wants to build city
                                if(self.boardView.buildCity_button.collidepoint(e.pos)):
                                    if(diceRolled == True): #Can only build city after rolling dice
                                        self.build(currPlayer, 'CITY')
                                        self.boardView.displayGameScreen()#Update back to original gamescreen
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                #Check if player wants to draw a development card
                                if(self.boardView.devCard_button.collidepoint(e.pos)):
                                    if(diceRolled == True): #Can only draw devCard after rolling dice
                                        currPlayer.draw_devCard(self.board)
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                                        print('Available Dev Cards:', currPlayer.devCards)

                                #Check if player wants to play a development card - can play devCard whenever after rolling dice
                                if(self.boardView.playDevCard_button.collidepoint(e.pos)):
                                        currPlayer.play_devCard(self)
                                        self.boardView.displayGameScreen()#Update back to original gamescreen
                                        
                                        #Check for Largest Army and longest road
                                        self.check_largest_army(currPlayer)
                                        self.check_longest_road(currPlayer)
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                                        print('Available Dev Cards:', currPlayer.devCards)

                                #Check if player wants to trade with the bank
                                if(self.boardView.tradeBank_button.collidepoint(e.pos)):
                                        currPlayer.initiate_trade(self, 'BANK')
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                                
                                #Check if player wants to trade with another player
                                if(self.boardView.tradePlayers_button.collidepoint(e.pos)):
                                        currPlayer.initiate_trade(self, 'PLAYER')
                                        #Show updated points and resources  
                                        print("Player:{}, Resources:{}, Points: {}".format(currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                #Check if player wants to end turn
                                if(self.boardView.endTurn_button.collidepoint(e.pos)):
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

                if(self.gameOver):
                    startTime = pygame.time.get_ticks()
                    runTime = 0
                    while(runTime < 10000): #10 second delay prior to quitting
                        runTime = pygame.time.get_ticks() - startTime

                    break
                    
                

#Initialize new game and run
newGame = catanGame()
newGame.playCatan()