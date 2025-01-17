from math import floor

from pieces import *
from board import *
import copy

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
    theres an uncaught bug where a (possibly) queen move adds two identical moves to the set. This solves the issue 
    '''
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.move_from, self.move_to, self.promotion, self.castle, self.enable_passant) == (other.move_from, other.move_to, other.promotion,other.castle,other.enable_passant)

    def __hash__(self):
        return hash((self.move_from, self.move_to, self.promotion, self.castle))

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
def calc_pawn(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    which_colour = 1 if piece.colour == BLACK else -1
    if chessboard[i + 8 * which_colour] == 0:
        if 0 <= i + 16 * which_colour < 64:
            moves.add(Move(i, i + 8 * which_colour))
        else:
            moves.add(Move(i, i + 8 * which_colour, promotion=QUEEN))
            moves.add(Move(i, i + 8 * which_colour, promotion=ROOK))
            moves.add(Move(i, i + 8 * which_colour, promotion=KNIGHT))
            moves.add(Move(i, i + 8 * which_colour, promotion=BISHOP))
        if 0 <= i + 16 * which_colour < 64:
            if chessboard[i + 16 * which_colour] == 0 and (int) (3.5-2.5*which_colour) == move_from[0]: # ingenious way of checking if on 2nd/7th rank
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
                        moves.add(Move(i, i + capture * which_colour, promotion=BISHOP))
                        moves.add(Move(i, i + capture * which_colour, promotion=ROOK))
                        moves.add(Move(i, i + capture * which_colour, promotion=KNIGHT))
    return moves


def calc_king(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    moves = set()
    offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    prevents_castling = [1,1,0,0] if piece.colour == WHITE else [0,0,1,1]
    for offset in offsets:
        if 0 <= i + offset < 64 and abs(i % 8 - (
                i + offset) % 8) <= 1:  # checking if the distance in x axes is at most 1, prevents out of bounds
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset,prevents_castle=prevents_castling))
            else:
                moves.add(Move(i, i + offset,prevents_castle=prevents_castling))

    if piece.colour == WHITE and i==60:
        if chessboard[63]!=0: #White short castle
            if chessboard[61]==0 and chessboard[62]==0:
                moves.add(Move(i,i+2,castle=1,prevents_castle=prevents_castling))
        if chessboard[56] != 0: #White long castle
            if chessboard[57]==0 and chessboard[58]==0 and chessboard[59]==0:
                moves.add(Move(i,i-2,castle=2,prevents_castle=prevents_castling))
    if piece.colour == BLACK and i==4:
        if chessboard[7] != 0: #Black short castle
            if chessboard[5]==0 and chessboard[6]==0:
                moves.add(Move(i,i+2,castle=1,prevents_castle=prevents_castling))
        if chessboard[0] != 0: #Black long castle
            if chessboard[1]==0 and chessboard[2]==0 and chessboard[3]==0:
                moves.add(Move(i,i-2,castle=2,prevents_castle=prevents_castling))
    return moves


def calc_rook(chessboard, move_from, piece):
    i = move_from[0] * 8 + move_from[1]
    prevents_castling = [1,1,1,1]
    if move_from == (7,7):
        prevents_castling = [1,1,1,0]
    if move_from == (7,0):
        prevents_castling = [1,1,0,1]
    if move_from == (0,7):
        prevents_castling = [1,0,1,1]
    if move_from == (0,0):
        prevents_castling = [0,1,1,1]
    moves = set()
    offsets = [-8, -1, 1, 8]
    for offset in offsets:
        offset_add = offset
        while 0 <= i + offset < 64 and (i % 8 - (i + offset) % 8) * (floor(i / 8) - floor((i + offset) / 8)) == 0:
            if chessboard[i + offset] != 0:
                if chessboard[i + offset].colour != piece.colour:
                    moves.add(Move(i, i + offset,prevents_castle=prevents_castling))
                break
            else:
                moves.add(Move(i, i + offset,prevents_castle=prevents_castling))
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
    moves = calc_rook(chessboard, move_from, piece)
    moves = moves | calc_bishop(chessboard, move_from, piece)
    return moves


def calc_piece_help(board, move_from, piece):
    chessboard = board.chessboard
    type = piece.type
    if type == PAWN:
        return calc_pawn(chessboard, move_from, piece)
    if type == ROOK:
        return calc_rook(chessboard, move_from, piece)
    if type == BISHOP:
        return calc_bishop(chessboard, move_from, piece)
    if type == KNIGHT:
        return calc_knight(chessboard, move_from, piece)
    if type == KING:
        return calc_king(chessboard, move_from, piece)
    if type == QUEEN:
        return calc_queen(chessboard, move_from, piece)

def calc_piece(board, move_from, piece):
    moves = calc_piece_help(board, move_from, piece)
    if piece.type != PAWN:
        return moves
    else:
        for move in board.passants:
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

    new_moves = set()
    boardcopy = copy.deepcopy(board)
    moves = all_moves(boardcopy, colour)
    for move in moves:
        if move.get_castle() == 1:
            offset = 3 if colour == WHITE else 1
            if board.castle_rights[offset]==0:
                continue
            # if is_square_attacked(boardcopy, move.move_from) or is_square_attacked(boardcopy, move.move_from + 1):
            #     continue
            if not (islegal(boardcopy, None) and islegal(boardcopy, Move(move.move_from, move.move_from + 1))):
                continue
        if move.get_castle() == 2:
            offset = 2 if colour == WHITE else 0
            if board.castle_rights[offset] == 0:
                continue
            # if is_square_attacked(boardcopy, move.move_from) or is_square_attacked(boardcopy, move.move_from - 1):
            #     continue
            if not (islegal(boardcopy, None) and islegal(boardcopy, Move(move.move_from, move.move_from - 1))):
                continue
        if not islegal(boardcopy, move):
            continue
        new_moves.add(move)
    return new_moves

def all_legal_piece_moves(board, move_from,piece):
    moves = calc_piece(board, move_from, piece)
    new_moves = set()
    boardcopy = copy.deepcopy(board)
    colour= piece.colour
    for move in moves:
        if move.get_castle() == 1:
            offset = 3 if colour == WHITE else 1
            if board.castle_rights[offset] == 0:
                continue
            # if is_square_attacked(boardcopy, move.move_from) or is_square_attacked(boardcopy, move.move_from + 1):
            #     continue
            if not (islegal(boardcopy, None) and islegal(boardcopy, Move(move.move_from, move.move_from + 1))):
                continue
        if move.get_castle() == 2:
            offset = 2 if colour == WHITE else 0
            if board.castle_rights[offset] == 0:
                continue
            # if is_square_attacked(boardcopy, move.move_from) or is_square_attacked(boardcopy, move.move_from - 1):
            #     continue
            if not (islegal(boardcopy, None) and islegal(boardcopy, Move(move.move_from, move.move_from - 1))):
                continue
        if not islegal(boardcopy, move):
            continue
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
    board.prev_king_check = board.king_in_check
    board.previous_passants = board.passants.copy()
    board.previous_piece = None
    board.previous_passant_move = False
    board.prev_castle_rights = board.castle_rights.copy()
    board.king_in_check = False
    if board.chessboard[move.move_to]!=0:
        board.previous_piece = board.chessboard[move.move_to]
        if board.chessboard[move.move_to].type == KING:
            board.king_in_check = True
    if board.castle_rights != [0, 0, 0, 0]:
        if move.move_to == 63:
            board.castle_rights[3]=0
        if move.move_to == 56:
            board.castle_rights[2]=0
        if move.move_to == 7:
            board.castle_rights[1]=0
        if move.move_to == 0:
            board.castle_rights[0]=0
        for i in range(4):
            board.castle_rights[i] = move.prevents_castle[i] & board.castle_rights[i]
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
        if move.get_castle() == 1: #short
            chessboard[j] = piece
            chessboard[i + 1] = chessboard[i + 3]
            chessboard[i + 3] = 0
        elif move.get_castle() == 2: #long
            chessboard[j] = piece
            chessboard[i - 1] = chessboard[i - 4]
            chessboard[i - 4] = 0
        else: #en passant
            board.previous_passant_move = True
            which_colour = 1 if piece.colour == BLACK else -1
            chessboard[j-8*which_colour] = 0

    chessboard[j] = piece
    if len(move.enable_passant) > 0:
        board.passants = move.get_passants()
    board.who_to_move = BLACK if board.who_to_move == WHITE else WHITE

def unmake_move(board,move):
    if move is None:
        board.who_to_move = BLACK if board.who_to_move == WHITE else WHITE
        return
    board.king_in_check = board.prev_king_check
    board.passants = board.previous_passants.copy()
    board.castle_rights = board.prev_castle_rights.copy()
    board.who_to_move = BLACK if board.who_to_move == WHITE else WHITE
    i = move.move_from
    j = move.move_to
    chessboard = board.chessboard
    moved_piece = chessboard[j]

    if move.get_castle() == 1:
        chessboard[i] = moved_piece
        chessboard[i + 3] = chessboard[i + 1]
        chessboard[i + 1] = 0
        chessboard[j]=0
        return
    if move.get_castle() == 2:
        chessboard[i] = moved_piece
        chessboard[i - 4] = chessboard[i - 1]
        chessboard[i - 1] = 0
        chessboard[j]=0
        return
    if move.get_promotion() != 0:
        chessboard[j]=0
        chessboard[i] = Piece(PAWN,board.who_to_move)
        if board.previous_piece is not None:
            chessboard[j] = board.previous_piece
        return
    if board.previous_passant_move:
        chessboard[i] = chessboard[j]
        chessboard[j]=0
        which_colour = 1 if moved_piece.colour == BLACK else -1
        chessboard[j-8*which_colour] = Piece(PAWN,BLACK if board.who_to_move == WHITE else WHITE)
        return
    if board.previous_piece is not None:
        chessboard[i] = moved_piece
        chessboard[j] = board.previous_piece
        return
    chessboard[i] = chessboard[j]
    chessboard[j]=0

def islegal(board, move):
    make_move(board, move)
    for movenext in all_moves(board,board.who_to_move):
        if king_capture(board.chessboard, movenext):
            unmake_move(board,move)
            return False
    unmake_move(board, move)
    return True
def is_square_attacked(board, index):
    who_to_move = WHITE if board.who_to_move == BLACK else BLACK
    moves = all_moves(board,who_to_move)
    for move in moves:
        if move.move_to == index:
            return True

    return False

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