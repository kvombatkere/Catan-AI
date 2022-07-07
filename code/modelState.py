#Settlers of Catan
#Model state class for AI training 
# TO-DO

from board import *
from catanGame import *
from player import *
from heuristicAIPlayer import *

class modelState():
    '''Define the variables needed by the RL model using a state and action object
    STATE: 
    Vertices: Array of length 54, use 0 for empty, -1/-2 for adversary, +1/+2 for self (settlements/cities)
    Edges/Roads: Array of length ___, use 0 for empty, -1 for adversary, +1 for self
    Victory Points: Array of length num_players, use value between 0 and 10
    HexTiles: Tuple array with resource and number
    NumPlayerCards: Array of length num_players, with number of total cards each player has - dev cards and resource cards
    Robber location: Current location of robber - hexTile

    ACTIONS:(under resource constraints)
    Build: Build City, Settlement, Road 
    Draw Dev Card: Draw a development card
    Play Dev Card: Play a development card
    Trade: Trade with Bank (Port option included) or with other players
    '''
    def __init__(self, catan_game):
        
        self.vertexState = [0]*54
        self.edgeState = [0]

        self.actionList = []

        print("Array length", len(self.vertexState))



a = modelState()
