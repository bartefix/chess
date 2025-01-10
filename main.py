from math import floor

import pygame
import pygame as p
from constants import *
from board import Board
from moves import *

p.init()
button_rect = p.Rect(80, 100, 160, 160)  # x, y, width, height
button_color = (255, 255, 255)

chessboard_img = p.image.load("graphics\chessboard.jpg")
b_king = p.image.load("graphics\\b_king_png_512px.png")
b_queen = p.image.load("graphics\\b_queen_png_512px.png")
b_rook = p.image.load("graphics\\b_rook_png_512px.png")
b_bishop = p.image.load("graphics\\b_bishop_png_512px.png")
b_knight = p.image.load("graphics\\b_knight_png_512px.png")
b_pawn = p.image.load("graphics\\b_pawn_png_512px.png")
w_king = p.image.load("graphics\\w_king_png_512px.png")
w_queen = p.image.load("graphics\\w_queen_png_512px.png")
w_rook = p.image.load("graphics\\w_rook_png_512px.png")
w_bishop = p.image.load("graphics\\w_bishop_png_512px.png")
w_knight = p.image.load("graphics\\w_knight_png_512px.png")
w_pawn = p.image.load("graphics\\w_pawn_png_512px.png")
sniper = p.image.load("graphics\sniper.png")
table = [w_king, w_queen, w_rook, w_bishop, w_knight, w_pawn, b_king, b_queen, b_rook, b_bishop, b_knight, b_pawn]


def resize(image):
    return p.transform.scale(image, (SIZE * image.get_width() / image.get_height(), SIZE))


def draw_piece(i, j, piece):
    type = piece.type + piece.colour
    window.blit(resize(table[type - 1]),
                (j * BLOCK + (BLOCK - table[type - 1].get_width()) / 2, i * BLOCK + BLOCK / 10))


def draw_piece_pixel(i, j, piece):
    type = piece.type + piece.colour
    window.blit(resize(table[type - 1]), (j - table[type - 1].get_width() / 2, i - table[type - 1].get_height() / 2))


def draw_board(board):
    window.blit(p.transform.scale(chessboard_img, (WIDTH, HEIGHT)), (0, 0))
    for i in range(8):
        for j in range(8):
            if board[i, j] != 0:
                draw_piece(i, j, board[i, j])


def retrieve_move(moves, move_from, move_to):
    temp_move = Move(move_from, move_to)
    for move in moves:
        if move == temp_move:
            return move
    return None


def valid_move(board, coords, move_from, piece, who):
    # if min(coords) < 0 or max(coords) > 7:
    #     return False
    if piece.colour != who:
        return None
    moves = calc_piece_passant(board, move_from, piece,passants)
    return retrieve_move(moves, move_from, coords)


def draw_moves(moves):
    for move in moves:
        (i, j) = move.getpair_to()
        window.blit(sniper, (j * BLOCK + 10, i * BLOCK + 10))

def calc_piece_passant(board, move_from, piece,passants):
    moves = calc_piece(board, move_from, piece)
    if piece.type != PAWN:
        return moves
    else:
        for move in passants:
            print(move.getpair_from(), move_from)
            if move.getpair_from() == move_from:
                moves.add(move)
        return moves

def make_move(chessboard, move):
    i = move.move_from
    j = move.move_to
    piece = chessboard[i]
    chessboard[i] = 0
    if move.get_promotion() != 0:
        chessboard[j] = Piece(move.get_promotion(), piece.colour)
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
        global passants
        passants = move.get_passants()

def draw_button():
    p.draw.rect(window, button_color, button_rect)
    font = p.font.Font(None, 64)
    text = font.render("RESTART", True, (0,0,0))
    text_rect = text.get_rect(center=button_rect.center)
    window.blit(text, text_rect)

    if state==DRAW:
        text = font.render("DRAW", True, (0,0,0))
        window.blit(text,(WIDTH//2-text.get_width()//2, 30))
    if state==STALEMATE:
        text = font.render("STALEMATE", True, (0,0,0))
        window.blit(text,(WIDTH//2-text.get_width()//2, 30))
    if state == LOST:
        player = "WHITE" if who_to_move == WHITE else "BLACK"
        text = font.render(f"{player} WON", True, (0, 0, 0))
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

window = p.display.set_mode((WIDTH, HEIGHT))
board = Board()
who_to_move = WHITE
selected_piece = 0
move_piece_from = (-1, -1)
available_moves = set()
passants = set()

state = PLAYING

def setup_game():
    board = Board()
    who_to_move = WHITE
    selected_piece = 0
    move_piece_from = (-1, -1)
    available_moves = set()
    passants = set()

if __name__ == "__main__":
    draw_board(board)
    pygame.display.update()
    run = True
    clock = p.time.Clock()
    while run:
        clock.tick(FPS)
        for event in p.event.get():
            if state != PLAYING:
                draw_board(board)
                draw_button()
                pygame.display.update()
                if event.type == p.QUIT:
                    run = False
                if event.type == p.MOUSEBUTTONUP:
                    if button_rect.collidepoint(event.pos):
                        setup_game()
                        state = PLAYING
                        draw_board(board)
                        pygame.display.update()
            else:
                if event.type == p.QUIT:
                    run = False
                if event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        coords = (floor(event.pos[0] / BLOCK), floor(event.pos[1] / BLOCK))
                        (j, i) = coords
                        coords = (i, j)
                        selected_piece = board[i, j]
                        move_piece_from = coords
                        board[i, j] = 0
                        #print(coords)
                        if selected_piece != 0:
                            draw_board(board)
                            #for move in passants:
                                #print(move.getpair_from(), move.getpair_to())
                            available_moves = calc_piece_passant(board, move_piece_from, selected_piece,passants)
                            draw_moves(available_moves)
                            draw_piece_pixel(event.pos[1], event.pos[0], selected_piece)

                if event.type == p.MOUSEMOTION:
                    if selected_piece != 0:
                        draw_board(board)
                        draw_moves(available_moves)
                        draw_piece_pixel(event.pos[1], event.pos[0], selected_piece)

                if event.type == p.MOUSEBUTTONUP:
                    if selected_piece == 0:
                        continue
                    coords = (floor(event.pos[0] / BLOCK), floor(event.pos[1] / BLOCK))
                    (j, i) = coords
                    coords = (i, j)
                    if (move := valid_move(board, coords, move_piece_from, selected_piece, who_to_move)) is not None:
                        board[move_piece_from] = selected_piece
                        passants.clear()
                        make_move(board.chessboard, move)
                        selected_piece = 0
                        who_to_move = BLACK if who_to_move == WHITE else WHITE
                    else:
                        board[move_piece_from[0], move_piece_from[1]] = selected_piece
                        selected_piece = 0
                    draw_board(board)
        pygame.display.update()
    p.quit()
