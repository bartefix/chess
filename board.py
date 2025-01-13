from constants import *
from pieces import *


class Board:
    def __init__(self):
        self.chessboard = [0 for x in range(64)]
        self.chessboard[0] = Piece(ROOK, BLACK)
        self.chessboard[1] = Piece(KNIGHT, BLACK)
        self.chessboard[2] = Piece(BISHOP, BLACK)
        self.chessboard[3] = Piece(QUEEN, BLACK)
        self.chessboard[4] = Piece(KING, BLACK)
        self.chessboard[5] = Piece(BISHOP, BLACK)
        self.chessboard[6] = Piece(KNIGHT, BLACK)
        self.chessboard[7] = Piece(ROOK, BLACK)
        for i in range(8):
            self.chessboard[8 + i] = Piece(PAWN,BLACK)

        self.chessboard[56] = Piece(ROOK, WHITE)
        self.chessboard[57] = Piece(KNIGHT, WHITE)
        self.chessboard[58] = Piece(BISHOP, WHITE)
        self.chessboard[59] = Piece(QUEEN, WHITE)
        self.chessboard[60] = Piece(KING, WHITE)
        self.chessboard[61] = Piece(BISHOP, WHITE)
        self.chessboard[62] = Piece(KNIGHT, WHITE)
        self.chessboard[63] = Piece(ROOK, WHITE)
        for i in range(8):
            self.chessboard[48 + i] = Piece(PAWN, WHITE)

        self.passants = set()
        self.who_to_move = WHITE

        self.previous_piece = None
        self.previous_castle = 0
        self.previous_passants = None
        self.previous_promotion = False
        self.previous_passant_move = False
        self.has_it_moved = False
    def __getitem__(self, indices):
        if isinstance(indices, tuple):
            i,j = indices
            return self.chessboard[i*8+j]
        else:
            raise TypeError("bad")

    def __setitem__(self, indices, value):
        if isinstance(indices, tuple):
            i,j = indices
            self.chessboard[i*8+j] = value
        else:
            raise TypeError("bad")


