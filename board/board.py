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
        self.held_cards = None
        self.held_cards_original_pos = None

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
        for x in range(8):
            for y in range(8):
                self.grid[x][y].clear_highlight()

    def get_all_enemy_moves(self, color: Color):

        all_moves = []
        
        #Get moves for each piece
        for rank in range(8):
            for file in range(8):
                piece = self.grid[rank][file].piece_here
                if piece and piece.color == color:
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
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        if (color == Color.WHITE):
            enemy_color = Color.BLACK
        else:
            enemy_color = Color.WHITE
        
        enemy_moves = self.get_all_enemy_moves(enemy_color)
        if king_pos in enemy_moves:
            return True
        else:
            return False
        
    #Function checks to see if moves will put king in check
    def check_if_move_into_check(self, piece: Piece, new_pos: tuple[int, int]):
        current_pos = piece.current_pos
        next_pos = self.grid[new_pos[1]][new_pos[0]]

        #Store piece on target tile
        captured_piece = next_pos.piece_here

        #Simulate move
        self.grid[current_pos[1]][current_pos[0]].piece_here = None
        next_pos.piece_here = piece
        piece.current_pos = next_pos

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

