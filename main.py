''' Main project executable to trigger gameplay loop, board/piece construction, and bot creation'''
import arcade
from _gui.view import GameView

# constants
def main():
    """ Main function to begin gameplay loop, and call all necessary components"""
    board_pixels = 850
    screen_height = 850
    sidebar_width = 260
    screen_width = board_pixels + sidebar_width
    screen_title = "CS3050 Chess"

    # self._board.print_board()
    window = arcade.Window(screen_width, screen_height, screen_title)
    view = GameView(screen_width, screen_height, screen_title)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
