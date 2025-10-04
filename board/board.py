from typing import List
from board.tile import Tile
from pieces.piece import Piece, PieceType, Color

class Board:
    def __init__(self) -> None:
        # nested list format
        # creates 8 lists for each row, each with 8 tile objects
        # initialized to none, replaced by Tile objects later
        self.grid: List[List[Tile]] = [[None for _ in range(8)] for _ in range(8)]

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
            self.grid[1][file].piece_here = Piece(PieceType.PAWN, Color.WHITE)
            self.grid[6][file].piece_here = Piece(PieceType.PAWN, Color.BLACK)

        # kings
        self.grid[0][4].piece_here = Piece(PieceType.KING, Color.WHITE)
        self.grid[7][4].piece_here = Piece(PieceType.KING, Color.BLACK)

        # queens
        self.grid[0][3].piece_here = Piece(PieceType.QUEEN, Color.WHITE)
        self.grid[7][3].piece_here = Piece(PieceType.QUEEN, Color.BLACK)

        # rooks
        self.grid[0][0].piece_here = Piece(PieceType.ROOK, Color.WHITE)
        self.grid[0][7].piece_here = Piece(PieceType.ROOK, Color.WHITE)
        self.grid[7][0].piece_here = Piece(PieceType.ROOK, Color.BLACK)
        self.grid[7][7].piece_here = Piece(PieceType.ROOK, Color.BLACK)

        # knights
        self.grid[0][1].piece_here = Piece(PieceType.KNIGHT, Color.WHITE)
        self.grid[0][6].piece_here = Piece(PieceType.KNIGHT, Color.WHITE)
        self.grid[7][1].piece_here = Piece(PieceType.KNIGHT, Color.BLACK)
        self.grid[7][6].piece_here = Piece(PieceType.KNIGHT, Color.BLACK)

        # bishops
        self.grid[0][2].piece_here = Piece(PieceType.BISHOP, Color.WHITE)
        self.grid[0][5].piece_here = Piece(PieceType.BISHOP, Color.WHITE)
        self.grid[7][2].piece_here = Piece(PieceType.BISHOP, Color.BLACK)
        self.grid[7][5].piece_here = Piece(PieceType.BISHOP, Color.BLACK)

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