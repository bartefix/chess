from moves import *
from constants import *
def evaluate_position(board):
    side = {WHITE: 1, BLACK: -1}
    eval = 0.0
    chessboard=board.chessboard
    for i in range(64):
        if chessboard[i]!= 0:
            if chessboard[i].colour==WHITE:
                eval += piece_value[chessboard[i].type-1] + squares_all[chessboard[i].type-1][i]
            if chessboard[i].colour==BLACK:
                r = 7 - (i // 8)
                c = i % 8
                j = r*8+c
                eval -= piece_value[chessboard[i].type - 1] + squares_all[chessboard[i].type-1][j]
    eval /=100
    return eval

def search(board,depth):
    board_copy = board.copy()
    if board.is_king_checked():
        moves = all_legal_moves(board_copy, board.who_to_move)
        if len(moves) == 0:
            return float('inf') if board.who_to_move == BLACK else float('-inf')
        else:
            return 0.0
    else: moves = None

    if insufficient_material(board):
        return 0.0

    if depth==0:
        return evaluate_position(board)

    if moves is None:
        moves = all_legal_moves(board_copy, board.who_to_move)
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
    #boardcopy = copy.deepcopy(board)
    boardcopy = board.copy()
    moves = all_legal_moves(boardcopy,boardcopy.who_to_move)
    if depth==1:
        return len(moves)
    numpos = 0
    for move in moves:
        make_move(boardcopy, move)
        a = count_positions(boardcopy, depth - 1)
        numpos+=a
        unmake_move(boardcopy, move)
        # if depth==2:
        #     print(f"{move.get_stockfish_format()}: {a}")
    return numpos

piece_value = [-1,20000,900,500,300,300,100]


squares_king = [-30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                 20, 20,  0,  0,  0,  0, 20, 20,
                 20, 30, 10,  0,  0, 10, 30, 20]

squares_queen = [-20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20]
squares_rook = [0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0]
squares_bishop =   [-20,-10,-10,-10,-10,-10,-10,-20,
                    -10,  0,  0,  0,  0,  0,  0,-10,
                    -10,  0,  5, 10, 10,  5,  0,-10,
                    -10,  5,  5, 10, 10,  5,  5,-10,
                    -10,  0, 10, 10, 10, 10,  0,-10,
                    -10, 10, 10, 10, 10, 10, 10,-10,
                    -10,  5,  0,  0,  0,  0,  5,-10,
                    -20,-10,-10,-10,-10,-10,-10,-20]
squares_knight =   [-50,-40,-30,-30,-30,-30,-40,-50,
                    -40,-20,  0,  0,  0,  0,-20,-40,
                    -30,  0, 10, 15, 15, 10,  0,-30,
                    -30,  5, 15, 20, 20, 15,  5,-30,
                    -30,  0, 15, 20, 20, 15,  0,-30,
                    -30,  5, 10, 15, 15, 10,  5,-30,
                    -40,-20,  0,  5,  5,  0,-20,-40,
                    -50,-40,-30,-30,-30,-30,-40,-50]
squares_pawn = [ 0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                 5,  5, 10, 25, 25, 10,  5,  5,
                 0,  0,  0, 20, 20,  0,  0,  0,
                 5, -5,-10,  0,  0,-10, -5,  5,
                 5, 10, 10,-20,-20, 10, 10,  5,
                 0,  0,  0,  0,  0,  0,  0,  0]
squares_all = [squares_king,squares_queen,squares_rook,squares_bishop,squares_knight,squares_pawn]