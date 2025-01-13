import time

from moves import *
from constants import *
from evaluation import *
import random
class Bot:
    def __init__(self,board):
        self.board = board



    def give_move(self):
        moves = all_legal_moves(self.board,self.board.who_to_move)
        moves_list = list(moves)

        depth = 1

        n = len(moves)
        #colour_modifier = 1 if self.board.who_to_move == WHITE else -1
        if self.board.who_to_move == WHITE:
            best_eval = float("-inf")
            best_move = -1
            for i in range(n):
                copy_board = copy.deepcopy(self.board)
                make_move(copy_board,moves_list[i])
                eval = search(copy_board,depth)
                if eval > best_eval:
                    best_eval = eval
                    best_move = moves_list[i]
            print(evaluate_position(self.board))
            return best_move
        if self.board.who_to_move == BLACK:
            best_eval = float("inf")
            best_move = -1
            for i in range(n):
                copy_board = copy.deepcopy(self.board)
                make_move(copy_board, moves_list[i])
                eval = search(copy_board,depth)
                if eval < best_eval:
                    best_eval = eval
                    best_move = moves_list[i]
            print(evaluate_position(self.board))
            return best_move

    def benchmark(self):
        for i in range(5):
            start_time = time.perf_counter()
            count = count_positions(self.board, i)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f" Num pos: {count}, Elapsed time: {elapsed_time:.6f} seconds")
        # for i in range(3):
        #     start_time = time.perf_counter()
        #     search(self.board,i)
        #     end_time = time.perf_counter()
        #     elapsed_time = end_time - start_time
        #     print(f"Elapsed time: {elapsed_time:.6f} seconds")