import arcade
from arcade import color as C
from board.board import Board
from assets.spritesheet import Spritesheet, ChessSprites

LIGHT_SQ = (240, 217, 181)
DARK_SQ  = (181, 136, 99)

def draw_board(board: Board, origin_x: int, origin_y: int, square: int):
    for rank in range(8):
        for file in range(8):
            x = origin_x + file * square
            y = origin_y + rank * square
            fill = LIGHT_SQ if board.grid[rank][file].is_light_square else DARK_SQ
            arcade.draw_lbwh_rectangle_filled(x, y, square, square, fill)

class GameView(arcade.View):
    def __init__(self, width: int, height: int, title: str):
        super().__init__()
        arcade.set_background_color(C.CADET_BLUE)

        self.board = Board()
        self.square  = width // 8
        self.origin_x = (width  - self.square * 8) // 2
        self.origin_y = (height - self.square * 8) // 2

        # Set this to the pixel width of your PNGs (e.g., 256 if your images are 256x256)
        CELL_PIXEL_WIDTH = 256

        # Loader + sprites from assets/spritesheet.py
        self.sheet = Spritesheet("assets/sprites")
        self.sprites = ChessSprites(self.sheet, CELL_PIXEL_WIDTH)
        self.sprites.build_from_board(self.board, self.square, self.origin_x, self.origin_y)

    def on_draw(self):
        self.clear()
        draw_board(self.board, self.origin_x, self.origin_y, self.square)
        self.sprites.draw()
