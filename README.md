# CatanAI
A Settler's of Catan framework built in Python with AI agents trained using deep Reinforcemen Learning. 
The GUI is implemented using ```pygame```, while the game log is currently output through the terminal to allow for easy play and testing

![Catan Board](https://github.com/kvombatkere/Catan-AI/blob/master/images/catan_gui.png)

## Framework Overview
Game functionality is implemented in the following modules:
1. ```hexTile.py``` - Implements the hexagonal tiles for the Catan board, with a complete graph representation outline for vertices and edges. Mathematical representation easy drawing of hexagonal grids and pixel math is implemented in ```hexLib.py```, adapted from  http://www.redblobgames.com/grids/hexagons/
2. ```board.py``` - Base class to implement the board, and board related functionality such as building roads, settlements and cities. 
3. ```player.py``` and ```AIPlayer.py``` - Base classes to implement player functionality. The AI Player inherits the player class and has some random heuristic capabilty
4. ```game.py``` and ```AIGame.py``` - Wrapper classes to interface game reprentation with pygame game loop

## Model Training
WIP - to be updated soon
