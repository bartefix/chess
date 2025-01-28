WIDTH = 960
HEIGHT = 960
BLOCK = HEIGHT/8
SIZE = 100
FPS = 100
KING = 1
QUEEN = 2
ROOK = 3
BISHOP = 4
KNIGHT = 5
PAWN = 6
WHITE = 0
BLACK = 6

SHORT = 1
LONG = 2

PLAYING = 1
DRAW = 2
STALEMATE = 3
CHECKMATE = 4

TIMEBETWEENMOVES = 0.1

fenpositions = [ # perft test
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - ",
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
    "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10 "

]
endgame_positions = [
    "5k2/3P4/8/8/8/8/8/4K3 w - - 1 8",
    "8/8/8/8/7p/4K2k/b7/8 w - - 0 71",
    "8/7k/7P/3p1pKp/2p5/2P1P3/8/8 w - - 0 55",
    "4kb2/8/8/8/4P3/8/2K5/8 w - - 0 1"
]
eval_test_positions = [
    "3K4/6q1/8/1b6/8/8/8/6k1 b - - 0 1",
    "4r1k1/p1p2ppp/b1p5/2bqN3/3P4/2P4P/P1P2PP1/R1BQR1K1 b Q - 0 1",
    "r1q1kbnr/pp2pppp/2p5/3p4/1n2P3/5N2/PPPP1PPP/RNB1KB1R b KQkq - 1 6",
    "2k5/1ppr1Bp1/p6p/8/Pb6/4P3/1PP2PPP/R5K1 w - - 1 20"

]
fenpositions_true_values = [
    [1,20,400,8902,197281,4865609],
    [1,48,2039,97862,4085603],
    [1,14,191,2812,43238, 674624],
    [1,6,264,9467,422333],
    [1,44,1486,62379,2103487],
    [1,46,2079,89890,3894594],
]
endgame_positions_true_values = [
    [1,9,33,409,2314,33392,172944,2929931],
    [1,8,81,505,6618,38706,529350,3128924],
    [1,6,34,225,1368,10330,65346,517174],
    [1,9,99,698,9066,62825,840930,5756269]

]
positions_package = [
    [fenpositions,fenpositions_true_values],
    [endgame_positions,endgame_positions_true_values],
]