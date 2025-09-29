import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "CS3050 Chess"

class gameWindow(arcade.View):
    def __init__(self):
        #Initialize variables needed within game
        super().__init__()
        arcade.set_background_color(arcade.csscolor.CADET_BLUE)

    def setup(self):
        #Set variables to proper values here
        pass

    def on_draw(self):
        self.clear()

def main():
    #Creates window class
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    #Creates the game window and show on screen
    game = gameWindow()
    window.show_view(game)

    #Run the game loop
    arcade.run()


if __name__ == "__main__":
    main()