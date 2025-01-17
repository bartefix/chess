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

    if board.king_in_check:
        moves = all_legal_moves(board, board.who_to_move)
        if len(moves) == 0:
            if not islegal(board, None):
                return float('inf') if board.who_to_move == BLACK else float('-inf')
            else:
                return 0.0
    else: moves = None

    if insufficient_material(board):
        return 0.0

    if depth==0:
        return evaluate_position(board)
    if moves is None:
        moves = all_legal_moves(board, board.who_to_move)
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
        return 1
    boardcopy = copy.deepcopy(board)
    moves = all_legal_moves(boardcopy,boardcopy.who_to_move)
    if depth==1:
        return len(moves)
    numpos = 0
    for move in moves:
        make_move(boardcopy, move)
        a = count_positions(boardcopy, depth - 1)
        numpos+=a
        unmake_move(boardcopy, move)
        # if depth==3:
        #     print(f"{move.get_stockfish_format()}: {a}")
    return numpos

piece_value = [-1,20000,900,500,300,300,100]