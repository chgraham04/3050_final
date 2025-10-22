import arcade
from arcade import color as C
from board.board import Board
from enums.color import Color
from assets.spritesheet import Spritesheet, ChessSprites
from stockfish import Stockfish
from game.import_stockfish import import_stockfish

LIGHT_SQ = (240, 217, 181)
DARK_SQ  = (181, 136, 99)
HIGHLIGHT_SQ = (118,150,86)

stockfish = Stockfish(path=import_stockfish())

def draw_board(board: Board, origin_x: int, origin_y: int, square: int):
    for rank in range(8):
        for file in range(8):
            x = origin_x + file * square
            y = origin_y + rank * square
            fill = LIGHT_SQ if board.grid[rank][file].is_light_square else DARK_SQ

            if (board.grid[rank][file]).highlighted:
                fill = HIGHLIGHT_SQ
            
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
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            file = int((x - self.origin_x) // self.square)
            rank = int((y - self.origin_y) // self.square)

            if (0 <= file <= 7 and 0 <= rank <= 7):
                tile = self.board.grid[rank][file]
                legal_moves = []
                if (tile.has_piece() and tile.piece_here.color == Color.WHITE):
                    print("Piece clicked!")
                    self.board.remove_highlights()
                    self.board.get_piece(tile.piece_here)
                    self.board.highlight_moves()

                elif(tile.highlighted == True):
                    self.board.remove_highlights()
                    before_move = self.board.selected_piece.get_position()
                    before_move_rank = before_move[1]
                    before_move_file = before_move[0]
                    self.board.grid[rank][file].piece_here = self.board.selected_piece
                    # What does this do?
                    # self.board.selected_piece.move([rank,file])
                    self.board.grid[before_move_rank][before_move_file].piece_here = None
                    self.board.selected_piece = None
                    print(self.board.board_state())
                    self.board.print_board()
                    # fen = self.board.board_state() + " b - - 0 8"
                    # s = stockfish.set_fen_position(fen)
                    # l = stockfish.get_best_move(s)
                    
                    # print(stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
                    # print(l)

                    

                else:
                    self.board.selected_piece = None
                    self.board.remove_highlights()
            

