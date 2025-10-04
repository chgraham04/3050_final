from dataclasses import dataclass
from typing import Optional
from pieces.piece import Piece

@dataclass()
class Tile:
    file: int
    rank: int
    is_light_square: bool
    piece_here: Optional[Piece] = None