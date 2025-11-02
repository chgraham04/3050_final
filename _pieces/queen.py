from dataclasses import dataclass
from _pieces.piece import Piece
from _enums.piece_type import PieceType
from _enums.color import Color
from _enums.piece_value import PieceValue


@dataclass
class Queen(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.QUEEN, color, PieceValue.QUEEN, start_pos)

    def get_position(self):
        return super().get_position()
    
    def get_moves(self, board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos

        #Potential moves
        possibilities = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for i in range(len(possibilities)):
            x_pos, y_pos = possibilities[i]
            counter = 1
           
            while True:
                check_square = position[0] + x_pos * counter, position[1] + y_pos * counter

                #Ensure square is within bounds of _board
                if not (0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7):
                    break

                tile = board.grid[check_square[1]][check_square[0]]

                if tile is not None and tile.has_piece():
                    if tile.is_same_color(self.color):
                        break
                    else:
                        legal_moves.append(check_square)
                        break

                else:
                    legal_moves.append(check_square)

                counter += 1

        return legal_moves

