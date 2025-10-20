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
    game.play_game()
    
if __name__ == "__main__":
    main() 
