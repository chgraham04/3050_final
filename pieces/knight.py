from dataclasses import dataclass
from piece import Piece
from ..enums.pieceType import PieceType
from ..enums.color import Color
from ..enums.pieceValue import PieceValue


@dataclass
class Knight(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.KNIGHT, color, PieceValue.KNIGHT, start_pos)

    def get_position(self):
        return super().get_position()