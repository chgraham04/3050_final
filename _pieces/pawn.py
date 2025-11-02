"""
Models pawn for game use
"""
from dataclasses import dataclass
from _enums.piece_type import PieceType
from _enums.color import Color
from _enums.piece_value import PieceValue
from _pieces.piece import Piece

### -- PYLINT NOTES -- ###
# current_pos initialized in parent class
# __init__ calls super class current_pos assignment, sets self.current_pos
### ------------------ ###

@dataclass
class Pawn(Piece):
    """
    Class representing the pawn piece
    """
    has_moved: bool = False
    en_passant_move: tuple[int, int] = None

    def __init__(self, color: Color, start_pos: tuple):
        """
        Initialize a pawn piece

        Args:
            color: Color of the piece (White or Black)
            start_pos: Starting position as (file, rank)
        """
        super().__init__(PieceType.PAWN, color, PieceValue.PAWN, start_pos)

    def move(self, new_square: tuple[int, int], board: "Board"):
        """
        Move the pawn to a new square

        Args:
            new_square: Target position as (file, rank)
            board: The game board
        """
        old_y = self.current_pos[1]
        new_x, new_y = new_square
        self.has_moved = True
        self.current_pos = new_square

        # Check for moving forwards twice (for en passant)
        if abs(new_y - old_y) == 2:
            mid_y = (old_y + new_y) // 2
            board.en_passant_target = (new_x, mid_y)
        else:
            board.en_passant_target = None

    def get_moves(self, board):
        """
        Get all legal moves for the pawn

        Args:
            board: The game board
        Returns:
            List of legal move positions as (file, rank) tuples
        """
        legal_moves = []
        position = self.current_pos

        if self.color == Color.WHITE:
            direction = 1
        else:
            direction = -1

        regular_move = (0, direction)
        first_move = (0, 2 * direction)
        takes = [(1, direction), (-1, direction)]
        en_passant_moves = [(-1, 0), (1, 0)]

        # Check for standard move
        check_square = (position[0] + regular_move[0], position[1] + regular_move[1])

        if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
            tile = board.grid[check_square[1]][check_square[0]]

            if not tile.has_piece():
                legal_moves.append(check_square)

        # Check for first move
        if not self.has_moved:
            check_square = (position[0] + first_move[0], position[1] + first_move[1])
            check_empty = (position[0], position[1] + direction)

            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]
                empty_tile = board.grid[check_empty[1]][check_empty[0]]

                if not tile.has_piece() and not empty_tile.has_piece():
                    legal_moves.append(check_square)

        # Check for takes
        for x, y in takes:
            check_square = (position[0] + x, position[1] + y)

            # Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]

                # See what piece is on the board; from tile.py
                if tile.has_piece() and tile.is_other_color(self.color):
                    legal_moves.append(check_square)

        # Check for en passant
        for x, y in en_passant_moves:
            check_square = (position[0] + x, position[1] + y)

            if check_square == board.en_passant_target:
                legal_moves.append((check_square[0], check_square[1] + direction))

        return legal_moves
