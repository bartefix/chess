from moves import *
from constants import *


best_move_last_iteration = (-1,None)
def set_last_best_move(move, depth):
    global best_move_last_iteration
    best_move_last_iteration = depth,move

def evaluate_position(board):
    '''
    Evaluation returns positive values if the position is good for the player whose turn it is.
    '''
    eval = 0.0
    chessboard=board.chessboard
    index = 1 if board.who_to_move==WHITE else -1
    white_material = -piece_value[0] # material without kings
    black_material = -piece_value[0]
    for i in range(64):
        if chessboard[i]!= 0:
                if chessboard[i].colour==WHITE:
                    white_material += piece_value[chessboard[i].type - 1]
                if chessboard[i].colour==BLACK:
                    black_material += piece_value[chessboard[i].type - 1]
    material = (white_material + black_material) / 7800
    for i in range(64):
        if chessboard[i]!= 0:
            if chessboard[i].type != KING:
                if chessboard[i].colour==WHITE:
                    if chessboard[i].type != PAWN:
                        eval += piece_value[chessboard[i].type-1] + squares_all[chessboard[i].type-1][i]
                    else:
                        eval += material * squares_pawn[i] + (1 - material) * squares_pawn_endgame[i]+ piece_value[chessboard[i].type-1]
                if chessboard[i].colour==BLACK:
                    r = 7 - (i // 8)
                    c = i % 8
                    j = r*8+c
                    if chessboard[i].type != PAWN:
                        eval -= piece_value[chessboard[i].type - 1] + squares_all[chessboard[i].type-1][j]
                    else:
                        eval -= material * squares_pawn[j] + (1 - material) * squares_pawn_endgame[j] + piece_value[chessboard[i].type-1]
    eval += calculate_king_eval(board, white_material, black_material)
    eval /=100
    return eval*index

def calculate_king_eval(board,white_material,black_material):
    index = 1 if white_material > black_material + 300 else 0
    index = -1 if black_material > white_material + 300 else index
    material = (white_material+black_material)/7800
    eval = 0.0
    eval += material * squares_king[board.king_pos[1]] + (1 - material) * squares_king_endgame[board.king_pos[1]]
    i = 7 - (board.king_pos[0] // 8)
    j = board.king_pos[0] % 8
    c = i * 8 + j
    eval -= material * squares_king[c] + (1 - material) * squares_king_endgame[c]
    if index!=0:
        i_white = board.king_pos[0] // 8
        j_white = board.king_pos[0] % 8
        i_black = board.king_pos[1] // 8
        j_black = board.king_pos[1] % 8
        distance = abs(i_white - i_black) + abs(j_white - j_black)
        eval += (16-distance)*(1-material)*index*15
    return eval

def move_heuristic(board,move):
    score = 0
    chessboard=board.chessboard
    index = 1 if board.who_to_move == WHITE else 0

    if move.castle != 0:
        score += 50

    if chessboard[move.move_to] != 0:
        score += max(piece_value[chessboard[move.move_to].type-1] - piece_value[chessboard[move.move_from].type-1],100)
        if board.attack_squares[index][move.move_to] == 0:
            score += piece_value[chessboard[move.move_to].type-1]

    if move.promotion != 0:
        score += piece_value[move.promotion-1]

    if board.pawn_attack_squares[index][move.move_to] == 1 and chessboard[move.move_from].type!=PAWN:
        score -= piece_value[chessboard[move.move_from].type-1]  # If we move a piece into a pawn held square its probably bad

    if board.pawn_attack_squares[index][move.move_from] == 1 and chessboard[move.move_from].type != PAWN:
        score += piece_value[chessboard[move.move_from].type-1] # If we move a piece from a pawn held square its probably good

    # if board.attack_squares[index][move.move_to] == 1: #and board.attack_squares[1-index][move.move_to] == 0:
    #     score -= piece_value[chessboard[move.move_from].type-1]

    score += squares_all[chessboard[move.move_from].type-1][move.move_to] - squares_all[chessboard[move.move_from].type-1][move.move_from]
    return score

def sort_moves(board,moves):
    moves.sort(key=lambda move: move_heuristic(board,move), reverse=True)

number_positions_searched = 0
def print_nps():
    global number_positions_searched
    global number_quiet_positions_searched
    print(f"Number of positions checked: {number_positions_searched}")
    x = number_positions_searched
    number_positions_searched = 0
    return x

def search(board,depth,alpha,beta):
    '''
    Alpha-Beta negative minimax algorithm. We use the fact that max(a, b) == -min(-a, -b)
    to get rid of different cases for black and white player.
    '''
    candidate = None
    if depth==0:
        eval = search_until_no_captures(board,alpha,beta)
        return eval,candidate
    board_copy = board.copy()
    moves = all_legal_moves(board_copy, board_copy.who_to_move)

    if not moves:
        if board.is_king_checked():
            return -MATEINONE, candidate
        else:
            return 0.0, candidate

    if insufficient_material(board):
        return 0.0, candidate

    moves = list(moves)
    sort_moves(board,moves)
    best = float('-inf')

    global best_move_last_iteration
    if best_move_last_iteration[0] == depth:

        moves.remove(best_move_last_iteration[1])
        moves.insert(0, best_move_last_iteration[1])

    for move in moves:

        make_move(board_copy,move)
        eval,_= search(board_copy,depth-1,-beta,-alpha)
        unmake_move(board_copy,move)

        #print(f"Depth: {depth},move: {move.get_stockfish_format()}, eval: {eval}")
        eval = -eval
        eval-=0.02 # To incentive playing good moves quicker

        if abs(eval) > MATEINONE/2:
            eval+= MATEDOWNSTEP * (-1 if eval > 0 else 1)

        if eval > best:
            best = eval
            candidate = move

        alpha = max(alpha, eval)
        if alpha >= beta:
            break

    return best,candidate

def search_until_no_captures(board, alpha, beta):

    standard_evaluation = evaluate_position(board)

    global number_positions_searched
    number_positions_searched += 1  # count number of nodes searched

    if standard_evaluation >= beta:
        return standard_evaluation

    if standard_evaluation > alpha:
        alpha = standard_evaluation

    board_copy = board.copy()
    capture_moves = all_legal_captures(board_copy,board_copy.who_to_move)
    moves = list(capture_moves)
    sort_moves(board, moves)

    for move in moves:

            make_move(board_copy, move)
            eval = -search_until_no_captures(board_copy, -beta, -alpha)
            unmake_move(board_copy, move)

            if eval >= beta:
                return beta  # Beta-cutoff

            if eval > alpha:
                alpha = eval  # update best found score

    return alpha  # return best found evaluation

def count_positions(board,depth):

    if depth==0:
        return 1

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

piece_value = [20000,900,500,300,300,100]
MATEINONE = 100_000
MATEDOWNSTEP = 5_000
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
                 -1, -3, 0, 23, 23,  0, -3, -1,
                 5, -5,-10,  0,  0,-10, -5,  5,
                 5, 10, 10,-20,-20, 10, 10,  5,
                 0,  0,  0,  0,  0,  0,  0,  0]
squares_king_endgame = [
                -50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50]
squares_pawn_endgame = [
                 0,  0,  0,  0,  0,  0,  0,  0,
                75, 75, 75, 75, 75, 75, 75, 75,
                50, 50, 50, 50, 50, 50, 50, 50,
                30, 30, 30, 30, 30, 30, 30, 30,
                15, 15, 15, 15, 15, 15, 15, 15,
                 5,  5,  5,  5,  5,  5,  5,  5,
                 5,  5,  5,  5,  5,  5,  5,  5,
                 0,  0,  0,  0,  0,  0,  0,  0
]
squares_all = [squares_king,squares_queen,squares_rook,squares_bishop,squares_knight,squares_pawn]