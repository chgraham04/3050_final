"""
Models rook for game use
"""
from dataclasses import dataclass
from _enums.piece_type import PieceType
from _enums.color import Color
from _enums.piece_value import PieceValue
from _pieces.piece import Piece

### -- PYLINT NOTES -- ###
# current_pos initialized in parent class
# __init__ calls super class current_pos assignment, sets self.current_pos

# unused arg 'board' used in move method to track has_moved boolean
# has_moved is REQUIRED for tracking a player's ability to castle
### ------------------ ###

@dataclass
class Rook(Piece):
    """
    Class representing the rook piece
    """
    has_moved: bool = False

    def __init__(self, color: Color, start_pos: tuple[int, int]):
        """
        Initialize a rook piece

        Args:
            color: Color of the piece (White or Black)
            start_pos: Starting position as (file, rank)
        """
        super().__init__(PieceType.ROOK, color, PieceValue.ROOK, start_pos)

    def move(self, new_square: tuple[int, int], board: "Board"):
        """
        Move the rook to a new square

        Args:
            new_square: Target position as (file, rank)
            board: The game board (unused but required by parent class)
        """
        self.current_pos = new_square
        self.has_moved = True

    def get_moves(self, board) -> list[tuple[int, int]]:
        """
        Get all legal moves for the rook

        Args:
            board: The game board
        Returns:
            List of legal move positions as (file, rank) tuples
        """
        legal_moves = []
        position = self.current_pos

        move_list = [(-1, 0),
                     (1, 0),
                     (0, -1),
                     (0, 1)]

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
