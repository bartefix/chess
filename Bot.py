import time

from moves import *
from constants import *
from evaluation import *
import random
class Bot:
    def __init__(self,board):
        self.board = board



    def give_move(self,_depth):
        moves = all_legal_moves(self.board,self.board.who_to_move)
        moves_list = list(moves)

        depth = _depth

        n = len(moves)
        #colour_modifier = 1 if self.board.who_to_move == WHITE else -1

        copy_board = copy.deepcopy(self.board)
        if self.board.who_to_move == WHITE:
            best_eval = float("-inf")
            best_move = -1
            for i in range(n):
                make_move(copy_board,moves_list[i])
                eval = search(copy_board,depth)
                unmake_move(copy_board,moves_list[i])
                if eval > best_eval:
                    best_eval = eval
                    best_move = moves_list[i]
            print(evaluate_position(self.board))
            return best_move
        if self.board.who_to_move == BLACK:
            best_eval = float("inf")
            best_move = -1
            for i in range(n):
                make_move(copy_board, moves_list[i])
                eval = search(copy_board,depth)
                unmake_move(copy_board, moves_list[i])
                if eval < best_eval:
                    best_eval = eval
                    best_move = moves_list[i]
            print(evaluate_position(self.board))
            return best_move

    def benchmark(self):
        for i in range(3):
            start_time = time.perf_counter()
            count = count_positions(self.board,i+1)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f" Move: {count}, Elapsed time: {elapsed_time:.6f} seconds")
        # for i in range(3):
        #     start_time = time.perf_counter()
        #     search(self.board,i)
        #     end_time = time.perf_counter()
        #     elapsed_time = end_time - start_time
        #     print(f"Elapsed time: {elapsed_time:.6f} seconds")