import arcade
from arcade import color as C
from board.board import Board
from pieces.piece import Piece, PieceType, Color
from gui.view import GameView, draw_board

class Game:
    def __init__(self) -> None:
        self.board = Board()

    def play_game(self):
        SCREEN_WIDTH = 850
        SCREEN_HEIGHT = 850
        SCREEN_TITLE = "CS3050 Chess"
        self.board.print_board()
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        window.show_view(view)
        arcade.run()
        
        if self.board.selected_piece != None:
            print("Hello")
        view.board.on_mouse_motion
