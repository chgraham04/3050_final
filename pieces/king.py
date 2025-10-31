from dataclasses import dataclass
from pieces.piece import Piece
from enums.pieceType import PieceType
from enums.color import Color
from enums.pieceValue import PieceValue

@dataclass
class King(Piece):

    has_moved: bool = False

    def __init__(self, color: Color, start_pos: tuple):
        piece_value = 1000
        super().__init__(PieceType.KING, color, piece_value, start_pos)

    def get_position(self):
        return super().get_position()
    
    def move(self, new_square: tuple[int, int], board: "Board"):
        self.current_pos = new_square
        self.has_moved = True
         
    
    def get_moves(self, board, ignore_checks: bool = False):
        legal_moves = []
        position = self.current_pos
        print(ignore_checks)
        

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

                #See what piece is on the board; from tile.py
                if not tile.has_piece() or tile.is_other_color(self.color):

                    legal_moves.append((check_square[0], check_square[1]))
        
        return legal_moves

        #Skips checking for castling if ignore checks turned on - prevents recursion
        if ignore_checks:
            return legal_moves
        
        print("Still goin")

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

                    #Ensure castling squares are safe from check and have no pieces occupying
                    if (not board.grid[row][5].has_piece()) and (not board.grid[row][6].has_piece()):
                        if (not board.check_if_danger(self.color, (5, row))) and (not board.check_if_danger(self.color, (5, row))):
                            legal_moves.append((6, row))

            queen_rook_tile = board.grid[row][0]
            queen_rook = queen_rook_tile.piece_here

            #Ensure rook has not moved
            if (queen_rook and queen_rook.piece_type == PieceType.ROOK):
                rook = queen_rook_tile.piece_here

                if not rook.has_moved:

                    #Ensure castling squares are safe from check and have no pieces occupying
                    if (not board.grid[row][1].has_piece()) and (not board.grid[row][2].has_piece()) and (not board.grid[row][3].has_piece()):
                        if (not board.check_if_danger(self.color, (2, row))) and (not board.check_if_danger(self.color, (3, row))):
                            legal_moves.append((2, row))
        
        
        return legal_moves



        


    # stuff