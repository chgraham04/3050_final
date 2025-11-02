from dataclasses import dataclass
from _pieces.piece import Piece
from _enums.piece_type import PieceType
from _enums.color import Color
from _enums.piece_value import PieceValue

@dataclass
class King(Piece):

    has_moved: bool = False

    def __init__(self, color: Color, start_pos: tuple):
        piece_value = 1000
        super().__init__(PieceType.KING, color, piece_value, start_pos)
        self.piece_type = PieceType.KING

    def get_position(self):
        return super().get_position()
    
    def move(self, new_square: tuple[int, int], board: "Board"):
        self.current_pos = new_square
        self.has_moved = True
         
    
    def get_moves(self, board, ignore_checks: bool = False):
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
                tile = board.grid[check_square[1]][check_square[0]]

                #See what piece is on the _board; from tile.py
                if not tile.has_piece() or tile.is_other_color(self.color):

                    legal_moves.append((check_square[0], check_square[1]))
        

        #Skips checking for castling if ignore checks turned on - prevents recursion
        if ignore_checks:
            return legal_moves
        ignore_checks = True
        
        #enemy_moves = _board.get_all_enemy_moves(self.color)

        #CASTLING
        if not self.has_moved and not board.check_for_checks(self.color):
            
            if self.color == Color.WHITE:
                row = 0
            else:
                row = 7

            king_rook_tile = board.grid[row][7]
            king_rook = king_rook_tile.piece_here

            #Ensure rook has not moved
            if (king_rook and king_rook.piece_type == PieceType.ROOK):
                rook = king_rook_tile.piece_here

                if not rook.has_moved:

                    #Ensure castling squares are safe from check and have no _pieces occupying
                    if (not board.grid[row][5].has_piece()) and (not board.grid[row][6].has_piece()):
                        legal_moves.append((6, row))

            queen_rook_tile = board.grid[row][0]
            queen_rook = queen_rook_tile.piece_here

            #Ensure rook has not moved
            if (queen_rook and queen_rook.piece_type == PieceType.ROOK):
                rook = queen_rook_tile.piece_here

                if not rook.has_moved:

                    #Ensure castling squares are safe from check and have no _pieces occupying
                    if (not board.grid[row][1].has_piece()) and (not board.grid[row][2].has_piece()) and (not board.grid[row][3].has_piece()):
                        legal_moves.append((2, row))
        
        
        return legal_moves



        


    # stuff