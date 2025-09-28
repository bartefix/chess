WIDTH = 1280
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

TIMEBETWEENMOVES = 0.2

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
    "4r1k1/p1p2ppp/b1p5/2bqN3/3P4/2P4P/P1P2PP1/R1BQR1K1 b Q - 0 1", #0
    "r1q1kbnr/pp2pppp/2p5/3p4/1n2P3/5N2/PPPP1PPP/RNB1KB1R b KQkq - 1 6",
    "2k5/1ppr1Bp1/p6p/8/Pb6/4P3/1PP2PPP/R5K1 w - - 1 20",
    "8/4k2K/8/8/6q1/8/8/8 b - - 3 2",
    "8/1R6/r6k/5K2/6P1/N4P2/1p6/r7 w - - 9 50",
    "r3k2r/pp1b1ppp/2n1pn2/q2p4/1b1P1B2/P1N2P2/1PPQN1PP/1K1R1B1R b kq - 0 11", #5
    "8/7K/4kq2/8/8/8/8/8 b - - 0 1",
    "4r1k1/1pp2pp1/1b2p2p/r2p4/P2P3q/2P4P/1PQ2PP1/R3R1K1 b - - 0 1",
    "r2qk2r/pp2bppp/2pp1n2/1B6/1n2P1b1/2N1QN2/PPP2PPP/R1B2RK1 b Qkq - 0 1",
    "r2qr1k1/ppp2pbp/2p1b1p1/4N2n/3PPB2/2N5/PPP2PPP/R2QR1K1 w Qq - 0 1",
    "8/1p6/8/6b1/7p/7K/5k2/8 w - - 0 1", #10
    "r1b1kb1r/pppqppp1/2n2n1p/3p4/3PP3/2NB1N2/PPP2PPP/R1BQ1RK1 w q - 1 8",
    "1kr1r3/1ppqbpp1/p2p1nb1/PP1Pp3/2P1P2p/2NBBP1P/5QP1/RR4K1 b - - 0 1",
    "1k1rr3/3qbpp1/RP1p1nb1/3pp3/4P2p/2NBBP1P/Q5P1/1R4K1 b - - 1 8",
    "7k/4p3/6Q1/3P4/8/2B5/PPP1PPPP/RN2KBNR b KQ - 0 1",
    "r5k1/p1p2ppp/2r5/4Rp2/3P2q1/2PQ2P1/P4P1P/R5K1 b Qq - 0 1", #15
]
puzzlerush_positions = [
    ["3k3r/1p6/pq6/3b1p1p/3Q4/8/PP3PPP/R5K1 b - - 0 1","b6d4"],
    ["4r1k1/p1pr1ppp/1p6/5bB1/1P1p3P/2P5/P4PKP/3RR3 w - - 0 1","e1e8"],
    ["3r4/p1k3pp/2p1p3/2P2p2/1P3P2/8/P5PP/R1BQ3K b - - 0 1","d8d1"],
    ["8/2r3pp/4k3/1BP5/P7/4BK2/r4P1P/8 w - - 0 1","b5c4"],
    ["6k1/5ppp/4pb2/3p4/1RrP4/8/3B1PPP/r3NK2 w - - 0 1","b4b8"],
    ["8/8/pK6/6pp/1PP4k/8/8/8 b - - 0 1", "g5g4"],
    ["r4rk1/ppp3p1/2n2qB1/b2ppb1Q/3P3P/2P5/PP3PP1/RN3RK1 w - - 0 1","h5h7"],
    ["r4r1k/2bp1pp1/R1p4p/7q/Q1PNP1P1/3P4/5PP1/2B2RK1 b - - 0 1","h5h2"],
    ["8/p3q1kp/2Q5/2P5/5P2/8/PP4PP/4rBK1 b - - 0 1","e7e3"],
    ["r3r1k1/p1p3pp/b2nNq2/3p1p2/8/2P3P1/PP1N1P1P/R2QR1K1 w - - 0 1","e6c7"],
    ["r3kbnr/p3pppp/3q4/1p1p4/3P4/1B3P1b/PPP2P1P/RNBQR1K1 b kq - 0 1","d6g6"],
    ["r5k1/p1R5/4N3/4pr2/2bp4/2P3p1/PP6/2KR4 w - - 0 1","c7g7"],
    ["2k5/ppp5/3pp3/7p/PPPpP3/3PnqP1/R4Q2/6K1 b - - 0 1", "f3d1"],
    ["K1R5/1R4PP/P4P2/2Pp4/p1qPp3/3p1p1p/6Q1/1rk5 b - - 0 1","c4a6"],
    ["r5kr/p1Q4p/6pB/4pq2/8/3P4/PPP1nbPP/RN3R1K b - - 0 1","e2g3"],
    ["8/6k1/4Qppp/q1p1p3/1n2N1P1/3PK2P/5P2/8 b - - 0 1", "b4c2"],
    ["7k/pp1bqrrp/2p1p3/2PnQ2R/3P1pP1/2P2P2/P5K1/7R w - - 0 1","h5h7"],
    ["r3k2r/p3nppp/4p3/2b1Pb2/4q3/5N2/PP1Q1PPP/2RR2K1 w kq - 0 18","d2d7"],
    ["8/6p1/5k2/pK6/P2P2R1/4P3/6pr/8 b - - 0 1","h2h5"],
    ["r7/P1r3p1/R6p/3kPp2/2pB4/6PP/5PK1/8 w - - 0 1","a6d6"],
    ["8/pR4pk/4p3/5p1K/4n3/P5P1/3r1P2/2R5 b - - 0 1","d2f2"],
    ["r1k4r/ppp1Q3/4N3/4P2p/3P1B1K/5q2/PP5P/nN5R b - - 0 1","f3g4"],
    ["r1b1k3/pp1p2pp/5r2/4B3/4B3/3P2P1/PPn3KP/RN5R b q - 0 1","c2e3"],
    ["3R2r1/1p2Pk1p/p3R3/1q6/4pp2/7P/5PP1/6K1 w - - 2 2","d8g8"],
    ["r4rk1/2q2ppp/p7/n4b2/1p2N3/2bQ1N1P/P1B2PP1/1RR3K1 w - - 0 1","e4f6"],
    ["5r2/3N2R1/2P1B3/3P4/p4kPp/P6K/4b2P/8 b - - 0 1","e2f1"],
    ["r2q2k1/5ppp/PR6/3pP3/3r1p2/1Q3P2/2R3PP/6K1 b - - 0 1","d4d1"],
    ["1r3N1k/pbp1n1p1/1p5p/8/1P2pP2/PBQP2qP/2P3P1/R4RK1 b - - 0 21","e4e3"],
    ["4r1k1/6pp/2bQ1p2/2B5/1n4PK/5q2/1P3P1P/3RR3 b - - 0 1","g7g5"],
    ["rnbk1r2/pppp1p1p/8/4Q3/7q/8/PPP5/RNBK1Bb1 w HQhq - 0 1","c1g5"],
    ["r1b1kr2/pppp2pp/2n5/2bqNQ2/2B2P2/4P1P1/PPP5/RNB1K3 w Qq - 0 1","f5f8"],
    ["r4r2/2p3kp/bp1pp1p1/p3n1N1/5R2/8/P1P3PP/5RK1 w - - 0 1","g5e6"],
    ["4r1k1/ppp2ppp/3p1n2/3b1P2/P2K3P/1PNQ4/2P2R2/R7 b - - 0 1","c7c5"],
    ["2R2Nk1/6p1/5p1p/4pK2/5nP1/8/p3r3/8 w - - 4 44","f8g6"],
    ["2r5/5PKR/1k6/8/7P/p7/8/8 b - - 0 1","a3a2"],
    ["8/3k4/7p/pppPK1p1/2P3P1/1P6/7P/8 w - - 0 1","c4b5"],
    ["8/2K5/8/k7/1p6/1p6/1P6/8 b - - 0 1", "a5b5"],
    ["8/8/5P2/1pb1P3/8/2K4p/6kB/8 w - - 1 46","e5e6"],
    ["3N1R2/p4P1p/6pB/1p1pnk2/1P6/r7/6PK/8 b - - 0 1","e5g4"],
    ["rn1qkb1r/p4ppp/bp2pn2/2pp4/3P1B2/2PBPN2/PP3PPP/RN1QK2R w KQkq - 0 1","d3a6"],
    ["5rk1/3p4/3qp3/3n2pQ/1p6/1P1N4/5PK1/3R4 w - - 0 1","h5g6"],
    ["8/6k1/1P1p3q/3Qpr2/6p1/p1PP2P1/P1R4P/6K1 b - - 0 1","h6e3"],
    ["2Q5/8/8/P3k1p1/3q3p/3n3P/6P1/7K w - - 9 48", "c8h8"],
    ["r7/pbkp1Q2/1p2r1p1/6q1/5N2/8/PP3RPP/RN4K1 b - - 0 1","e6e1"],
    ["5k2/6pp/5p2/3Q4/2r5/4RPq1/1P2K1P1/r7 w - - 1 2","d5d8"],
    ["2kr3r/2p1bpp1/p1P2n1p/1p6/8/N3QB2/PqP2PPP/4RK1R w - - 0 1","e3a1"],
    ["1r3r2/p5pk/1p3n2/5RRP/2P5/2qQp1P1/4PPBK/8 b - - 0 1","c3d3"],

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
    eval_test_positions,
]