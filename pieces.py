
class Piece:
    def __init__(self,type,colour):
        self.type = type
        self.colour = colour
        self.moved = False
    def move(self):
        self.moved=True
