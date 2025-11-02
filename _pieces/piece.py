from _enums.color import Color
from enum import Enum, auto
from _enums.pieceValue import PieceValue
from _enums.pieceType import PieceType


class Piece:
    def __init__(self, piece_type: PieceType, color: Color, piece_value: PieceValue, start_pos: tuple):
        self.piece_type = piece_type
        self.color = color
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.piece_value = piece_value

    def __repr__(self):
        return f"{self.color.name} {self.piece_type.name}"
    
    def delete(self):
        self.current_pos = None
    
    def get_position(self):
        return self.current_pos
    
    def move(self, new_square: tuple[int, int], board: "Board"):
        self.current_pos = new_square

    def get_moves(self, board: "Board"):
        return []
    
    def destination_point(self):
        return self.destination_point
    
    def destination_point(self, destination_point):
        self.destination_point = destination_point
        self.change_x = 0.0
        self.change_y = 0.0



    
