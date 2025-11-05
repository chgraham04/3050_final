from _enums.color import Color

class Player:
    def __init__(self) -> None:
        self.color = Color.WHITE
        self.player_turn = True