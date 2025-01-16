from moves import *
from constants import *
def evaluate_position(board):
    side = {WHITE: 1, BLACK: -1}
    eval = 0.0
    chessboard=board.chessboard
    for i in range(64):
        if chessboard[i]!= 0:
            eval += piece_value[chessboard[i].type]*side[chessboard[i].colour]
    eval /=100
    return eval

def search(board,depth):

    if depth==0:
        return evaluate_position(board)

    moves = all_legal_moves(board, board.who_to_move)
    if len(moves) == 0:
        if not islegal(board, None):
            return float('inf') if board.who_to_move == BLACK else float('-inf')
        else:
            return 0.0
    if insufficient_material(board):
        return 0.0

    board_copy = copy.deepcopy(board)
    if board.who_to_move==WHITE:
        best = float('-inf')
        for move in moves:
            make_move(board_copy,move)
            eval = search(board_copy,depth-1)
            unmake_move(board_copy,move)
            if eval > best:
                best = eval
        return best

    if board.who_to_move==BLACK:
        best = float('inf')
        for move in moves:
            make_move(board_copy,move)
            eval = search(board_copy,depth-1)
            unmake_move(board_copy, move)
            if eval < best:
                best = eval
        return best

def count_positions(board,depth):
    if depth==0:
        return 1;
    moves = all_legal_moves(board,board.who_to_move)
    numpos = 0
    boardcopy = copy.deepcopy(board)
    for move in moves:
        make_move(boardcopy,move)
        numpos += count_positions(boardcopy,depth-1)
        unmake_move(boardcopy,move)
    return numpos

piece_value = [-1,20000,900,500,300,300,100]