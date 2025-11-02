"""
Models knight for game use
"""
from dataclasses import dataclass
from _enums.piece_type import PieceType
from _enums.color import Color
from _enums.piece_value import PieceValue
from _pieces.piece import Piece


@dataclass
class Knight(Piece):
    """
    Class representing the knight piece
    """
    def __init__(self, color: Color, start_pos: tuple):
        """
        Initialize a knight piece

        Args:
            color: Color of the piece (White or Black)
            start_pos: Starting position as (file, rank)
        """
        super().__init__(PieceType.KNIGHT, color, PieceValue.KNIGHT, start_pos)

    def get_moves(self, board) -> list[tuple[int, int]]:
        """
        Get all legal moves for the knight

        Args:
            board: The game board
        Returns:
            List of legal move positions as (file, rank) tuples
        """
        legal_moves = []
        position = self.current_pos

        # Legal moves for knight
        move_list = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2)
        ]

        for x_offset, y_offset in move_list:
            check_square = (position[0] + x_offset, position[1] + y_offset)

            # Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]

                # See what piece is on the board; from tile.py
                if not tile.has_piece() or tile.is_other_color(self.color):
                    legal_moves.append((check_square[0], check_square[1]))

        return legal_moves
