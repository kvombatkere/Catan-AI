#Karan Vombatkere
#May 2020

#Imports

#Class definition for a player
class player():
    'Class Definition for Game Player'

    #Initialize a game player, we use A, B and C to identify
    def __init__(self, playerName, playerColor):
        self.name = playerName
        self.color = playerColor
        self.victoryPoints = 0
        self.visibleVictoryPoints = 0

        self.settlementsLeft = 5
        self.roadsLeft = 15
        self.citiesLeft = 4
        self.resources = {'ORE':3, 'BRICK':1, 'WHEAT':4, 'WOOD':1, 'SHEEP':4} #Dictionary that keeps track of resource amounts

        self.knightsPlayed = 0

        #Undirected Graph to keep track of which vertices and edges player has colonised
        #Every time a player's build graph is updated the gameBoardGraph must also be updated

        #Each of the 3 lists store vertex information - Roads are stores with tuples of vertex pairs
        self.buildGraph = {'ROADS':[], 'SETTLEMENTS':[], 'CITIES':[]} 

        self.devCards = None #Dev cards in possession

    #function to update player resources based on dice roll
    def update_resources(self, diceRoll):
        'Update resource amount of players'


    #function to build a settlement on vertex v
    def build_settlement(self, v):
        'Update buildGraph to add a settlement on vertex v'
        #Take input from Player on where to build settlement
        #Check if valid location (Does this player have a road leading upto settlement)
            #Check if player has correct resources
                #Update player resources and boardGraph with transaction

        self.buildGraph['SETTLEMENTS'].append(v)
        self.settlementsLeft -= 1

    #Function to get a list of available vertices for settlements


    #function to build a road from vertex v1 to vertex v2
    def build_road(self, v1, v2):
        'Update buildGraph to add a road on edge v1 - v2'
        self.buildGraph['ROADS'].append((v1,v2))
        self.roadsLeft -= 1

        #Update player resources
        self.resources['BRICK'] -= 1
        self.resources['WOOD'] -= 1

    #function to build a city on vertex v
    def build_city(self, v):
        'Upgrade existing settlement to city in buildGraph'
    
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

    
