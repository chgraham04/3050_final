import os
from _enums.color import Color
from stockfish import Stockfish
from _game.import_stockfish import import_stockfish


class Bot:
    def __init__(self) -> None:
        stockfish_path = import_stockfish()

        if stockfish_path is None:
            raise FileNotFoundError("Could not find or download Stockfish executable")

        print(f"Using Stockfish at: {stockfish_path}")
        self.stockfish = Stockfish(path=stockfish_path, parameters={"Skill Level": 1})
        self.color = Color.BLACK
        
    def next_move(self, fen: str) -> list[tuple[int, int]]:
        files = {"a": 0, "b": 1, "c": 2,
                 "d": 3, "e": 4, "f": 5,
                 "g": 6, "h": 7}
        position = self.stockfish.set_fen_position(fen)
        best_move = self.stockfish.get_best_move(position)
        print(self.stockfish.is_fen_valid(fen=fen))
        print(best_move)
        start_file = files[best_move[0]]
        start_rank = best_move[1]
        move_to_file = files[best_move[2]]
        move_to_rank = best_move[3]
        return [(int(start_rank) - 1, start_file), (int(move_to_rank) - 1, move_to_file)]
