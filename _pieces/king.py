"""
Models king for game use
"""
from dataclasses import dataclass
from _enums.piece_type import PieceType
from _enums.color import Color
from _pieces.piece import Piece

### -- PYLINT NOTES -- ###
# current_pos initialized in parent class
# __init__ calls super class current_pos assignment, sets self.current_pos

# unused arg 'board' used in move method to track has_moved boolean
# has_moved is REQUIRED for tracking a player's ability to castle

# 16 local vars required to implement king piece functionality

# reducing branches would require pulling the castling logic out of the move function,
# decreasing method override consistency between piece classes
### ------------------ ###

@dataclass
class King(Piece):
    """
    Class representing the king piece
    """
    has_moved: bool = False

    def __init__(self, color: Color, start_pos: tuple):
        """
        Initialize a king piece

        Args:
            color: Color of the piece (White or Black)
            start_pos: Starting position as (file, rank)
        """
        piece_value = 1000
        super().__init__(PieceType.KING, color, piece_value, start_pos)
        self.piece_type = PieceType.KING

    def move(self, new_square: tuple[int, int], board: "Board"):
        """
        Move the king to a new square

        Args:
            new_square: Target position as (file, rank)
            board: The game board (unused but required by parent class)
        """
        self.current_pos = new_square
        self.has_moved = True

    def get_moves(self, board, ignore_checks: bool = False):
        """
        Get all legal moves for the king

        Args:
            board: The game board
            ignore_checks: If True, skip castling logic to prevent recursion
        Returns:
            List of legal move positions as (file, rank) tuples
        """
        legal_moves = []
        position = self.current_pos

        # Legal moves for King
        move_list = [(1, 0),
                     (1, 1),
                     (1, -1),
                     (-1, -1),
                     (-1, 0),
                     (-1, 1),
                     (0, 1),
                     (0, -1)]

        for x_offset, y_offset in move_list:
            check_square = (position[0] + x_offset, position[1] + y_offset)

            # Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]

                # See what piece is on the board; from tile.py
                if not tile.has_piece() or tile.is_other_color(self.color):
                    legal_moves.append((check_square[0], check_square[1]))

        # Skip checking for castling if ignore checks turned on
        # Prevents recursion
        if ignore_checks:
            return legal_moves

        # CASTLING
        if not self.has_moved and not board.check_for_checks(self.color):

            if self.color == Color.WHITE:
                row = 0
            else:
                row = 7

            king_rook_tile = board.grid[row][7]
            king_rook = king_rook_tile.piece_here

            # Ensure rook has not moved
            if king_rook and king_rook.piece_type == PieceType.ROOK:
                rook = king_rook_tile.piece_here

                if not rook.has_moved:
                    # Ensure castling squares have no pieces occupying
                    if (not board.grid[row][5].has_piece() and
                            not board.grid[row][6].has_piece()):
                        legal_moves.append((6, row))

            queen_rook_tile = board.grid[row][0]
            queen_rook = queen_rook_tile.piece_here

            # Ensure rook has not moved
            if queen_rook and queen_rook.piece_type == PieceType.ROOK:
                rook = queen_rook_tile.piece_here

                if not rook.has_moved:
                    # Ensure castling squares have no pieces occupying
                    if (not board.grid[row][1].has_piece() and
                            not board.grid[row][2].has_piece() and
                            not board.grid[row][3].has_piece()):
                        legal_moves.append((2, row))

        return legal_moves
