import os
from _enums.color import Color
from _enums.piece_type import PieceType
from stockfish import Stockfish
from _game.import_stockfish import import_stockfish

class Bot:
    def __init__(self) -> None:
        stockfish_path = import_stockfish()
        if stockfish_path is None:
            raise FileNotFoundError("Could not find or download Stockfish executable")

        print(f"Using Stockfish at: {stockfish_path}")
        self.stockfish = Stockfish(path=stockfish_path, parameters={"UCI_Elo": 100})
        self.color = Color.BLACK

    def set_elo(self, elo: int):
        stockfish_path = import_stockfish()
        self.stockfish = Stockfish(path=stockfish_path, parameters={"UCI_Elo": elo})

    def next_move(self, fen: str) -> list[tuple[int, int]]:
        """Get the next move coordinates from Stockfish"""
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
        print(self.stockfish.get_parameters())
        return [(int(start_rank) - 1, start_file), (int(move_to_rank) - 1, move_to_file)]


    def make_move(self, board, bot_color: Color) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Execute the bot's move on the board.

        Args:
            board: The Board object to make the move on
            bot_color: The color the bot is playing

        Returns:
            Tuple of (from_pos, to_pos) if move was made, None otherwise
        """
        # Check if we can make a move
        if not board.is_curr_pos() or board.checkmate or board.stalemate:
            return None

        # Get best move from Stockfish
        bot_moves = self.next_move(fen=board.board_state(active_color=bot_color))
        from_pos = bot_moves[0]
        to_pos = bot_moves[1]

        # Select and move the piece
        board.selected_piece = board.grid[from_pos[0]][from_pos[1]].piece_here
        board.move_piece(to_pos[1], to_pos[0])

        # Check for pawn promotion
        final_rank = to_pos[0]
        final_file = to_pos[1]
        piece = board.grid[final_rank][final_file].piece_here

        if (piece and piece.piece_type == PieceType.PAWN and
                final_rank == (0 if bot_color == Color.BLACK else 7) and
                piece.color == bot_color):
            print(f"{bot_color.name} PAWN PROMOTED")
            piece.promote()
            board.promote(bot_color, final_file, final_rank)

        return (from_pos, to_pos)