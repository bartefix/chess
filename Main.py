import copy
import threading
import pygame
import pygame as p
from win32con import NULLREGION

from constants import *
from Board import Board
from evaluation import count_positions, evaluate_position, sort_moves
from moves import *
from Bot import Bot
import time
from Button import Button

p.init()
p.mixer.init()
button_rect = p.Rect(80, 100, 160, 160)  # x, y, width, height
button_color = (255, 255, 255)
cached_background = p.Surface((WIDTH, HEIGHT))
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

move_sound = pygame.mixer.Sound("sounds/move-self.mp3")
capture_sound = pygame.mixer.Sound("sounds/capture.mp3")
check_sound = pygame.mixer.Sound("sounds/move-check.mp3")

def play_sound():

    if board.is_king_checked():
        check_sound.play()
        return

    if board.previous_piece is not None:
        capture_sound.play()
        return

    move_sound.play()

def resize(image):
    return p.transform.scale(image, (SIZE * image.get_width() / image.get_height(), SIZE))

def draw_piece2(i, j, piece, surface):
    type = piece.type + piece.colour
    resized_piece = resize(table[type - 1])
    i,j = (i,j) if not is_board_flipped else (7-i,7-j)
    x = j * BLOCK + (BLOCK - resized_piece.get_width()) / 2
    y = i * BLOCK + BLOCK / 10
    surface.blit(resized_piece, (x, y))

def draw_piece_pixel(x, y, piece):
    if not isinstance(piece, Piece):
        return
    type = piece.type + piece.colour
    window.blit(resize(table[type - 1]), (y - table[type - 1].get_width() / 2, x - table[type - 1].get_height() / 2))

def draw_board(board):
    global cached_background

    cached_background = p.Surface((HEIGHT, HEIGHT))  # Create a new cached surface
    cached_background.blit(p.transform.scale(chessboard_img, (HEIGHT, HEIGHT)), (0, 0))  # Draw the board from top left corner
    window.blit(p.transform.scale(chessboard_img, (HEIGHT, HEIGHT)), (0, 0))
    for i in range(8):
        for j in range(8):
            if board[i, j] != 0 and not move_piece_from == (i,j):
                if lastmove is not None:
                    if lastmove.getpair_to() == (i,j):
                        x,y = (i,j) if not is_board_flipped else (7-i,7-j)
                        p.draw.rect(cached_background, (252,205,76), (y * BLOCK, x * BLOCK, BLOCK, BLOCK))
                draw_piece2(i, j, board[i, j],cached_background)

    ui_rect = p.Rect(HEIGHT, 0, WIDTH-HEIGHT, HEIGHT)
    p.draw.rect(window, (50, 50, 50), ui_rect)
    for button in buttons:
        button.draw(window)

def retrieve_move(moves, move_from, move_to):

    temp_move = Move(move_from, move_to)

    for move in moves:
        if move.move_to == temp_move.move_to and move.move_from == temp_move.move_from:
            if move.get_promotion()==0:
                return move
            if move.get_promotion()==QUEEN:
                return move
    return None

def valid_move(board, coords, move_from, piece, who):
    if piece.colour != who:
        return None
    boardcopy = copy.deepcopy(board)
    new_moves = all_legal_piece_moves(boardcopy, move_from, selected_piece)
    return retrieve_move(new_moves, move_from, coords)

def valid_moves(board,move_from, selected_piece):
    if selected_piece.colour != board.who_to_move:
        return set()
    boardcopy = copy.deepcopy(board)
    return all_legal_piece_moves(boardcopy, move_from, selected_piece)

def draw_moves(moves):
    for move in moves:
        (i, j) = move.getpair_to()
        i,j = (i,j) if not is_board_flipped else (7-i,7-j)
        window.blit(sniper, (j * BLOCK + 10, i * BLOCK + 10))

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

    if state == CHECKMATE:
        player = "WHITE" if board.who_to_move == BLACK else "BLACK"
        text = font.render(f"{player} WON", True, (0, 0, 0))
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

def setup_game():
    global selected_piece, move_piece_from, available_moves,board,bot,state, is_board_flipped, lastmove
    is_board_flipped = False
    board = Board()
    selected_piece = 0
    move_piece_from = (-1, -1)
    available_moves = set()
    bot = Bot(board)
    lastmove = None
    state = PLAYING
    draw_board(board)
    window.blit(cached_background, (0, 0))
    pygame.display.update()

def play_as_bot(depth):
    global lastmove, state, selected_piece,move_piece_from
    draw_board(board)  # Draw board first
    window.blit(cached_background, (0, 0))
    pygame.display.update()
    start_time = time.perf_counter()
    move = bot.give_move(depth)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    if move.getpair_to() == move_piece_from:
        selected_piece = 0
        move_piece_from = (-1, -1)
    make_move(board, move)
    lastmove = move
    draw_board(board)
    window.blit(cached_background, (0, 0))
    play_sound()
    state = isgameover(board)
    if state != PLAYING:
        draw_button()
    pygame.display.update()
    if selected_piece != 0:
        draw_piece_pixel(event.pos[1], event.pos[0], selected_piece)

def flip_board():
    global is_board_flipped
    is_board_flipped = not is_board_flipped
    draw_board(board)
    window.blit(cached_background, (0, 0))
    pygame.display.update()

def switch_sides():
    global WHITE_PLAYER,BLACK_PLAYER
    WHITE_PLAYER = not WHITE_PLAYER
    BLACK_PLAYER = not BLACK_PLAYER

def bot_move(depth,colour):
    play_as_bot(depth)
    board.who_to_move = WHITE if colour == BLACK else BLACK
    global bot_thinking
    bot_thinking = False

def undo_move():
    global board
    if not bot_thinking:
        board = copy.deepcopy(prev_board)
        bot.board = board
        draw_board(board)
        window.blit(cached_background, (0, 0))
        pygame.display.update()
        print(board.who_to_move)

window = p.display.set_mode((WIDTH, HEIGHT))
board = Board()
prev_board = Board()
selected_piece = 0
move_piece_from = (-1, -1)
available_moves = set()
lastmove = None
state = PLAYING
bot = Bot(board)
WHITE_PLAYER = True #false means bot
BLACK_PLAYER = False
is_board_flipped=False
bot_thinking = False

buttons = [
    Button((HEIGHT + 20, 20, 160, 40), "New Game", setup_game, p.font.SysFont(None, 32)),
    Button((HEIGHT + 20, 80, 160, 40), "Flip Board",flip_board, p.font.SysFont(None, 32)),
    Button( (HEIGHT + 20, 140, 160, 40), "Switch sides", switch_sides, p.font.SysFont(None, 32)),
    Button((HEIGHT + 20, 200, 160, 40), "Undo", undo_move, p.font.SysFont(None, 32)),
]

if __name__ == "__main__":

    draw_board(board)
    window.blit(cached_background, (0, 0))
    pygame.display.update()
    run = True
    clock = p.time.Clock()
    first_turn = True

    while run:
        clock.tick(FPS)
        for event in p.event.get():
            if first_turn:
                play_sound()
                first_turn = False

            if board.who_to_move == BLACK and state == PLAYING and not BLACK_PLAYER and not bot_thinking:
                bot_thinking = True
                threading.Thread(target=bot_move, args=(3, BLACK), daemon=True).start()

            if board.who_to_move == WHITE and state == PLAYING and not WHITE_PLAYER and not bot_thinking:
                bot_thinking = True
                threading.Thread(target=bot_move, args=(3, WHITE), daemon=True).start()

            for button in buttons:
                button.handle_event(event)

            if state != PLAYING:

                if event.type == p.QUIT:
                    run = False

                if event.type == p.MOUSEBUTTONUP:
                    if button_rect.collidepoint(event.pos):
                        print("RESTART")
                        setup_game()
            else:
                if event.type == p.QUIT:
                    run = False

                if event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        coords = (floor(event.pos[0] / BLOCK), floor(event.pos[1] / BLOCK))
                        (j, i) = coords
                        i,j = (i,j) if not is_board_flipped else (7-i,7-j)
                        coords = (i, j)
                        if max(i,j)>=8:
                            continue
                        selected_piece = board[i, j]
                        move_piece_from = coords
                        if selected_piece != 0:
                            available_moves = valid_moves(board, move_piece_from, selected_piece)
                            draw_board(board)
                            window.blit(cached_background, (0, 0))
                            draw_piece_pixel(event.pos[1], event.pos[0], selected_piece)
                            draw_moves(available_moves)
                if event.type == p.MOUSEMOTION:
                    if selected_piece != 0:
                        #draw_board(board) <- lowers fps
                        window.blit(cached_background, (0, 0))
                        draw_moves(available_moves)
                        draw_piece_pixel(event.pos[1], event.pos[0], selected_piece)

                if event.type == p.MOUSEBUTTONUP:

                    if selected_piece == 0:
                        continue

                    coords = (floor(event.pos[1] / BLOCK), floor(event.pos[0] / BLOCK))
                    i,j = coords
                    coords = (i, j) if not is_board_flipped else (7-i,7-j)
                    if (move := valid_move(board, coords, move_piece_from, selected_piece, board.who_to_move)) is not None and not bot_thinking:
                        prev_board = copy.deepcopy(board)
                        board[move_piece_from] = selected_piece
                        make_move(board, move)
                        lastmove = move
                        play_sound()
                    else:
                         if board[move_piece_from[0], move_piece_from[1]] != 0:
                             board[move_piece_from[0], move_piece_from[1]] = selected_piece

                    selected_piece = 0
                    move_piece_from = (-1, -1)
                    draw_board(board)
                    window.blit(cached_background, (0, 0))
                    state = isgameover(board)

        pygame.display.update()
    p.quit()
