from enum import Enum, auto

class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    # determine color of player and opponent
    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE