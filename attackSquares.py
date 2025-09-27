from math import floor

from constants import *
from Move import Move


'''
Attacked squares differ from calculating moves because we can attack squares occupied by pieces of our colour.
It also requieres much less computation so it is more efficient to write another set of functions
'''

def calc_pawn_attacksquares(chessboard, i, piece,attack_squares,pawn_attack_squares):

    which_colour = 1 if piece.colour == BLACK else -1
    for capture in [7, 9]:
        if 0 <= i + capture * which_colour < 64 and abs(i % 8 - (i + capture * which_colour) % 8) < 2:
            attack_squares[i + capture * which_colour] = 1
            pawn_attack_squares[i + capture * which_colour] = 1

def calc_king_attacksquares(chessboard, i, piece,attack_squares):
    offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (
                i + offset) % 8) <= 1:  # checking if the distance in x axes is at most 1, prevents out of bounds
            attack_squares[i + offset]=1


def calc_rook_attacksquares(chessboard, i, piece,attack_squares):
    offsets = [-8, -1, 1, 8]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and (i % 8 - (i + offset) % 8) * (floor(i / 8) - floor((i + offset) / 8)) == 0:
            if chessboard[i + offset] != 0:
                attack_squares[i + offset]=1
                break
            else:
                attack_squares[i + offset]=1
            offset += offset_add

def calc_bishop_attacksquares(chessboard, i, piece,attack_squares):
    offsets = [-9, -7, 7, 9]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and abs(i % 8 - (i + offset) % 8) == abs(floor(i / 8) - floor((i + offset) / 8)):
            if chessboard[i + offset] != 0:
                attack_squares[i + offset]=1
                break
            else:
                attack_squares[i + offset]=1
            offset += offset_add

def calc_knight_attacksquares(chessboard, i, piece,attack_squares):
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (i + offset) % 8) <= 2:
            attack_squares[i + offset]=1

def calc_queen_attacksquares(chessboard, i, piece,attack_squares):
    calc_rook_attacksquares(chessboard, i, piece,attack_squares)
    calc_bishop_attacksquares(chessboard, i, piece,attack_squares)

def calc_attacks_help(board, i, piece,attack_squares,pawn_attack_squares):
    chessboard = board.chessboard
    type = piece.type
    if type == PAWN:
        calc_pawn_attacksquares(chessboard, i, piece,attack_squares,pawn_attack_squares)
    if type == ROOK:
        calc_rook_attacksquares(chessboard, i, piece,attack_squares)
    if type == BISHOP:
        calc_bishop_attacksquares(chessboard, i, piece,attack_squares)
    if type == KNIGHT:
        calc_knight_attacksquares(chessboard, i, piece,attack_squares)
    if type == KING:
        calc_king_attacksquares(chessboard, i, piece,attack_squares)
    if type == QUEEN:
        calc_queen_attacksquares(chessboard, i, piece,attack_squares)

def calculate_attack_squares(board,colour):
    index = 0 if colour == WHITE else 1
    board.attack_squares[index] = [0 for x in range(64)]
    board.pawn_attack_squares[index] = [0 for x in range(64)]
    for i in range(64):
            if board.chessboard[i] != 0:
                if board.chessboard[i].colour == colour:
                    calc_attacks_help(board, i, board.chessboard[i],board.attack_squares[index],board.pawn_attack_squares[index])

def squares_between(): #preprocessing squares between every two squares to quickly find if we can block check
    arr = [[[] for _ in range(64)] for _ in range(64)]

    for sq1 in range(64):
        for sq2 in range(64):

            rank1, file1 = divmod(sq1, 8)
            rank2, file2 = divmod(sq2, 8)

            between = []

            if rank1 == rank2:
                if abs(file1 - file2) > 1:
                    start, end = sorted((file1, file2))
                    between = [rank1 * 8 + f for f in range(start + 1, end)]

            elif file1 == file2:
                if abs(rank1 - rank2) > 1:
                    start, end = sorted((rank1, rank2))
                    between = [r * 8 + file1 for r in range(start + 1, end)]

            elif abs(rank1 - rank2) == abs(file1 - file2):
                rank_step = 1 if rank2 > rank1 else -1
                file_step = 1 if file2 > file1 else -1

                for step in range(1, abs(rank1 - rank2)):
                    r = rank1 + step * rank_step
                    f = file1 + step * file_step
                    between.append(r * 8 + f)

            arr[sq1][sq2] = between

    return arr
arr = squares_between()
