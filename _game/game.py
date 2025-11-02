""" Game class creates and stores a board object, and turn tracker """
from arcade import color as Color
from _board.board import Board

class Game:
    """ Store board object and player turns for gameplay"""
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Color.WHITE
