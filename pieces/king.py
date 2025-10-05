from dataclasses import dataclass
from piece import Piece
from ..enums.pieceType import PieceType
from ..enums.color import Color
from ..board.board import Board
from ..enums.pieceValue import PieceValue


@dataclass
class King(Piece):
    def __init__(self, color: Color, start_pos: tuple):
        piece_value = 1000
        super().__init__(PieceType.KING, color, piece_value, start_pos)

    def get_position(self):
        return super().get_position()
    
    def get_moves(self, board:Board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos
        

        #Legal moves for King
        move_list = [(1, 0), 
                     (1, 1), 
                     (1, -1), 
                     (-1, -1), 
                     (-1, 0), 
                     (-1, 1), 
                     (0, 1), 
                     (0, -1)]
        
        for i in range(len(move_list)):
            check_square = (position[0] + move_list[i][0], position[1] + move_list[i][1])
            
            #Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[0], check_square[1]]

                #See what piece is on the board; from tile.py
                if not tile.has_piece() or tile.is_opposite_color(self.color):

                    #TODO: Ensure that cannot be moved into check
                    #TODO: Implement castling
                    legal_moves.append((check_square[0], check_square[1]))

        return legal_moves



        


    # stuff