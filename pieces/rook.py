from dataclasses import dataclass
from pieces.piece import Piece
from enums.pieceType import PieceType
from enums.color import Color
from enums.pieceValue import PieceValue
@dataclass
class Rook(Piece):
    def __init__(self, color: Color, start_pos: tuple[int, int]):
        super().__init__(PieceType.ROOK, color, PieceValue.ROOK, start_pos)

    def get_position(self):
        return super().get_position()

    def get_moves(self, board) -> list[tuple[int, int]]:
        legal_moves: list[tuple[int, int]] = []
        r, c = self.current_pos  # (rank, file)

        # 4 sliding directions for a rook (rank/file)
        directions = [
            (1, 0),   # down (toward higher ranks)
            (-1, 0),  # up   (toward lower ranks)
            (0, 1),   # right (higher files)
            (0, -1),  # left  (lower files)
        ]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                tile = board.grid[nr][nc]

                if tile.has_piece():
                    # same color blocks, can't land there
                    if tile.is_same_color(self.color):
                        break
                    # enemy piece: can capture, then stop in this direction
                    if tile.is_other_color(self.color):
                        legal_moves.append((nr, nc))
                        break
                else:
                    # empty: can move and keep sliding
                    legal_moves.append((nr, nc))

                nr += dr
                nc += dc

        return legal_moves
