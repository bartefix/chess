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
        print(moves_list)
        depth = _depth
        n = len(moves)
        #colour_modifier = 1 if self.board.who_to_move == WHITE else -1
        alpha = float("-inf")
        beta = float("inf")
        copy_board = copy.deepcopy(self.board)
        eval,best_move = search(copy_board,depth,alpha,beta)
        print(f"Best move: {best_move}, eval: {eval}")
        return best_move
        if self.board.who_to_move == WHITE:
            best_eval = float("-inf")
            best_move = -1
            for i in range(n):
                make_move(copy_board,moves_list[i])
                eval,path = search(copy_board,depth,alpha,beta)
                unmake_move(copy_board,moves_list[i])
                print(path)
                print(f"Depth: {depth} - After move: {moves_list[i].get_stockfish_format()}, eval: {eval}")
                if eval >= best_eval:
                    best_eval = eval
                    best_move = moves_list[i]
                # alpha = max(alpha, eval)
                # if alpha >= beta:
                #     break
            #print(evaluate_position(self.board))
            print("Best move: ",best_move)
            return best_move
        if self.board.who_to_move == BLACK:
            best_eval = float("inf")
            best_move = -1
            for i in range(n):
                make_move(copy_board, moves_list[i])
                eval,path = search(copy_board,depth,alpha,beta)
                unmake_move(copy_board, moves_list[i])
                print(f"Depth: {depth} - After move: {moves_list[i].get_stockfish_format()}, eval: {eval}, path: {path}")
                if eval <= best_eval:
                    best_eval = eval
                    best_move = moves_list[i]
                # beta = min(beta, eval)
                # if alpha >= beta:
                #     break
            print("Best move: ", best_move)
            return best_move

    def benchmark(self,_depth, package): # package is index under which the position package is
        total_time = [0] * _depth        # second index is for positions or their evaluations
        for i in range(len(positions_package[package][0])):
            for depth in range(_depth):
                self.board.load_fen(positions_package[package][0][i])
                start_time = time.perf_counter()
                count = count_positions(self.board,depth)
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                total_time[depth] += elapsed_time
                print(f" Move: {count}, True value: {positions_package[package][1][i][depth]}, Elapsed time: {elapsed_time:.6f} seconds")
            print("\n")
        formatted_total_time = [f"{time:.6f}" for time in total_time]
        print(f" Total time: {formatted_total_time}")

