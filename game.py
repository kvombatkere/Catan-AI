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

        #Basic GamePlay Buttons
        self.rollDice_button = pygame.Rect(20, 20, 50, 50)
        self.buildRoad_button = pygame.Rect(20, 80, 50, 50)
        self.endTurn_button = pygame.Rect(20, 140, 50, 50)

        pygame.draw.rect(self.board.screen, [255, 0, 0], self.rollDice_button) 
        pygame.draw.rect(self.board.screen, [0, 255, 0], self.buildRoad_button) 
        pygame.draw.rect(self.board.screen, [120, 200, 120], self.endTurn_button) 

        
        #Run test functions to view board and vertex graph
        self.board.printGraph()
        

        #Add functionality to add the number of players (3-4)
        self.playerQueue = queue.Queue()
        player1 = player("A", 'maroon1')
        player2 = player("B", 'skyblue1')
        player3 = player("C", 'darkorange1')
        self.playerQueue.put(player1)
        self.playerQueue.put(player2)
        self.playerQueue.put(player3)

        #Add functionality to set up first 2 settlements and roads
        


    #Function to roll dice and update resources for all players
    def rollDice(self):
        dice_1 = np.random.randint(1,7)
        dice_2 = np.random.randint(1,7)
        print("Dice Roll = ", dice_1, dice_2)
        return dice_1 + dice_2


    #Function that runs the main game loop with all players and pieces
    def playCatan(self):
        self.board.displayBoard() #Display updated board

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


                        #Check if player wants to build road
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.buildRoad_button.collidepoint(e.pos)):
                                #Code to check if road is legal and build
                                if(diceRolled == True): #Can only build after rolling dice
                                    if(currPlayer.resources['BRICK'] > 0 and currPlayer.resources['WOOD'] > 0):
                                        print("Building Road..")
                                        v1 = Point(x=580.0, y=400.0)
                                        v2 = Point(x=540.0, y=330.72)
                                        currPlayer.build_road(v1, v2)
                                        self.board.draw_road(((v1.x,v1.y),(v2.x, v2.y)), currPlayer.color)
                                        #Get all spots the player can build a road


                        #Check if player wants to build settlement

                        #Check if player wants to end turn
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.endTurn_button.collidepoint(e.pos)):
                                if(diceRolled == True): #Can only end turn after rolling dice
                                    print("Ending Turn!")
                                    turnOver = True

                        #Update the display
                        pygame.display.update()   
                    
                
            #Player.action() -> Update player graph and Vertex graph
            
            #Proceed to nextplayer turn
        

#Initialize new game and run
newGame = catanGame()
newGame.playCatan()