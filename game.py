from board import *
from player import *
import queue
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
        #self.board.printGraph()
        

        #Add functionality to add the number of players (3-4)
        self.playerQueue = queue.Queue()
        player1 = player("A")
        player2 = player("B")
        player3 = player("C")
        self.playerQueue.put(player1)
        self.playerQueue.put(player2)
        self.playerQueue.put(player3)

        print(self.playerQueue)
        #Add functionality to set up first 2 settlements and roads


    #Function that runs the main game loop with all players and pieces
    def playCatan(self):
        
        #While gameOver = False
        while (self.gameOver == False):

            #Loop for each player's turn ->
            for currPlayer in self.playerQueue.queue:
                print("Current Player:", currPlayer.playerName)

                turnOver = False
                while(turnOver == False):

                    for e in pygame.event.get():
                        #print(e)
                        if e.type == pygame.QUIT:
                            sys.exit(0)

                        #Check mouse click in rollDice
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.rollDice_button.collidepoint(e.pos)):
                                print("Rolling Dice..")
                                #Code to update player resources

                        #Check if player wants to build road
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.buildRoad_button.collidepoint(e.pos)):
                                print("Building Road..")
                                #Code to update player resources

                        #Check if player wants to build settlement

                        #Check if player wants to end turn
                        if(e.type == pygame.MOUSEBUTTONDOWN):
                            if(self.endTurn_button.collidepoint(e.pos)):
                                print("Ending Turn!")

                                turnOver = True

                    self.board.displayBoard() #Display updated board
                
            #Player.action() -> Update player graph and Vertex graph
            
            #Proceed to nextplayer turn
        

#Initialize new game and run
newGame = catanGame()
newGame.playCatan()