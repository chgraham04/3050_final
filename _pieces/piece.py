"""
Models generic piece object for game use
"""
from _enums.color import Color
from _enums.piece_value import PieceValue
from _enums.piece_type import PieceType

### -- PYLINT NOTES -- ###
# 8 instance attributes required to store piece data/implement piece functionality
# no obvious way to refactor this to pass test
### ------------------ ###

class Piece:
    """
    General piece class representing a chess piece
    """

    def __init__(self, piece_type: PieceType, color: Color,
                 piece_value: PieceValue, start_pos: tuple):
        """
        Initialize a chess piece

        Args:
            piece_type: Type of piece (Pawn, Knight, etc.)
            color: Color of the piece (White or Black)
            piece_value: Point value of the piece
            start_pos: Starting position as (file, rank)
        """
        self.piece_type = piece_type
        self.color = color
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.piece_value = piece_value
        self._destination_point = None
        self.change_x = 0.0
        self.change_y = 0.0

    def __repr__(self):
        """
        String representation of the piece

        Returns:
            String showing color and piece type
        """
        return f"{self.color.name} {self.piece_type.name}"

    def delete(self):
        """
        Mark piece as deleted by setting position to None
        """
        self.current_pos = None

    def get_position(self):
        """
        Get the current position of the piece

        Returns:
            Current position as (file, rank) tuple
        """
        return self.current_pos

    def move(self, new_square: tuple[int, int], board: "Board"):
        """
        Move the piece to a new square

        Args:
            new_square: Target position as (file, rank)
            board: The game board (unused in base class)
        """

        # _board unused by this class, but required for specific piece overrides
        _ = board
        self.current_pos = new_square

    def get_moves(self, board: "Board"):
        """
        Get all possible moves for this piece

        Args:
            board: The game board (unused in base class)
        Returns:
            List of valid move positions
        """
        # _board unused by this class, but required for specific piece overrides
        _ = board
        return []

    @property
    def destination_point(self):
        """
        Get the destination point for animation

        Returns:
            The destination point tuple
        """
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        """
        Set the destination point for animation

        Args:
            destination_point: Target destination for animation
        """
        self._destination_point = destination_point
        self.change_x = 0.0
        self.change_y = 0.0
