''' This module calls functions to set up the game window and start the game loop'''
import arcade
from gui.view import GameView

# constants
def main():
    board_pixels = 850
    screen_height = 850
    sidebar_width = 260
    screen_width = board_pixels + sidebar_width
    screen_title = "CS3050 Chess"

    #self.board.print_board()
    window = arcade.Window(screen_width, screen_height, screen_title)
    view = GameView(screen_width, screen_height, screen_title)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
