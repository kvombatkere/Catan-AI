#Karan Vombatkere
#May 2020

#Imports

#Class definition for a player
class player():
    'Class Definition for Game Player'

    #Initialize a game player
    def __init__(self):
        self.victoryPoints = 0
        self.visibleVictoryPoints = 0

        self.settlementsLeft = 5
        self.roadsLeft = 15
        self.citiesLeft = 4
        self.resources = {} #Dictionary that keeps track of resource amounts

        self.knightsPlayed = 0

        #Undirected Graph to keep track of which vertices and edges player has colonised
        #Every time a player's build graph is updated the gameBoardGraph must also be updated
        self.buildGraph = None 

        self.devCards = None #Dev cards in possession

    #function to generate random dice roll
    def roll_dice():
        'Update resource amounts of all players'

    #function to build a settlement on vertex v
    def build_settlement(self, v):
        'Update buildGraph to add a settlement on vertex v'

    #function to build a road from vertex v1 to vertex v2
    def build_road(self, v1, v2):
        'Update buildGraph to add a road on edge v1 - v2'

    #function to build a city on vertex v
    def build_city(self, v):
        'Upgrade existing settlement to city in buildGraph'

    #function to draw a Development Card
    def draw_devCard(self):
        'Draw a random dev card from stack and update self.devcards'
    
    #function to end turn
    def end_turn():
        'Pass turn to next player and update game state'

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

    
