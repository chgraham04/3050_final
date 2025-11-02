from typing import List
from board.tile import Tile
from pieces.piece import Piece, PieceType, Color, PieceValue
import arcade
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook


class Board:
    def __init__(self) -> None:
        # nested list format
        # creates 8 lists for each row, each with 8 tile objects
        # initialized to none, replaced by Tile objects later
        self.grid: List[List[Tile]] = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.checking_for_checks = False
        self.en_passant_target = None

        # assign tile objects to None lists
        for rank in range(8):
            for file in range(8):
                # determine if tile is light or dark square
                is_light = ((file + rank) % 2 == 1)
                # assign Tile object to list
                # use grid structure to format 2d matrix
                self.grid[rank][file] = Tile(file, rank, is_light)
        self.initialize_pieces()

    # initialize and populate all pieces to starting location on board
    # each corresponding tile is updated with that piece (piece_here)
    def initialize_pieces(self):
        # Pawns
        for file in range(8):
            self.grid[1][file].piece_here = Pawn(Color.WHITE, (file, 1))
            self.grid[6][file].piece_here = Pawn(Color.BLACK, (file, 6))

        # Kings
        self.grid[0][4].piece_here = King(Color.WHITE, (4, 0))
        self.grid[7][4].piece_here = King(Color.BLACK, (4, 7))

        # Queens
        self.grid[0][3].piece_here = Queen(Color.WHITE, (3, 0))
        self.grid[7][3].piece_here = Queen(Color.BLACK, (3, 7))

        # Rooks
        self.grid[0][0].piece_here = Rook(Color.WHITE, (0, 0))
        self.grid[0][7].piece_here = Rook(Color.WHITE, (7, 0))
        self.grid[7][0].piece_here = Rook(Color.BLACK, (0, 7))
        self.grid[7][7].piece_here = Rook(Color.BLACK, (7, 7))

        # Knights
        self.grid[0][1].piece_here = Knight(Color.WHITE, (1, 0))
        self.grid[0][6].piece_here = Knight(Color.WHITE, (6, 0))
        self.grid[7][1].piece_here = Knight(Color.BLACK, (1, 7))
        self.grid[7][6].piece_here = Knight(Color.BLACK, (6, 7))

        # Bishops
        self.grid[0][2].piece_here = Bishop(Color.WHITE, (2, 0))
        self.grid[0][5].piece_here = Bishop(Color.WHITE, (5, 0))
        self.grid[7][2].piece_here = Bishop(Color.BLACK, (2, 7))
        self.grid[7][5].piece_here = Bishop(Color.BLACK, (5, 7))

    def move_piece(self, file, rank):
        before_move = self.selected_piece.get_position()
        before_move_rank = before_move[1]
        before_move_file = before_move[0]

        captured_piece = self.grid[rank][file].piece_here
        if captured_piece:
            captured_piece.delete
        
        self.selected_piece.move((file, rank), self)

        self.grid[rank][file].piece_here = self.selected_piece
        self.grid[before_move_rank][before_move_file].piece_here = None

        piece = self.selected_piece
        if piece.piece_type == PieceType.KING:
            print(f"Moved king from rank {rank} to file {file}")

        print(piece.piece_type == PieceType.PAWN)
        # CASTLING
        if piece.piece_type == PieceType.KING and before_move_file == 4:
            if piece.color == Color.WHITE and rank == 0 and file == 6:
                rook = self.grid[0][7].get_piece_here()
                if rook:
                    self.grid[0][5].piece_here = rook
                    self.grid[0][7].piece_here = None
                    rook.current_pos = (5, 0)
                    print("White short castle")

            elif piece.color == Color.WHITE and rank == 0 and file == 2:
                rook = self.grid[0][0].get_piece_here()
                if rook:
                    self.grid[0][3].piece_here = rook
                    self.grid[0][0].piece_here = None
                    rook.current_pos = (3, 0)
                    print("White long castle")

            elif piece.color == Color.BLACK and rank == 7 and file == 6:
                rook = self.grid[7][7].get_piece_here()
                if rook:
                    self.grid[7][5].piece_here = rook
                    self.grid[7][7].piece_here = None
                    rook.current_pos = (5, 7)
                    print("Black short castle")

            elif piece.color == Color.BLACK and rank == 7 and file == 2:
                rook = self.grid[7][0].get_piece_here()
                if rook:
                    self.grid[7][3].piece_here = rook
                    self.grid[7][0].piece_here = None
                    rook.current_pos = (3, 7)
                    print("Black long castle")

        #Remove captured pieces from sprite list
        piece = self.selected_piece
        enemy_color = Color.BLACK if piece.color == Color.WHITE else Color.WHITE

        if self.check_for_checks(enemy_color):
            print(f"{enemy_color.name} is in check!")

        print(f"{piece.color} {piece.piece_type} moved from {before_move} to {(file, rank)}")    

        self.selected_piece = None
        #self.sprites.build_from_board(self, self.square, self.origin_x, self.origin_y)
        #Deals with en passant
        # if (piece.piece_type == PieceType.PAWN):
        #     self.en_passant(piece, new_pos)


    def get_piece(self, piece: Piece):
        self.selected_piece = piece

    #Calls highlight_move on tiles with legal moves
    def highlight_moves(self):
        #ensure a piece is selected
        if self.selected_piece:
            legal_moves = self.get_all_legal(self.selected_piece)
            for move in legal_moves:
                self.grid[move[1]][move[0]].highlight_move()


    #Removes all highlighted legal moves
    def remove_highlights(self):
        for rank in range(8):
            for file in range(8):
                self.grid[rank][file].clear_highlight()

    def get_all_enemy_moves(self, color: Color):

        all_moves = []
        
        #Get moves for each piece
        for rank in range(8):
            for file in range(8):
                piece = self.grid[rank][file].piece_here
                if piece and piece.color != color and piece.piece_type != PieceType.KING:
                    curr = piece.get_moves(self)

                    for move in curr:
                        if (move not in all_moves):
                            all_moves.append(move)
        
        return all_moves

    #Function finds the player's king
    def find_king(self, color: Color):
        for rank in range(8):
            for file in range(8):
                piece = self.grid[rank][file].piece_here
                if piece and piece.color == color and piece.piece_type.name == "KING":
                    return (file, rank)
        
        return None
    
    #Function checks whether king is currently in check
    def check_for_checks(self, color: Color):
        
        # prevent infinite recursion
        if self.checking_for_checks:
            return False
        
        self.checking_for_checks = True

        try:
            king_pos = self.find_king(color)
            if not king_pos:
                return False

            enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
            enemy_moves = self.get_all_enemy_moves(color)
            return king_pos in enemy_moves
        
        finally:
            self.checking_for_checks = False
        
    #Function checks to see if moves will put king in check
    def check_if_move_into_check(self, piece: Piece, new_pos: tuple[int, int]):
        current_pos = piece.current_pos
        next_pos = self.grid[new_pos[1]][new_pos[0]]

        #Store piece on target tile
        captured_piece = next_pos.piece_here

        #Simulate move
        self.grid[current_pos[1]][current_pos[0]].piece_here = None
        next_pos.piece_here = piece
        piece.current_pos = new_pos

        #See if moves into check
        check = self.check_for_checks(piece.color)

        #Undo move
        self.grid[current_pos[1]][current_pos[0]].piece_here = piece
        next_pos.piece_here = captured_piece
        piece.current_pos = current_pos

        return check
    
    #Returns all legal moves that do not put king in check
    def get_all_legal(self, piece: Piece):
        check_moves = piece.get_moves(self)
        legal_moves = []

        for move in check_moves:
            if not self.check_if_move_into_check(piece, move):
                legal_moves.append(move)

        return legal_moves
    
    #Checks if a certain tile is under threat of enemy pieces
    def check_if_danger(self, color: Color, square: tuple[int, int], enemy_moves: list, visited_squares = None):

        if visited_squares is None:
            visited_squares = set()

        #Prevent recursion
        if square in visited_squares:
            return False

        visited_squares.add(square)

        if square in enemy_moves:
            return True
        
        return False
    
    #Function handles en passant checking and capturing
    def en_passant(self, piece: Pawn, new_pos: tuple[int, int]):
        prev_pos = piece.current_pos

        if self.en_passant_target and new_pos == self.en_passant_target:
                
            if piece.color == Color.WHITE:
                check_square = (new_pos[0], new_pos[1] - 1)
            else:
                check_square = (new_pos[0], new_pos[1] + 1)
            
            self.grid[check_square[1]][check_square[0]].piece_here = None
        
        self.grid[prev_pos[1]][prev_pos[0]].piece_here = None
        self.grid[new_pos[1]][new_pos[0]].piece_here = piece
        piece.current_pos = new_pos
        piece.has_moved = True
    
        self.en_passant_target = None




        


    ### JUST FOR TESTING ###

    def print_board(self):
        piece_symbols = {
            PieceType.PAWN: "P",
            PieceType.KNIGHT: "N",
            PieceType.BISHOP: "B",
            PieceType.ROOK: "R",
            PieceType.QUEEN: "Q",
            PieceType.KING: "K",
        }

        for rank in range(7, -1, -1):  # print rank 8 down to 1
            row_str = ""
            for file in range(8):  # left to right
                piece = self.grid[rank][file].piece_here
                if piece is None:
                    row_str += ". "
                else:
                    symbol = piece.piece_type.value
                    # uppercase for White, lowercase for Black
                    row_str += symbol.upper() + " " if piece.color == Color.WHITE else symbol.lower() + " "
            print(row_str)
        print()

    def board_state(self):
        fen_string = ""
        for rank in range(7, -1, -1):  # print rank 8 down to 1
            fen_row = ""
            empty_count = 0
            for file in range(8):
                piece = self.grid[rank][file].piece_here
                if piece is None:
                    empty_count += 1
                    if file == 7:
                        fen_row = fen_row + str(empty_count)
                else:
                    symbol = piece.piece_type.value
                    if empty_count > 0:
                        fen_row = fen_row + str(empty_count)
                        empty_count = 0
                        fen_row += symbol.upper() if piece.color == Color.WHITE else symbol.lower()
                    else:
                        fen_row += symbol.upper() if piece.color == Color.WHITE else symbol.lower()
            fen_string += (fen_row + "/")
        fen_string = fen_string[:-1]
        return fen_string

    def on_mouse_release(self, x: float, y:float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass

