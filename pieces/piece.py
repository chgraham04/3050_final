from enums.color import Color
from enum import Enum, auto
from enums.pieceValue import PieceValue

class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

class Piece:
    def __init__(self, piece_type: PieceType, color: Color, piece_value: PieceValue, start_pos: tuple):
        self.piece_type = piece_type
        self.color = color
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.piece_value = piece_value

    def __repr__(self):
        return f"{self.color.name} {self.piece_type.name}"
    
    def get_position(self) -> tuple[int, int]:
        return self.current_pos
    
    def move(self, new_square: tuple[int, int]):
        self.current_pos = new_square

    def get_moves(self, board: "Board") -> list[tuple[int, int]]:
        return []
    
    def destination_point(self):
        return self.destination_point
    
    def destination_point(self, destination_point):
        self.destination_point = destination_point
        self.change_x = 0.0
        self.change_y = 0.0



    
