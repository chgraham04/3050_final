from dataclasses import dataclass
from typing import Optional
from ..pieces.piece import Piece

@dataclass
class Tile:
    row: int
    col: int

    # could also be a boolean variable
    # optional may make it easier to access the actual piece
    piece: Optional[Piece] = None