# CatanAI
A Settlers of Catan framework built in Python with AI agents trained using Reinforcement Learning. The goal of this project is to implement full multiplayer game functionality and use MCTS and reinforcement learning to build an AI player that can effectively explore-exploit heuristic strategies.
The GUI is implemented using ```pygame```, while the game log is currently output through the terminal to allow for easy play and testing.

![Catan Board](/images/catan_gui.png)

## Framework Overview
Game functionality is implemented in the following modules:
1. ```hexTile.py``` - Implements the hexagonal tiles for the Catan board, with a complete graph representation outline for vertices and edges. Mathematical representation easy drawing of hexagonal grids and pixel math is implemented in ```hexLib.py```, adapted from  http://www.redblobgames.com/grids/hexagons/
2. ```board.py``` - Base class to implement the board, and board related functionality such as building roads, settlements and cities. 
3. ```player.py``` and ```heuristicAIPlayer.py``` - Base classes to implement player functionality. The AI Player inherits the player class and enacts heuristic strategies
4. ```catanGame.py``` and ```AIGame.py``` - Wrapper classes to interface game representation with GUI
5. ```gameView.py``` - Graphics class implemented to interface game mechanics with pygame-based GUI.


## AI Player Model Training
The ```modelState.py``` class is implemented to store a state-action representation of the game. Vectors representing the vertices and edges on the board along with player-related features such as resources, development cards and existing buildings are used to represent the game state. Actions are implemented in a hierarchical manner, where the AI must first decide the best current strategy via reinforcement learning, and then use a heuristic implementation of that strategy to play.


## References
1. Xenou, Konstantia, Georgios Chalkiadakis, and Stergos Afantenos. "Deep Reinforcement Learning in Strategic Board Game Environments." European Conference on Multi-Agent Systems. Springer, Cham, 2018.
2. Pfeiffer, Michael. "Reinforcement learning of strategies for Settlers of Catan." Proceedings of the International Conference on Computer Games: Artificial Intelligence, Design and Education. 2004.
3. Gendre, Quentin, and Tomoyuki Kaneko. "Playing Catan with Cross-Dimensional Neural Network." International Conference on Neural Information Processing. Springer, Cham, 2020.
