import arcade
from arcade import color as Color
from _board.board import Board

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Color.WHITE

