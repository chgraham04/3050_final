from dataclasses import dataclass
from piece import Piece
from ..enums.pieceType import PieceType
from ..enums.color import Color
from ..enums.pieceValue import PieceValue
from ..board.board import Board



@dataclass
class Rook(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.ROOK, color, PieceValue.ROOK, start_pos)

    def get_position(self):
        return super().get_position()

    def move(self, new_square: tuple[int, int]):
        return

    def get_moves(self, board:Board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos


