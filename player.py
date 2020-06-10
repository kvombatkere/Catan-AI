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

        self.maxRoadLength = 0
        self.settlementsLeft = 5
        self.roadsLeft = 15
        self.citiesLeft = 4
        self.resources = {'ORE':6, 'BRICK':16, 'WHEAT':6, 'WOOD':16, 'SHEEP':4} #Dictionary that keeps track of resource amounts

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

                #Calculate current max road length and update
                maxRoads = self.get_road_length(board)
                self.maxRoadLength = maxRoads

                print('Player {} Successfully Built a Road. MaxRoadLength: {}'.format(self.name, self.maxRoadLength))

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
        if(self.resources['WHEAT'] >= 2 and self.resources['ORE'] >= 3): #Check if player has resources available
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
        
    #Function to calculate road length for longest road calculation
    #Use both player buildgraph and board graph to compute recursively
    def get_road_length(self, board):
        roadLengths = [] #List to store road lengths from each starting edge
        for road in self.buildGraph['ROADS']: #check for every starting edge
            self.road_i_lengths = [] #List to keep track of all lengths of roads resulting from this root road
            roadCount = 0
            roadArr = []
            vertexList = []
            #print("Start road:", road)
           
            self.check_path_length(road, roadArr, roadCount, vertexList, board.boardGraph)

            road_inverted = (road[1], road[0])
            roadCount = 0
            roadArr = []
            vertexList = []
            self.check_path_length(road_inverted, roadArr, roadCount, vertexList, board.boardGraph)
                
            roadLengths.append(max(self.road_i_lengths)) #Update roadLength with max starting from this road
            #print(self.road_i_lengths)

        #print("Road Lengths:", roadLengths, max(roadLengths))
        return max(roadLengths)

    #Function to checl the path length from a current edge to all possible other vertices not yet visited by t
    def check_path_length(self, edge, edgeList, roadLength, vertexList, boardGraph):
        if(edge not in edgeList and (edge[1], edge[0]) not in edgeList):
            #Append current edge to list and increment road count
            edgeList.append(edge) #Append both orientations of the road
            roadLength += 1
            vertexList.append(edge[0])
            
            #Get new neighboring forward edges from this edge - not visited by the search yet
            road_neighbors_list = self.get_neighboring_roads(edge, boardGraph, edgeList, vertexList)
            
            #print(neighboringRoads)
            #if no neighboring roads exist append the roadLength upto this edge
            if(road_neighbors_list == []):
                #print("No new neighbors found")
                self.road_i_lengths.append(roadLength)
                return

            else:
                #check paths from left and right neighbors separately
                for neighbor_road in road_neighbors_list:
                    #print("checking neighboring edge:", neighbor_road)
                    return self.check_path_length(neighbor_road, edgeList, roadLength, vertexList, boardGraph)
        else:
            print('loop detected')
            self.road_i_lengths.append(roadLength)
            return



    #Helper function to get neighboring edges from this road that haven't already been explored
    #We want forward neighbors only
    def get_neighboring_roads(self, road_i, boardGraph, visitedRoads, visitedVertices):
        #print("Getting neighboring roads for current road:", road_i)
        newNeighbors = []
        #Use v1 and v2 to get the vertices to expand from
        v1 = road_i[0]
        v2 = road_i[1] 
        for edge in self.buildGraph['ROADS']:
            if(edge[1] in visitedVertices):
                edge = (edge[1], edge[0]) #flip the edge if the orientation is reversed

            if(edge not in visitedRoads): #If it is a new distinct edge
                if(boardGraph[v2].state['Player'] in [self, None]):#Add condition for vertex to be not colonised by anyone else
                    if(edge[0] == v2 and v2 not in visitedVertices):  #If v2 has neighbors, defined starting or finishing at v2
                        #print("Appending NEW neighbor:", edge)
                        newNeighbors.append(edge)

                    if(edge[0] == v1 and v1 not in visitedVertices):
                        newNeighbors.append(edge)

                    if(edge[1] == v2 and v2 not in visitedVertices): #If v1 has neighbors, defined starting or finishing at v2
                        newNeighbors.append((edge[1], edge[0]))

                    if(edge[1] == v1 and v1 not in visitedVertices):
                        newNeighbors.append((edge[1], edge[0]))

        return newNeighbors

        
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

    
