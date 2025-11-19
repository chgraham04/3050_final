""" Game class creates and stores a board object, and turn tracker """
from _board.board import Board
from _enums.color import Color

class Game:
    """ Store board object and player turns for gameplay"""
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Color.WHITE
        self.user_color = Color.WHITE