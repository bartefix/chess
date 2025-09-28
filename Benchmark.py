from Bot import Bot
from Board import *

board = Board()
bot = Bot(board)

#bot.benchmark(5,0)
#bot.benchmark(7,1)
#bot.benchmark_search(3,2)
bot.benchmark_puzzles(4)