from constants import *
from pieces import *
from attackSquares import calculate_attack_squares

class Board:
    def __init__(self):
        self.chessboard = [0 for x in range(64)]
        # self.chessboard[0] = Piece(ROOK, BLACK)
        # self.chessboard[1] = Piece(KNIGHT, BLACK)
        # self.chessboard[2] = Piece(BISHOP, BLACK)
        # self.chessboard[3] = Piece(QUEEN, BLACK)
        # self.chessboard[4] = Piece(KING, BLACK)
        # self.chessboard[5] = Piece(BISHOP, BLACK)
        # self.chessboard[6] = Piece(KNIGHT, BLACK)
        # self.chessboard[7] = Piece(ROOK, BLACK)
        # for i in range(8):
        #     self.chessboard[8 + i] = Piece(PAWN,BLACK)
        #
        # self.chessboard[56] = Piece(ROOK, WHITE)
        # self.chessboard[57] = Piece(KNIGHT, WHITE)
        # self.chessboard[58] = Piece(BISHOP, WHITE)
        # self.chessboard[59] = Piece(QUEEN, WHITE)
        # self.chessboard[60] = Piece(KING, WHITE)
        # self.chessboard[61] = Piece(BISHOP, WHITE)
        # self.chessboard[62] = Piece(KNIGHT, WHITE)
        # self.chessboard[63] = Piece(ROOK, WHITE)
        # for i in range(8):
        #     self.chessboard[48 + i] = Piece(PAWN, WHITE)
        self.passants = set()
        self.who_to_move = WHITE
        self.previous_piece = None
        self.previous_passants = None
        self.previous_passant_move = False
        self.castle_rights = [0,0,0,0]  # 0 - q, 1 - k, 2 - Q, 3 - K
        self.prev_castle_rights = [0,0,0,0]

        self.attack_squares = [[0 for x in range(64)],[0 for x in range(64)]]
        self.previous_attack_squares = [[0 for x in range(64)],[0 for x in range(64)]]

        self.load_fen(fenpositions[0])

    def print_board(self):
        for idx, squares in enumerate(self.attack_squares):
            print(f"Board {idx + 1}:")
            for row in range(8):
                print(squares[row * 8:(row + 1) * 8])  # Slicing each row
            print()  # Blank line between boards
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
        for i in range(64):
            if self.chessboard[i] != 0:
                if self.chessboard[i].type == KING:
                    if self.chessboard[i].colour == self.who_to_move:
                        if self.attack_squares[index][i]==1:
                            return True
        return False
    def get_king_position(self):
        for i in range(64):
            if self.chessboard[i] != 0:
                if self.chessboard[i].type == KING:
                    if self.chessboard[i].colour == self.who_to_move:
                            return i
        return -1
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

        # Parse en passant
        if en_passant != '-':
            pass
        calculate_attack_squares(self,WHITE)
        calculate_attack_squares(self, BLACK)


