from dataclasses import dataclass
from pieces.piece import Piece
from enums.pieceType import PieceType
from enums.color import Color
from enums.pieceValue import PieceValue


@dataclass
class Pawn(Piece):

    has_moved: bool = False

    def __init__(self, color: Color, start_pos: tuple):
        super().__init__(PieceType.PAWN, color, PieceValue.PAWN, start_pos)

    def get_position(self):
        return super().get_position()
    
    def move(self, new_square: tuple[int, int]):
         self.current_pos = new_square
         self.has_moved = True
         

    def get_moves(self, board) -> list[tuple[int, int]]:
        legal_moves = []
        position = self.current_pos

        if self.color == Color.WHITE:
            direction = 1
        else:
            direction = -1

        regular_move = (0, direction)
        first_move = (0, 2 * direction)
        takes = [(1, direction), (-1, direction)]

        #Check for standard move
        check_square = (position[0] + regular_move[0], position[1] + regular_move[1])

        if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]

                if not tile.has_piece():
                     legal_moves.append(check_square) 
        3
        #Check for first move
        if not self.has_moved:
            check_square = (position[0] + first_move[0], position[1] + first_move[1])

            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                    tile = board.grid[check_square[1]][check_square[0]]

                    if not tile.has_piece():
                        legal_moves.append(check_square) 
        
        #Check for takes
        for x, y in takes:
            check_square = (position[0] + x, position[1] + y)
            
            #Ensure square is within bounds and not a friendly piece
            if 0 <= check_square[0] <= 7 and 0 <= check_square[1] <= 7:
                tile = board.grid[check_square[1]][check_square[0]]

                #See what piece is on the board; from tile.py
                if tile.has_piece() and tile.is_other_color(self.color):

                    legal_moves.append((check_square))
        
        print(len(legal_moves)) #Testing
        return legal_moves

        
