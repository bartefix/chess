from math import floor

from constants import *
from Move import Move

def calc_pawn(chessboard, i, piece):
    moves = set()
    which_colour = 1 if piece.colour == BLACK else -1

    for capture in [7, 9]:
        if  0 <= i + capture * which_colour < 64 and abs(i%8 - (i+capture*which_colour)%8) < 2:
            if chessboard[i + capture * which_colour] != 0:
                if chessboard[i + capture * which_colour].colour != piece.colour:
                    if 0 <= i + (8+capture)*which_colour<64:
                        moves.add(Move(i, i + capture * which_colour))
                    else:
                        moves.add(Move(i, i + capture * which_colour,promotion=QUEEN))
                        moves.add(Move(i, i + capture * which_colour, promotion=BISHOP))
                        moves.add(Move(i, i + capture * which_colour, promotion=ROOK))
                        moves.add(Move(i, i + capture * which_colour, promotion=KNIGHT))
    return moves

def calc_king(chessboard, i, piece):
    moves = set()
    offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (
                i + offset) % 8) <= 1:  # checking if the distance in x axes is at most 1, prevents out of bounds
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
    return moves

def calc_rook(chessboard, i, piece):

    moves = set()
    offsets = [-8, -1, 1, 8]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and (i % 8 - (i + offset) % 8) * (floor(i / 8) - floor((i + offset) / 8)) == 0:
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
                break
            offset += offset_add
    return moves

def calc_bishop(chessboard, i, piece):
    moves = set()
    offsets = [-9, -7, 7, 9]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and abs(i % 8 - (i + offset) % 8) == abs(floor(i / 8) - floor((i + offset) / 8)):
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
                break
            offset += offset_add
    return moves

def calc_knight(chessboard, i, piece):
    moves = set()
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (i + offset) % 8) <= 2:
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
    return moves

def calc_queen(chessboard, move_from, piece):
    moves = calc_rook(chessboard, move_from, piece)
    moves = moves | calc_bishop(chessboard, move_from, piece)
    return moves


def calc_piece_help(board, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    chessboard = board.chessboard
    type = piece.type
    if type == PAWN:
        return calc_pawn(chessboard, i, piece)
    if type == ROOK:
        return calc_rook(chessboard, i, piece)
    if type == BISHOP:
        return calc_bishop(chessboard, i, piece)
    if type == KNIGHT:
        return calc_knight(chessboard, i, piece)
    if type == KING:
        return calc_king(chessboard, i, piece)
    if type == QUEEN:
        return calc_queen(chessboard, i, piece)

def calc_piece(board, move_from, piece):
    moves = calc_piece_help(board, move_from, piece)
    if piece.type != PAWN:
        return moves
    else:
        for move in board.passants:
            if move.getpair_from() == move_from:
                moves.add(move)
        return moves

def all_captures(board, colour):
    moves = set()
    for i in range(8):
        for j in range(8):
            if board[i,j]!=0:
                if board[i,j].colour == colour:
                    moves = moves | calc_piece(board,(i,j),board[i,j])
    return moves

