# Connect 4 Game AI Project

This repository contains an AI project for playing the Connect 4 game against a Myopic player, and the AI is implemented using a Game Tree-based search. The goal is to create an AI player that can beat the Myopic player.

## About Connect 4

Connect 4 is a two-player connection game in which the players choose a color and then take turns dropping colored discs into a grid. The objective is to connect four of one's own discs of the same color next to each other vertically, horizontally, or diagonally before Ir opponent.

## Project Components

### Myopic Player

The Myopic player is the opponent in the game. It looks only one move ahead before choosing the best action.

### Game Tree-Based AI

The Game Tree-based AI is the AI player which is implemented. It looks ahead 5 moves in the game tree and uses alpha-beta pruning to make decisions.

### Evaluation Functions

Implementing two different evaluation functions and compare them based on the number of games won (out of 50 games) and the average number of moves before each win.

### Move Ordering Heuristic

Implementing a move ordering heuristic and observe any reduction in total recursive function calls or a reduction in the average time needed to beat the Myopic player.

### Cut-Off Depth

Initially, the AI will look 3 moves ahead for faster performance. Later, I will increase the depth to 5.

## Requirements

The project is implemented in Python and makes use of the `testcase.csv` file.

## Report and Findings

The report include:
- Details of the evaluation functions I considered.
- A comparison of the different evaluation functions based on the number of games won and the average number of moves before winning.
- Observations on the impact of implementing alpha-beta pruning.
- Insights from the move ordering heuristic.
- Results of increasing the cut-off depth to 5.

