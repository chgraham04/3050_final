from typing import List
from board.tile import Tile
from pieces.piece import Piece, PieceType, Color, PieceValue
import arcade

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
        # pawns first
        for file in range(8):
            self.grid[1][file].piece_here = Piece(PieceType.PAWN, Color.WHITE, PieceValue.PAWN, (1, file))
            self.grid[6][file].piece_here = Piece(PieceType.PAWN, Color.BLACK, PieceValue.PAWN, (6, file))

        # kings
        self.grid[0][4].piece_here = Piece(PieceType.KING, Color.WHITE, 1000, (0, 4))
        self.grid[7][4].piece_here = Piece(PieceType.KING, Color.BLACK, 1000, (7, 4))

        # queens
        self.grid[0][3].piece_here = Piece(PieceType.QUEEN, Color.WHITE, PieceValue.QUEEN, (0, 3))
        self.grid[7][3].piece_here = Piece(PieceType.QUEEN, Color.BLACK, PieceValue.QUEEN, (7, 3))

        # rooks
        self.grid[0][0].piece_here = Piece(PieceType.ROOK, Color.WHITE, PieceValue.ROOK, (0, 0))
        self.grid[0][7].piece_here = Piece(PieceType.ROOK, Color.WHITE, PieceValue.ROOK, (0, 7))
        self.grid[7][0].piece_here = Piece(PieceType.ROOK, Color.BLACK, PieceValue.ROOK, (7, 0))
        self.grid[7][7].piece_here = Piece(PieceType.ROOK, Color.BLACK, PieceValue.ROOK, (7, 7))

        # knights
        self.grid[0][1].piece_here = Piece(PieceType.KNIGHT, Color.WHITE, PieceValue.KNIGHT, (0, 1))
        self.grid[0][6].piece_here = Piece(PieceType.KNIGHT, Color.WHITE, PieceValue.KNIGHT, (0, 6))
        self.grid[7][1].piece_here = Piece(PieceType.KNIGHT, Color.BLACK, PieceValue.KNIGHT, (7, 1))
        self.grid[7][6].piece_here = Piece(PieceType.KNIGHT, Color.BLACK, PieceValue.KNIGHT, (7, 6))

        # bishops
        self.grid[0][2].piece_here = Piece(PieceType.BISHOP, Color.WHITE, PieceValue.BISHOP, (0, 2))
        self.grid[0][5].piece_here = Piece(PieceType.BISHOP, Color.WHITE, PieceValue.BISHOP, (0, 5))
        self.grid[7][2].piece_here = Piece(PieceType.BISHOP, Color.BLACK, PieceValue.BISHOP, (7, 2))
        self.grid[7][5].piece_here = Piece(PieceType.BISHOP, Color.BLACK, PieceValue.BISHOP, (7, 5))

    def get_piece(self, piece: Piece):
        self.selected_piece = piece

    #Calls highlight_move on tiles with legal moves
    def highlight_moves(self):
        #ensure a piece is selected
        if self.selected_piece:
            legal_moves = self.selected_piece.get_moves(self)
            for move in legal_moves:
                self.grid[move[0]][move[1]].highlight_move()


    #Removes all highlighted legal moves
    def remove_highlights(self):
        for x in range(8):
            for y in range(8):
                self.grid[x][y].clear_highlight()

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
                    symbol = piece_symbols[piece.piece_type]
                    # uppercase for White, lowercase for Black
                    row_str += symbol.upper() + " " if piece.color == Color.WHITE else symbol.lower() + " "
            print(row_str)
        print()

    def on_mouse_release(self, x: float, y:float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass

