from dataclasses import dataclass
from _pieces.piece import Piece
from _enums.pieceType import PieceType
from _enums.color import Color
from _enums.pieceValue import PieceValue


@dataclass
class Knight(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.KNIGHT, color, PieceValue.KNIGHT, start_pos)

    def get_position(self):
        return super().get_position()
    
    def get_moves(self, board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos

        #Legal moves for knight
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

        for i in range(len(move_list)):
            check_square = (position[0] + move_list[i][0], position[1] + move_list[i][1])
            
            #Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]

                #See what piece is on the _board; from tile.py
                if not tile.has_piece() or tile.is_other_color(self.color):

                    #TODO: Ensure that cannot be moved into check
                    legal_moves.append((check_square[0], check_square[1]))
        
        return legal_moves

