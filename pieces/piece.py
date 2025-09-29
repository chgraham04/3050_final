from dataclasses import dataclass
from ..enums.color import Color
from ..enums.pieceType import PieceType

@dataclass

class Piece:
    color: Color
    pieceType: PieceType

    # generic move function

    # generic symbol function using enum file