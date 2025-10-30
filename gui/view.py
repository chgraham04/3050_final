import arcade
from arcade import color as C
from board.board import Board
from enums.color import Color
from assets.spritesheet import Spritesheet, ChessSprites
from stockfish import Stockfish
from game.game import Game
from bot.bot import Bot

LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)
HIGHLIGHT_SQ = (118, 150, 86)
SIDEPANEL_BG = (50, 50, 50)


def draw_board(board: Board, origin_x: int, origin_y: int, square: int):
    for rank in range(8):
        for file in range(8):
            x = origin_x + file * square
            y = origin_y + rank * square
            fill = LIGHT_SQ if board.grid[rank][file].is_light_square else DARK_SQ

            if (board.grid[rank][file]).highlighted:
                fill = HIGHLIGHT_SQ

            arcade.draw_lbwh_rectangle_filled(x, y, square, square, fill)


def draw_sidepanel(x: int, y: int, width: int, height: int, game: Game):
    # Background
    arcade.draw_lbwh_rectangle_filled(x, y, width, height, SIDEPANEL_BG)

    # Title
    arcade.draw_text("BLAHBLAHBLAH", x + width // 2, y + height - 40,
                     C.WHITE, 20, anchor_x="center", bold=True)

    # Current turn
    turn_text = "White's Turn" if game.turn == Color.WHITE else "Black's Turn"
    arcade.draw_text(turn_text, x + width // 2, y + height - 80,
                     C.WHITE, 16, anchor_x="center")


class GameView(arcade.View):
    def __init__(self, width: int, height: int, title: str):
        super().__init__()
        arcade.set_background_color(C.CADET_BLUE)

        self.board = Board()
        self.game = Game()
        self.bot = Bot()
        self.square = 850 // 8
        self.origin_x = 0
        self.origin_y = (height - self.square * 8) // 2
        self.sidepanel_x = 850
        self.sidepanel_width = width - 850

        CELL_PIXEL_WIDTH = 256

        # Loader + sprites from assets/spritesheet.py
        self.sheet = Spritesheet("assets/sprites")
        self.sprites = ChessSprites(self.sheet, CELL_PIXEL_WIDTH)
        self.sprites.build_from_board(self.board, self.square, self.origin_x, self.origin_y)

    def on_draw(self):
        self.clear()
        draw_board(self.board, self.origin_x, self.origin_y, self.square)
        self.sprites.draw()
        draw_sidepanel(self.sidepanel_x, 0, self.sidepanel_width,
                       self.window.height, self.game)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            file = int((x - self.origin_x) // self.square)
            rank = int((y - self.origin_y) // self.square)

            if (0 <= file <= 7 and 0 <= rank <= 7):
                tile = self.board.grid[rank][file]

                # TODO: Implement for whichever color's turn it is
                if (tile.has_piece() and tile.piece_here.color == Color.WHITE):
                    print("Piece clicked!")
                    self.board.remove_highlights()
                    self.board.get_piece(tile.piece_here)
                    self.board.highlight_moves()

                elif (self.game.turn == Color.BLACK):
                    print("Not your turn")

                elif (tile.highlighted == True):
                    self.board.remove_highlights()
                    # new funciton in board
                    self.board.move_piece(rank, file, self.board.selected_piece)

                    self.board.print_board()

                    self.game.turn = Color.BLACK

                    bot_moves = self.bot.next_move(fen=self.board.board_state())

                    self.board.selected_piece = self.board.grid[bot_moves[0][0]][bot_moves[0][1]].piece_here

                    self.board.move_piece(bot_moves[1][0], bot_moves[1][1], self.board.selected_piece)

                    self.game.turn = Color.WHITE

                else:
                    self.board.selected_piece = None
                    self.board.remove_highlights()