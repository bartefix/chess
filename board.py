import copy

from constants import *
from pieces import *
from attackSquares import calculate_attack_squares

class Board:
    def __init__(self):
        self.chessboard = [0 for x in range(64)]
        self.passants = set()
        self.who_to_move = WHITE
        self.previous_piece = None
        self.previous_passants = None
        self.previous_passant_move = False
        self.castle_rights = [0,0,0,0]  # 0 - q, 1 - k, 2 - Q, 3 - K
        self.prev_castle_rights = [0,0,0,0]
        self.king_pos = [4,60] # 1 - white, 0 - black
        self.prev_king_pos = [4,60]
        self.attack_squares = [[0 for x in range(64)],[0 for x in range(64)]] # 1 - white, 0 - black
        #self.previous_attack_squares = [[0 for x in range(64)],[0 for x in range(64)]]
        self.load_fen(eval_test_positions[3])

    def print_board(self):
        for idx, squares in enumerate(self.attack_squares):
            print(f"Board {idx + 1}:")
            for row in range(8):
                print(squares[row * 8:(row + 1) * 8])
            print()
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

    def is_king_checked(self):
        index = 1 if self.who_to_move == WHITE else 0
       # print(self.king_pos)
        return self.attack_squares[index][self.king_pos[index]]

    def get_king_position(self):
        index = 1 if self.who_to_move == WHITE else 0
        return self.king_pos[index]

    def load_fen(self, fen):

        self.chessboard = [0 for x in range(64)]
        self.passants.clear()

        fields = fen.split()
        piece_placement, active_color, castling, en_passant, *_ = fields

        rows = piece_placement.split('/')
        for rank_idx, row in enumerate(rows):
            file_idx = 0
            for char in row:
                if char.isdigit():

                    file_idx += int(char)
                else:
                    colour = WHITE if char.isupper() else BLACK
                    piece_type = {
                        'p': PAWN, 'r': ROOK, 'n': KNIGHT, 'b': BISHOP, 'q': QUEEN, 'k': KING
                    }[char.lower()]
                    position = rank_idx * 8 + file_idx
                    self.chessboard[position] = Piece(piece_type, colour)
                    file_idx += 1

        self.who_to_move = WHITE if active_color == 'w' else BLACK

        for char in castling: # 0 - q, 1 - k, 2 - Q, 3 - K
            if char == 'k':
                self.castle_rights[1]=1
            elif char == 'q':
                self.castle_rights[0]=1
            elif char == 'K':
                self.castle_rights[3]=1
            elif char == 'Q':
                self.castle_rights[2]=1

        # Parse en passant - not implemented
        if en_passant != '-':
            pass
        calculate_attack_squares(self,WHITE)
        calculate_attack_squares(self, BLACK)

        for i in range(64):
            if self.chessboard[i] != 0:
                if self.chessboard[i].type == KING:
                    if self.chessboard[i].colour == WHITE:
                        self.king_pos[1]=i
                    else:
                        self.king_pos[0]=i


    def copy(self):
        boardcopy = copy.copy(self)
        boardcopy.king_pos = self.king_pos.copy()
        boardcopy.prev_king_pos = self.prev_king_pos.copy()
        boardcopy.castle_rights = self.castle_rights.copy()
        boardcopy.prev_castle_rights = self.prev_castle_rights.copy()
        return boardcopy