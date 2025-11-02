""" Enum for piece value """
from enum import Enum

class PieceValue(Enum):
    """ Each piece has unique value """
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
