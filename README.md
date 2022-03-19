# mancalaAI
DTU prject repo for Intro to AI course assignment 1. 

This project develops a game-playing AI using the material of the course. 

## About

The game of choice is Kalah (Mancala). 
The group implemented 4 algorithms to play the Human or AI vs AI. These are: 

- MiniMax
- AlphaBeta
- MCTS
- Our own algorithm we call `naive maximizer` (?)

To run the experiments we use the `run_game.py` script that runs the game without a UI and does not allow for a human player. 
To play against the AI using a Terminal UI, we run `run_game_with_ui.py`. The usage of these two scripts is explained below. 

### Implemented rules

- Board Size: 2x6
- Pebbles per pit: 4
- Game runs clockwise
- Move ending on player's house results in free turn
- Move ending on an empty pit "captures" all seeds from the opposite pit
- Player never seeds opponent's house
- If any player makes a move that results in all houses of either player being empty, the player with no available moves captures the pebbles of the opposite player and the game ends. 

## Running the game

### How to run `run_game_with_ui.py`:

To play the game using the UI we run `run_game_with_ui.py`. 
One is allowed to select the AI one wants to play against inside the game. However, we need to provide 3 arguments to the script to initialize the settings of the AI. These are: 


```bash
--heuristic HEURISTIC
                        Heuristic to use for AI player when applicable.
  -md MAX_DEPTH, --max_depth MAX_DEPTH
                        Max depth for AI player when applicable.
  -numit MCTS_NUMBER_OF_ITERATIONS, --mcts_number_of_iterations MCTS_NUMBER_OF_ITERATIONS
                        Number of iterations for AI with MCTS.
``` 

An example run can be: 

```bash
python src/run_game_with_ui.py --heuristic h1 -md 2 -numit 10
```
This will use H1 heuristic for the MiniMax or Alphabeta algorithms and will run them with max depth of 2. If one will choose the Monte Carlo Tree Search inside the UI, the algorithm will run with 10 iterations. 


Note that to run the move of the AI, just press ENTER when it is not your turn. 

### How to run `run_game.py`:

This script is used for experiments where AIs are playing against each other with different configurations.
The following arguments are expected: 


```bash
  -p0 PLAYER0, --player0 PLAYER0
                        Type of AI to play player 0
  -p1 PLAYER1, --player1 PLAYER1
                        Type of AI to play player 1
  -h0 HEURISTIC0, --heuristic0 HEURISTIC0
                        Heuristic to use for AI player 0
  -h1 HEURISTIC1, --heuristic1 HEURISTIC1
                        Heuristic to use for AI player 1
  -md0 MAX_DEPTH_0, --max_depth_0 MAX_DEPTH_0
                        Max depth for AI player 0
  -md1 MAX_DEPTH_1, --max_depth_1 MAX_DEPTH_1
                        Max depth for AI player 1
  -mcts_n0 MCTS_NUMBER_OF_IT_0, --mcts_number_of_it_0 MCTS_NUMBER_OF_IT_0
                        Number of iterations for MCTS if AI player 0
  -mcts_n1 MCTS_NUMBER_OF_IT_1, --mcts_number_of_it_1 MCTS_NUMBER_OF_IT_1
                        Number of iterations for MCTS if AI player 0
```

An example is: 

```bash
python src/run_game.py -p0 minimax -p1 alphabeta -h0 h1 -h1 h1 -md0 2 -md1 2
```

### How to run `run_experiments.py`:

Largerly the same way as `run_game.py`, but with a few extra arguments.
All available arguments are following: 


```bash
  -p0 PLAYER0, --player0 PLAYER0
                        Type of AI to play player 0
  -p1 PLAYER1, --player1 PLAYER1
                        Type of AI to play player 1
  -h0 HEURISTIC0, --heuristic0 HEURISTIC0
                        Heuristic to use for AI player 0
  -h1 HEURISTIC1, --heuristic1 HEURISTIC1
                        Heuristic to use for AI player 1
  -md0 MAX_DEPTH_0, --max_depth_0 MAX_DEPTH_0
                        Max depth for AI player 0
  -md1 MAX_DEPTH_1, --max_depth_1 MAX_DEPTH_1
                        Max depth for AI player 1
  -mcts_n0 MCTS_NUMBER_OF_IT_0, --mcts_number_of_it_0 MCTS_NUMBER_OF_IT_0
                        Number of iterations for MCTS if AI player 0
  -mcts_n1 MCTS_NUMBER_OF_IT_1, --mcts_number_of_it_1 MCTS_NUMBER_OF_IT_1
                        Number of iterations for MCTS if AI player 0
  -r REPEATS, --repeats REPEATS
                        Number of repeats to run the experiment for.
  -n NAME, --name NAME  Name the experiment
```

Compared to `run_game.py`, one must provide `-r` that is the number of games to run and `-n` which is a string with no spaces naming the experiment. 

When an experiment is run, the script will create a folder:`./experiments/<concat name of the experiment>/` and inside there `results.txt` and `args.txt` will be placed.