from math import floor

from pieces import *
from board import *
import copy

class Move:
    def __init__(self, move_from, move_to, promotion=0, castle=0, enable_passant=None):
        # parameters passed either both as pairs or both as integers
        if enable_passant is None:
            enable_passant = set()
        if isinstance(move_from, tuple):
            self.move_from = 8 * move_from[0] + move_from[1]
            self.move_to = 8 * move_to[0] + move_to[1]
        else:
            self.move_from = move_from
            self.move_to = move_to
        self.promotion = promotion  # 0 - no promotion, else - the piece to promote to
        self.castle = castle  # 0 - not a castle move, 1 short castle, 2 long castle, 3 en passant
        self.enable_passant = enable_passant # set of en passant moves for next turn

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.move_from == other.move_from and self.move_to == other.move_to

    def __hash__(self):
        return hash((self.move_from, self.move_to))

    def getpair_from(self):
        i = floor(self.move_from / 8)
        j = self.move_from % 8
        return (i, j)

    def getpair_to(self):
        i = floor(self.move_to / 8)
        j = self.move_to % 8
        return (i, j)

    def get_promotion(self):
        return self.promotion
    def get_castle(self):
        return self.castle
    def get_passants(self):
        return self.enable_passant

def calc_pawn(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    which_colour = 1 if piece.colour == BLACK else -1
    if chessboard[i + 8 * which_colour] == 0:
        if 0 <= i + 16 * which_colour < 64:
            moves.add(Move(i, i + 8 * which_colour))
        else:
            moves.add(Move(i, i + 8 * which_colour, promotion=QUEEN))
        if 0 <= i + 16 * which_colour < 64:
            if chessboard[i + 16 * which_colour] == 0 and not piece.moved:
                passants_to_add = set()
                for capture in [15, 17]:
                    if 0 <= i + capture * which_colour < 64 and abs(i % 8 - (i + capture * which_colour) % 8) < 2:
                        if chessboard[i + capture * which_colour] != 0:
                            if chessboard[i + capture * which_colour].colour != piece.colour:
                                passants_to_add.add(Move(i + capture*which_colour, i +which_colour*8,castle=3))

                moves.add(Move(i, i + 16 * which_colour,enable_passant = passants_to_add))
    for capture in [7, 9]:
        if  0 <= i + capture * which_colour < 64 and abs(i%8 - (i+capture*which_colour)%8) < 2:
            if chessboard[i + capture * which_colour] != 0:
                if chessboard[i + capture * which_colour].colour != piece.colour:
                    if 0 <= i + (8+capture)*which_colour<64:
                        moves.add(Move(i, i + capture * which_colour))
                    else:
                        moves.add(Move(i, i + capture * which_colour,promotion=QUEEN))
    return moves


def calc_king(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (
                i + offset) % 8) <= 1:  # checking if the distance in x axes is at most 1, prevents out of bounds
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
            else:
                moves.add(Move(i, i + offset))
    if not piece.moved:
        if piece.colour == WHITE:
            if chessboard[63]!=0:
                if chessboard[61]==0 and chessboard[62]==0 and not chessboard[63].moved:
                    moves.add(Move(i,i+2,castle=1))
            if chessboard[56] != 0:
                if chessboard[57]==0 and chessboard[58]==0 and chessboard[59]==0 and not chessboard[56].moved:
                    moves.add(Move(i,i-3,castle=2))
        else:
            if chessboard[7] != 0:
                if chessboard[5]==0 and chessboard[6]==0 and not chessboard[7].moved:
                    moves.add(Move(i,i+2,castle=1))
            if chessboard[0] != 0:
                if chessboard[1]==0 and chessboard[2]==0 and chessboard[3]==0 and not chessboard[0].moved:
                    moves.add(Move(i,i-2,castle=2))
    return moves


def calc_rook(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    offsets = [-8, -1, 1, 8]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and (i % 8 - (i + offset) % 8) * (floor(i / 8) - floor((i + offset) / 8)) == 0:
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
                break
            else:
                moves.add(Move(i, i + offset))
            offset += offset_add
    return moves


def calc_bishop(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    offsets = [-9, -7, 7, 9]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and abs(i % 8 - (i + offset) % 8) == abs(floor(i / 8) - floor((i + offset) / 8)):
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
                break
            else:
                moves.add(Move(i, i + offset))
            offset += offset_add
    return moves


def calc_knight(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (i + offset) % 8) <= 2:
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset))
            else:
                moves.add(Move(i, i + offset))
    return moves


def calc_queen(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    moves = moves | calc_rook(chessboard, move_from, piece)
    moves = moves | calc_bishop(chessboard, move_from, piece)
    return moves


def calc_piece_help(board, move_from, piece):
    chessboard = board.chessboard
    type = piece.type
    if type == KING:
        return calc_king(chessboard, move_from, piece)
    if type == QUEEN:
        return calc_queen(chessboard, move_from, piece)
    if type == ROOK:
        return calc_rook(chessboard, move_from, piece)
    if type == BISHOP:
        return calc_bishop(chessboard, move_from, piece)
    if type == KNIGHT:
        return calc_knight(chessboard, move_from, piece)
    if type == PAWN:
        return calc_pawn(chessboard, move_from, piece)

def calc_piece(board, move_from, piece):
    passants = board.passants
    moves = calc_piece_help(board, move_from, piece)
    if piece.type != PAWN:
        return moves
    else:
        for move in passants:
            if move.getpair_from() == move_from:
                moves.add(move)
        return moves

def all_moves(board, colour):
    moves = set()
    for i in range(8):
        for j in range(8):
            if board[i,j]!=0:
                if board[i,j].colour == colour:
                    moves = moves | calc_piece(board,(i,j),board[i,j])
    return moves

def all_legal_moves(board, colour):
    moves = all_moves(board, colour)
    new_moves = set()
    for move in moves:
        if islegal(board, move):
            new_moves.add(move)
    return new_moves

def king_capture(chessboard, move):
    if chessboard[move.move_to] != 0: # this is single index format
        if chessboard[move.move_to].type == KING:
            return True
    return False

def make_move(board, move):
    if move is None:
        board.who_to_move = BLACK if board.who_to_move == WHITE else WHITE
        return
    board.passants.clear()
    chessboard = board.chessboard
    i = move.move_from
    j = move.move_to
    piece = chessboard[i]
    chessboard[i] = 0
    if move.get_promotion() != 0:
        chessboard[j] = Piece(move.get_promotion(), piece.colour)
        board.who_to_move = BLACK if board.who_to_move == WHITE else WHITE
        return
    if move.get_castle() != 0:
        if move.get_castle() == 1:
            chessboard[j] = piece
            chessboard[j].moved = True
            chessboard[i + 1] = chessboard[i + 3]
            chessboard[i + 3] = 0
            chessboard[i + 1].moved = True
        elif move.get_castle() == 2:
            chessboard[j] = piece
            chessboard[j].moved = True
            chessboard[i - 1] = chessboard[i - 4]
            chessboard[i - 4] = 0
            chessboard[i - 1].moved = True
        else:
            which_colour = 1 if piece.colour == BLACK else -1
            chessboard[j-8*which_colour] = 0

    chessboard[j] = piece
    chessboard[j].moved = True
    if len(move.enable_passant) > 0:
        board.passants = move.get_passants()
    board.who_to_move = BLACK if board.who_to_move == WHITE else WHITE

def islegal(board, move):
    board_copy = copy.deepcopy(board)
    make_move(board_copy, move)
    for move in all_moves(board_copy,board_copy.who_to_move):
        if king_capture(board_copy.chessboard, move):
            return False
    return True

def insufficient_material(board):
    chessboard = board.chessboard
    count_pieces = [0,0,0,0,0,0] # 0-king, 1-queen,2-rook,3-bishop, 4-knight,5-pawn
    for i in range(64):
        if chessboard[i]!=0:
            count_pieces[chessboard[i].type-1] += 1
    if count_pieces[1]+count_pieces[2]+count_pieces[5] > 0:
        return False
    else:
        if count_pieces[3] + count_pieces[4] < 3:
            return True
        else:
            return False

def isgameover(board):
    moves = all_legal_moves(board,board.who_to_move)
    if len(moves) == 0:
        if not islegal(board,None):
            return CHECKMATE
        else:
            return STALEMATE
    if insufficient_material(board):
        return DRAW
    return PLAYING