""" Enum for piece color """
from enum import Enum, auto

class Color(Enum):
    """ Pieces are either white or black"""
    WHITE = auto()
    BLACK = auto()

    def opposite(self):
        """ Determine color of player and opponent """
        return Color.BLACK if self == Color.WHITE else Color.WHITE
