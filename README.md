# Chess Engine in Python
## Overview
This is a simple chess engine written in python. 
Its strength is in the vicinity of 1200 ELO on chess.com, although it is difficult to measure it.
Currently the bot does decently in the opening, well in the middlegame and poorly in the endgame.
It searches to a depth of 3 PLY not including extensions. Deeper searches significantly slow down performance due to Python’s execution speed.  

## Running the Chess Engine
1. Clone the repository
2. To run the program simply run *Main.py*
3. Optionally modify lines 153,154 to change which colour the bot plays.

## Testing
The *Benchmark.py* program is used to check both correctness of move generation, its speed and speed of actual search. 
It evaluates itself on positions in corresponding tables in *constants.py*. To add a position for testing simply paste its fen string into one of the tables.
