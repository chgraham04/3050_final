from dataclasses import dataclass
from piece import Piece
from ..enums.pieceType import PieceType
from ..enums.color import Color


@dataclass
class Queen(Piece):
    color: Color

    # stuff