from dataclasses import dataclass
from pieces.piece import Piece
from enums.pieceType import PieceType
from enums.color import Color
from enums.pieceValue import PieceValue

@dataclass
class Bishop(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.BISHOP, color, PieceValue.BISHOP, start_pos)

    def get_position(self):
        return super().get_position()

    def get_moves(self, board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos

        move_list = [(-1, 1),
                     (1, 1),
                     (-1, -1),
                     (1, -1)]

        for i in range(len(move_list)):
            x_pos, y_pos = move_list[i]
            counter = 1

            while True:
                check_square = position[0] + x_pos * counter, position[1] + y_pos * counter

                # Ensure square is within bounds of board
                if not (0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7):
                    break

                tile = board.grid[check_square[1]][check_square[0]]

                if tile is not None:
                    if tile.is_same_color(self.color):
                        break
                    else:
                        legal_moves.append(check_square)
                        break

                else:
                    legal_moves.append(check_square)

                counter += 1

        return legal_moves