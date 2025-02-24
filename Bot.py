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
        #sort_moves(self.board, moves_list)

        # if len(moves_list) == 1: # If only one move we don't have a choice
        #     return moves_list[0] # But it's not that great because then evaluation says everything is fine even if it's mate in 1

        #print(moves_list)
        depth = _depth
        colour_modifier = 1 if self.board.who_to_move == WHITE else -1
        copy_board = copy.deepcopy(self.board)
        alpha = float("-inf")
        beta = float("inf")
        '''
        We first search at a super shallow depth, and in the next iteration look at the best move
        from previous iteration first. Despite the shallow depth the moves are often the best moves found at deeper depth.
        This is a simplified version of a Principle Variation.
        '''
        set_last_best_move(None,-1)
        if depth > 2:
            _, best_move = search(copy_board, depth-2, alpha, beta)
            set_last_best_move(best_move,depth)

        copy_board = copy.deepcopy(self.board)
        eval,best_move = search(copy_board,depth,alpha,beta)
        print(f"Best move: {best_move}, eval: {eval*colour_modifier:.2f}")
        print_nps()
        return best_move

        # random.shuffle(moves_list)
        # best_eval = float("-inf")
        # best_move = -1
        # for i in range(n):
        #     make_move(copy_board,moves_list[i])
        #     eval,path = search(copy_board,depth-1,-beta,-alpha)
        #     eval = -eval
        #     unmake_move(copy_board,moves_list[i])
        #     print(f"Depth: {depth} - After move: {moves_list[i].get_stockfish_format()}, eval: {eval}, path: {path}")
        #     if eval >= best_eval:
        #         best_eval = eval
        #         best_move = moves_list[i]
        #     alpha = max(alpha, eval)
        #
        # #print(evaluate_position(self.board))
        # print("Best move: ",best_move)
        # print_nps()
        # return best_move

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

    def benchmark2(self,_depth, package):
        total_time=0
        total_nodes=0
        for i in range(len(positions_package[package])):
                self.board.load_fen(positions_package[package][i])
                start_time = time.perf_counter()
                move = self.give_move(_depth)
                total_nodes +=print_nps()
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                total_time += elapsed_time
                print(f" Move: {move}, Elapsed time: {elapsed_time:.6f} seconds")
        print(f"Total time: {total_time}, total nodes: {total_nodes}")