import arcade
from arcade import color as C
from board.board import Board
from pieces.piece import Piece, PieceType, Color
from gui.view import GameView, draw_board
from game.game import Game

# constants
# TODO: make these dynamic depending on device


def main():
    game = Game()

    BOARD_PIXELS = 850
    SCREEN_HEIGHT = 850
    SIDEBAR_WIDTH = 260
    SCREEN_WIDTH = BOARD_PIXELS + SIDEBAR_WIDTH
    SCREEN_TITLE = "CS3050 Chess"

    #self.board.print_board()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main() 
