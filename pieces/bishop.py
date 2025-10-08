from dataclasses import dataclass
from piece import Piece
from ..enums.pieceType import PieceType
from ..enums.color import Color
from ..enums.pieceValue import PieceValue
from ..board.board import Board


@dataclass
class Bishop(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.BISHOP, color, PieceValue.BISHOP, start_pos)

    def get_position(self):
        return super().get_position()

    def get_moves(self, board: Board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos

        move_list = [(-1, 1),
                     (1, 1),
                     (-1, -1),
                     (-1, 1)]

        # Bishop can move until it hits an edge or hits its same color piece
        # Bishop can take any piece in a clear diagonal path

        # Check for standard move
        check_square = (position[0] + regular_move[0], position[1] + regular_move[1])

        if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
            tile = board.grid[check_square[0], check_square[1]]

            if not tile.has_piece():
                legal_moves.append(check_square)

                # Check for first move
        if (self.has_moved == False):
            check_square = (position[0] + first_move[0], position[1] + first_move[1])

            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[0], check_square[1]]

                if not tile.has_piece():
                    legal_moves.append(check_square)

                    # Check for takes
        for i in range(len(takes)):
            check_square = (position[0] + takes[i][0], position[1] + takes[i][1])

            # Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[0], check_square[1]]

                # See what piece is on the board; from tile.py
                if tile.is_opposite_color(self.color):
                    legal_moves.append((check_square))

        return legal_moves