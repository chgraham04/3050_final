"""
GUI view module
Contains the GameView class which handles rendering and user interaction
"""
import arcade
from arcade import color as C
from _board.board import Board
from _enums.color import Color
from _enums.piece_type import PieceType
from _assets.spritesheet import Spritesheet, ChessSprites
from _game.game import Game
from _bot.bot import Bot

LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)
HIGHLIGHT_SQ = (118, 150, 86)
SIDEPANEL_BG = (50, 50, 50)


def draw_board(board: Board, origin_x: int, origin_y: int, square: int):
    """
    Draw the chess board with all tiles

    Args:
        board: The Board object to draw
        origin_x: X coordinate of board origin
        origin_y: Y coordinate of board origin
        square: Size of each square in pixels
    """
    for rank in range(8):
        for file in range(8):
            x = origin_x + file * square
            y = origin_y + rank * square
            fill = LIGHT_SQ if board.grid[rank][file].is_light_square else DARK_SQ

            if board.grid[rank][file].highlighted:
                fill = HIGHLIGHT_SQ

            arcade.draw_lbwh_rectangle_filled(x, y, square, square, fill)


def draw_sidepanel(x: int, y: int, width: int, height: int, game: Game):
    """
    Draw the side panel with game information

    Args:
        x: X coordinate of panel
        y: Y coordinate of panel
        width: Width of panel
        height: Height of panel
        game: The Game object containing game state
    """
    # Background
    arcade.draw_lbwh_rectangle_filled(x, y, width, height, SIDEPANEL_BG)

    # Title
    arcade.draw_text("BLAHBLAHBLAH", x + width // 2, y + height - 40,
                     C.WHITE, 20, anchor_x="center", bold=True)

    # Current turn
    turn_text = "White's Turn" if game.turn == Color.WHITE else "Black's Turn"
    arcade.draw_text(turn_text, x + width // 2, y + height - 80,
                     C.WHITE, 16, anchor_x="center")

class GameView(arcade.View):
    """
    Main game view handling rendering and user interaction.
    Manages the chess board, pieces, and player/bot turns.
    """

    def __init__(self, width: int, height: int, title: str):
        """
        Initialize the game view.

        Args:
            width: Window width
            height: Window height
            title: Window title (unused but required by parent)
        """
        super().__init__()
        arcade.set_background_color(C.CADET_BLUE)
        self.window.set_caption(title)

        self.board = Board()
        self.game = Game()
        self.bot = Bot()
        self.square = 850 // 8
        self.origin_x = 0
        self.origin_y = (height - self.square * 8) // 2
        self.sidepanel_x = 850
        self.sidepanel_width = width - 850

        cell_pixel_width = 256

        # Loader + sprites from _assets/spritesheet.py
        self.sheet = Spritesheet("_assets/_sprites")
        self.sprites = ChessSprites(self.sheet, cell_pixel_width)
        self.sprites.build_from_board(
            self.board, self.square, self.origin_x, self.origin_y
        )

        # TRACKERS FOR SPRITE DRAGGING
        self.dragging_sprite = None
        self.drag_start_pos = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def on_draw(self):
        """ Draw the game board, pieces, and side panel """
        self.clear()
        draw_board(self.board, self.origin_x, self.origin_y, self.square)
        self.sprites.draw()
        draw_sidepanel(self.sidepanel_x, 0, self.sidepanel_width,
                       self.window.height, self.game)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle mouse button press events

        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
            button: Which mouse button was pressed
            key_modifiers: Active keyboard modifiers
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Required by python arcade, needed to pass pylint
            # no functionality currently
            if modifiers & arcade.key.MOD_SHIFT:
                pass

            file = int((x - self.origin_x) // self.square)
            rank = int((y - self.origin_y) // self.square)

            if 0 <= file <= 7 and 0 <= rank <= 7:
                tile = self.board.grid[rank][file]

                if tile.has_piece() and tile.piece_here.color == Color.WHITE:
                    self.board.remove_highlights()
                    self.board.get_piece(tile.piece_here)
                    self.board.highlight_moves()

                    # Start dragging the sprite
                    sprite = self.get_sprite_at_position(file, rank)
                    if sprite:
                        self.dragging_sprite = sprite
                        self.drag_start_pos = (file, rank)

                        # Calculate offset
                        self.drag_offset_x = x - sprite.center_x
                        self.drag_offset_y = y - sprite.center_y

                elif self.game.turn == Color.BLACK:
                    print("Not your turn")

                elif tile.highlighted:
                    self.board.remove_highlights()
                    # new function in board
                    self.board.move_piece_and_update_sprites(file, rank)
                    self.board.print_board()

                    self.game.turn = Color.BLACK

                    print(self.board.board_state())  # Debugging
                    bot_moves = self.bot.next_move(
                        fen=self.board.board_state()
                    )

                    self.board.selected_piece = (
                        self.board.grid[bot_moves[0][0]][bot_moves[0][1]]
                        .piece_here
                    )

                    self.board.move_piece_and_update_sprites(
                        bot_moves[1][0], bot_moves[1][1]
                    )

                    self.game.turn = Color.WHITE

                else:
                    self.board.selected_piece = None
                    self.board.remove_highlights()

    def get_tile_from_mouse(self, x, y):
        """
        Convert mouse coordinates to board tile coordinates

        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
        Returns:
            Tuple of (file, rank) or (None, None) if outside board
        """
        file = int((x - self.origin_x) // self.square)
        rank = int((y - self.origin_y) // self.square)

        if 0 <= file <= 7 and 0 <= rank <= 7:
            return file, rank
        return None, None

    def get_sprite_at_position(self, file, rank):
        """
        Find the sprite at a given board position

        Args:
            file: Board file (0-7)
            rank: Board rank (0-7)
        Returns:
            The sprite at that position, or None if not found
        """
        # Calculate the center of the square
        center_x = self.origin_x + file * self.square + self.square // 2
        center_y = self.origin_y + rank * self.square + self.square // 2

        # Find sprite near this position (within half a square)
        for sprite in self.sprites.sprite_list:
            if (abs(sprite.center_x - center_x) < self.square // 2 and
                    abs(sprite.center_y - center_y) < self.square // 2):
                return sprite
        return None

    def move_piece_and_update_sprites(self, file, rank):
        """
        Move a piece and update sprite positions.

        Args:
            file: Target file (0-7)
            rank: Target rank (0-7)
        """
        # Pawn at end of board (promotion)
        piece = self.board.grid[rank][file].piece_here
        if (piece and piece.piece_type == PieceType.PAWN and
                rank == 7 and piece.color == Color.WHITE):
            piece = self.board.grid[rank][file].piece_here
            piece.piece_type = PieceType.QUEEN
            self.board.grid[rank][file].piece_here = piece

        piece = self.board.grid[rank][file].piece_here
        if piece:
            captured_piece = piece
            self.sprites.remove_sprite_by_piece(captured_piece)
            self.board.grid[rank][file].piece_here = None

        # Move piece on board and update sprite positions
        self.board.move_piece(file, rank)

        # Rebuild sprites to show new board state
        self.sprites.build_from_board(
            self.board, self.square, self.origin_x, self.origin_y
        )

        # Reset game state
        self.board.print_board()
        self.game.turn = Color.BLACK

        # Bot's turn
        bot_moves = self.bot.next_move(fen=self.board.board_state())
        self.board.selected_piece = (
            self.board.grid[bot_moves[0][0]][bot_moves[0][1]].piece_here
        )
        self.board.move_piece(bot_moves[1][1], bot_moves[1][0])

        # Rebuild sprites again after bot move
        self.sprites.build_from_board(
            self.board, self.square, self.origin_x, self.origin_y
        )

        # User currently hardcoded as white
        self.game.turn = Color.WHITE

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Handle mouse motion events

        Args:
            x: Current mouse x coordinate
            y: Current mouse y coordinate
            dx: Change in x position
            dy: Change in y position
        """
        # Handle dragging of pieces
        if self.dragging_sprite:
            # Update sprite position to follow mouse
            self.dragging_sprite.center_x = x - self.drag_offset_x
            self.dragging_sprite.center_y = y - self.drag_offset_y

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Handle mouse button release events.

        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
            button: Which mouse button was released
            modifiers: Active keyboard modifiers
        """
        # Required by python arcade, needed to pass pylint
        # no functionality currently
        if modifiers & arcade.key.MOD_SHIFT:
            pass

        # Handle dropping of pieces
        if button == arcade.MOUSE_BUTTON_LEFT and self.dragging_sprite:
            file, rank = self.get_tile_from_mouse(x, y)

            # Check if dropped on valid highlighted square
            if file is not None and rank is not None:
                tile = self.board.grid[rank][file]

                if tile.highlighted:
                    # Valid move
                    self.board.remove_highlights()
                    self.move_piece_and_update_sprites(file, rank)
                else:
                    # Invalid move - snap back to original position
                    orig_file, orig_rank = self.drag_start_pos
                    center = self.sprites._tile_center(
                        self.origin_x, self.origin_y, self.square,
                        orig_rank, orig_file
                    )
                    self.dragging_sprite.center_x = center[0]
                    self.dragging_sprite.center_y = center[1]
                    self.dragging_sprite = None
                    self.drag_start_pos = None
                    self.drag_offset_x = 0
                    self.drag_offset_y = 0
                    return

            else:
                # Dropped outside board - snap back
                orig_file, orig_rank = self.drag_start_pos
                center = self.sprites._tile_center(
                    self.origin_x, self.origin_y, self.square,
                    orig_rank, orig_file
                )
                self.dragging_sprite.center_x = center[0]
                self.dragging_sprite.center_y = center[1]
                self.dragging_sprite = None
                self.drag_start_pos = None
                self.drag_offset_x = 0
                self.drag_offset_y = 0
                return

        self.dragging_sprite = None
        self.drag_start_pos = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
