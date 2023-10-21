# Mancala Game
This is a Python implementation of the popular board game Mancala, which is a two-player turn-based strategy game. 
In the game, players take turns picking up all the stones in one of their pockets and sowing them one by one in the 
succeeding pockets, including their own mancala, but excluding the opponent's mancala. The game ends when one player 
has no more stones in their pockets. The player with the most stones in their mancala at the end of the game wins.

The code consists of several classes and functions:

`PocketName`: defines constants used to represent the pockets and mancalas of the game board.

`GameState`: represents the state of the game, including the game board, whose turn it is, whether stealing is allowed, 
and who the winner is (if any).

`Player`: an abstract class that defines the basic interface for a player of the game.

`Human`: a concrete implementation of Player that allows a human to play the game.

`Machine`: a concrete implementation of Player that uses the minimax algorithm with alpha-beta pruning to make 
moves in the game.

`static_eval`: a function that evaluates the static value of a given game state.

`minimax`: an implementation of the minimax algorithm for determining the best move to make in a given game state.

`minimax_alpha_beta`: an implementation of the minimax algorithm with alpha-beta pruning for determining the best 
move to make in a given game state.

## 📏 Rules of the Game
Mancala is a two-player strategy game that is played on a board with two rows of six holes, or pits, in each row. 
At the beginning of the game, four stones are placed in each of the twelve holes, for a total of 48 stones.

Each player controls the six holes on their side of the board, and their goal is to collect as many stones as possible
in their "mancala", which is the large pit to their right.

Players take turns moving the stones from one of their holes, dropping one stone in each hole they pass over, including
their own mancala, but not their opponent's. If the last stone dropped lands in the player's mancala,
they get to take another turn.

The game ends when one player has no more stones in their holes, at which point the other player gets to move any
remaining stones from their side into their mancala. The player with the most stones in their mancala at the end
of the game is the winner.

## 🎮 How to Play
To play the game, simply run the mancala.py script in your terminal or command prompt. The game will prompt you to enter
the number of the hole you want to move from, and it will show you the resulting board state after each move.

The game includes a simple AI opponent that makes random moves, so you can play against the computer if you don't have
a friend to play with.

### Example of Usage 

To start a game between a human player and a machine player with difficulty level easy level and material_advantage as
eval_function, run the following code:

```python
from game import human_machine_game, machine_level
from aiEngine import extra_turn

# Play against the machine at level 6 (hard difficulty)
# with extra_turn evaluation function

human_machine_game(machine_level, extra_turn)

```

This will start the game and allow the human player to enter moves through the console, while the machine player uses
minimax with alpha-beta pruning to make its moves. The game will continue until one player wins, and the final board
configuration and the winning player will be displayed.

## Dependencies
This implementation of Mancala requires Python 3 and uses the built-in random module for the AI opponent.

## 🗓️ Future Improvements
Possible future improvements to the game could include a more sophisticated AI opponent that uses a heuristic to make 
better moves, a graphical user interface using a library like Pygame, or the ability to play the game over a network 
with a friend.

🏗️ Contributions and suggestions for improvements are welcome!