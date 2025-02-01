from constants import *
from Piece import *
class Move:
    def __init__(self, move_from, move_to, promotion=0, castle=0, enable_passant=None, prevents_castle=None):
        # parameters passed either both as pairs or both as integers
        if prevents_castle is None:
            prevents_castle = [1, 1, 1, 1]
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
        self.prevents_castle = prevents_castle # values to be and-ed with
        self.enable_passant = enable_passant # set of en passant moves for next turn

    '''
    there WAS an uncaught bug where a (possibly) queen move adds two identical moves to the set. This solves the issue 
    '''
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.move_from, self.move_to, self.promotion, self.castle, self.enable_passant) == (other.move_from, other.move_to, other.promotion,other.castle,other.enable_passant)

    def __hash__(self):
        return hash((self.move_from, self.move_to, self.promotion, self.castle))

    def getpair_from(self):
        i = self.move_from // 8
        j = self.move_from % 8
        return (i, j)

    def getpair_to(self):
        i = self.move_to // 8
        j = self.move_to % 8
        return (i, j)

    def get_promotion(self):
        return self.promotion
    def get_castle(self):
        return self.castle
    def get_passants(self):
        return self.enable_passant
    def get_stockfish_format(self):
        row,col = self.getpair_from()
        file = chr(ord('a') + col)  # Convert column index to letter
        rank = str(8 - row)  # Convert row index to rank (8 to 1)
        letterfrom = file + rank
        row, col = self.getpair_to()
        file = chr(ord('a') + col)  # Convert column index to letter
        rank = str(8 - row)  # Convert row index to rank (8 to 1)
        letterto = file + rank
        return letterfrom+letterto
    def __repr__(self):
        return f"{self.get_stockfish_format()}"
