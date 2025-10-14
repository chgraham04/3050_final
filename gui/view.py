import arcade
from arcade import color as C
from board.board import Board
from typing import Dict
from pieces.piece import PieceType, Color as PieceColor

# light and dark square colors
LIGHT_SQ = (240, 217, 181)
DARK_SQ  = (181, 136, 99)
HIGHLIGHT_SQ = (118, 150, 86)

def draw_board(board: Board, origin_x: int, origin_y: int, square: int):
    # draw 8x8 grid
    for rank in range(8):
        for file in range(8):
            # 64 unique tile objects assigned
            tile = board.grid[rank][file]
            # coordinates necessary for passing into draw_lbwh_rectangle_filled()
            bottom_left_x = origin_x + file * square
            bottom_left_y = origin_y + rank * square
            top_left = (bottom_left_x, bottom_left_y)
            top_right = (bottom_left_x + square, bottom_left_y + square)
            # determine if light or dark square
            fill = LIGHT_SQ if tile.is_light_square else DARK_SQ

            #Fill color with highlight if legal moves
            if (tile.highlighted):
                fill = HIGHLIGHT_SQ

            arcade.draw_lbwh_rectangle_filled(bottom_left_x, bottom_left_y,square, square, fill)

# establish window
class GameView(arcade.View):
    def __init__(self, width: int, height: int, title: str):
        # calls base python arcade __init__ method
        # window reference isn't passed here, allows for long-term scalability
        super().__init__()
        arcade.set_background_color(C.CADET_BLUE)

        # assign board
        self.board = Board()

        # board layout
        self.square  = width // 8
        self.origin_x = (width  - self.square * 8) // 2
        self.origin_y = (height - self.square * 8) // 2

    def on_draw(self):
        # ensure nothing is overwritten without being cleared
        self.clear()
        draw_board(self.board, self.origin_x, self.origin_y, self.square)