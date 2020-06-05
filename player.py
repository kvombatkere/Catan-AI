#Karan Vombatkere
#Summer 2020

#Imports
from board import *
import numpy as np

#Class definition for a player
class player():
    'Class Definition for Game Player'

    #Initialize a game player, we use A, B and C to identify
    def __init__(self, playerName, playerColor):
        self.name = playerName
        self.color = playerColor
        self.victoryPoints = 0

        self.settlementsLeft = 5
        self.roadsLeft = 15
        self.citiesLeft = 4
        self.resources = {'ORE':6, 'BRICK':6, 'WHEAT':6, 'WOOD':6, 'SHEEP':4} #Dictionary that keeps track of resource amounts

        self.knightsPlayed = 0

        #Undirected Graph to keep track of which vertices and edges player has colonised
        #Every time a player's build graph is updated the gameBoardGraph must also be updated

        #Each of the 3 lists store vertex information - Roads are stores with tuples of vertex pairs
        self.buildGraph = {'ROADS':[], 'SETTLEMENTS':[], 'CITIES':[]} 

        self.devCards = None #Dev cards in possession
        #self.visibleVictoryPoints = self.victoryPoints - devCard victory points


    #function to build a road from vertex v1 to vertex v2
    def build_road(self, v1, v2, board):
        'Update buildGraph to add a road on edge v1 - v2'

        if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0): #Check if player has resources available
            if(self.roadsLeft > 0): #Check if player has roads left
                self.buildGraph['ROADS'].append((v1,v2))
                self.roadsLeft -= 1

                #Update player resources
                self.resources['BRICK'] -= 1
                self.resources['WOOD'] -= 1

                board.updateBoardGraph_road(v1, v2, self) #update the overall boardGraph
                print('Player {} Successfully Built a Road'.format(self.name))

                #TO-DO: Calculate current road length

        else:
            print("Insufficient Resources to Build Road - Need 1 BRICK, 1 WOOD")


    #function to build a settlement on vertex with coordinates vCoord
    def build_settlement(self, vCoord, board):
        'Update player buildGraph and boardgraph to add a settlement on vertex v'
        #Take input from Player on where to build settlement
            #Check if player has correct resources
                #Update player resources and boardGraph with transaction

        if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0): #Check if player has resources available
            if(self.settlementsLeft > 0): #Check if player has settlements left
                self.buildGraph['SETTLEMENTS'].append(vCoord)
                self.settlementsLeft -= 1

                #Update player resources
                self.resources['BRICK'] -= 1
                self.resources['WOOD'] -= 1
                self.resources['SHEEP'] -= 1
                self.resources['WHEAT'] -= 1
                
                self.victoryPoints += 1
                board.updateBoardGraph_settlement(vCoord, self) #update the overall boardGraph
                print('Player {} Successfully Built a Settlement'.format(self.name))

                

        else:
            print("Insufficient Resources to Build Settlement. Build Cost: 1 BRICK, 1 WOOD, 1 WHEAT, 1 SHEEP")

    #function to build a city on vertex v
    def build_city(self, vCoord, board):
        'Upgrade existing settlement to city in buildGraph'
        if(self.resources['WHEAT'] >= 2 and self.resources['ORE'] > 3): #Check if player has resources available
            if(self.citiesLeft > 0):
                self.buildGraph['CITIES'].append(vCoord)
                self.settlementsLeft += 1 #Increase number of settlements and decrease number of cities
                self.citiesLeft -=1

                #Update player resources
                self.resources['ORE'] -= 3
                self.resources['WHEAT'] -= 2
                self.victoryPoints += 1

                board.updateBoardGraph_city(vCoord, self) #update the overall boardGraph
                print('Player {} Successfully Built a City'.format(self.name))

        else:
            print("Insufficient Resources to Build City. Build Cost: 3 ORE, 2 WHEAT")
    
    #function to move robber to a specific hex and steal from a player
    def move_robber(self, hexIndex, board, player_robbed):
        'Update boardGraph with Robber'
        board.updateBoardGraph_robber(hexIndex)
        
        #Steal a random resource from other players
        self.steal_resource(player_robbed)


    #Function to steal a random resource from player_2
    def steal_resource(self, player_2):
        if(player_2 == None):
            print("No Player on this hex to Rob")
            return
        
        #Get all resources player 2 has in a list and use random list index to steal
        p2_resources = []
        for resourceName, resourceAmount in player_2.resources.items():
            p2_resources += [resourceName]*resourceAmount

        resourceIndexToSteal = np.random.randint(0, len(p2_resources))
        resourceStolen = p2_resources[resourceIndexToSteal]
        
        #Update resources of both players
        player_2.resources[resourceStolen] -= 1
        self.resources[resourceStolen] += 1
        print("Stole 1 {} from Player {}".format(resourceStolen, player_2.name))
        

        
    #function to end turn
    def end_turn():
        'Pass turn to next player and update game state'

    #function to draw a Development Card
    def draw_devCard(self):
        'Draw a random dev card from stack and update self.devcards'

    #function to play a development card
    def play_devCard():
        'Update game state'

    #function to initate a trade - with bank or other players
    def initiate_trade():
        return None


#Class Definition for Development card stack
class devCardStack():
    def __init__(self):
        'Initialize the Dev Card Stack'
        self.Knights = 15
        self.VictoryPoints = 5
        self.Monopoly = 2
        self.RoadBuilding = 2
        self.YearofPlenty = 2

    #Function to take a card from the stack
    def draw_Card():
        'Give card to player and update the stack'

    
