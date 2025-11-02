from dataclasses import dataclass
from typing import Optional
from pieces.piece import Piece
from enums.color import Color

@dataclass()
class Tile:
    file: int
    rank: int
    is_light_square: bool
    piece_here: Optional[Piece] = None
    highlighted: bool = False

    def has_piece(self) -> bool:
        return self.piece_here is not None
    
    def is_same_color(self, color: Color) -> bool:
        return self.piece_here is not None and self.piece_here.color == color
    
    def is_other_color(self, color: Color) -> bool:
        return self.piece_here is not None and self.piece_here.color != color
    
    def highlight_move(self):
        self.highlighted = True
    
    def clear_highlight(self):
        self.highlighted = False
    
    def get_piece_here(self):
        return self.piece_here
    
    

