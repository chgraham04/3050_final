"""
Models bishop for game use
"""
from dataclasses import dataclass
from _enums.piece_type import PieceType
from _enums.color import Color
from _enums.piece_value import PieceValue
from _pieces.piece import Piece

@dataclass
class Bishop(Piece):
    """
    Class representing the bishop piece
    """
    def __init__(self, color: Color, start_pos: tuple):
        """
        Initialize a bishop piece

        Args:
            color: Color of the piece (White or Black)
            start_pos: Starting position as (file, rank)
        """
        super().__init__(PieceType.BISHOP, color, PieceValue.BISHOP, start_pos)

    def get_moves(self, board) -> list[tuple[int, int]]:
        """
        Get all legal moves for the bishop

        Args:
            board: The game board
        Returns:
            List of legal move positions as (file, rank) tuples
        """
        legal_moves = []
        position = self.current_pos

        move_list = [(-1, 1),
                     (1, 1),
                     (-1, -1),
                     (1, -1)]

        for x_pos, y_pos in move_list:
            counter = 1

            while True:
                check_square = position[0] + x_pos * counter, position[1] + y_pos * counter

                # Ensure square is within bounds of board
                if not (0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7):
                    break

                tile = board.grid[check_square[1]][check_square[0]]

                if tile is not None and tile.has_piece():
                    if tile.is_same_color(self.color):
                        break
                    legal_moves.append(check_square)
                    break

                legal_moves.append(check_square)
                counter += 1

        return legal_moves
