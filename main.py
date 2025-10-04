import arcade
from arcade import color as C
from board.board import Board
from pieces.piece import Piece, PieceType, Color
from gui.view import GameView, draw_board

# constants
# TODO: make these dynamic depending on device
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 850
SCREEN_TITLE = "CS3050 Chess"

def main():
    # --- BOARD TESTING --- #
    # board = Board()
    # board.print_board()
    # --- END TESTING --- #

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()