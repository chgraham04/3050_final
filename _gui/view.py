"""
GUI view module
Contains the GameView class which handles rendering and user interaction
"""
import arcade
import time
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
PREV_SQ = (125, 135, 150)
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
            
            if board.grid[rank][file].prev:
                fill = PREV_SQ
            
            if board.grid[rank][file].highlighted:
                fill = HIGHLIGHT_SQ

            arcade.draw_lbwh_rectangle_filled(x, y, square, square, fill)


def draw_sidepanel(x: int, y: int, width: int, height: int, game: Game, board: Board):
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
    arcade.draw_text("CHESS", x + width // 2, y + height - 40,
                     C.WHITE, 20, anchor_x="center", bold=True)

    # Current turn
    if board.stalemate == False and board.checkmate == False:
        turn_text = "White's Turn" if game.turn == Color.WHITE else "Black's Turn"
    elif board.stalemate == True:
        turn_text = "Stalemate!"
    else: #checkmate
        turn_text = "Checkmate!"

    arcade.draw_text(turn_text, x + width // 2, y + height - 80,
                     C.WHITE, 16, anchor_x="center")

    material_diff = board.material_differential
    # print(f"DEBUG draw_sidepanel: material diff = {material_diff}")
    if board.checkmate == False and board.stalemate == False:
        if material_diff > 0:
            material_msg = f"White + {material_diff}"
        elif material_diff < 0:
            material_msg = f"Black + {abs(material_diff)}"
        else:
            material_msg = f"Even Material"
    elif board.checkmate == True:
        if board.mate_color == Color.WHITE:
            material_msg = f"White Wins!"
        else:
            material_msg = f"Black Wins!"
    else: 
        #Stalemate
        material_msg = f"Draw :/"

    arcade.draw_text(material_msg, x + width // 2, y + height - 120,
                     C.WHITE, 14, anchor_x="center")

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
                       self.window.height, self.game, self.board)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle mouse button press events

        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
            button: Which mouse button was pressed
            key_modifiers: Active keyboard modifiers
        """

        if self.board.checkmate or self.board.stalemate:
            return 
        
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

                    #Check if checkmate or stalemate
                    piece = tile.get_piece_here()
                    if piece.piece_type == PieceType.KING:
                        king_moves = self.board.get_all_legal(piece)
                        if len(king_moves) == 0:

                            #Check if anyone has moves
                            all_moves = self.board.get_all_moves(Color.WHITE)
                            if len(all_moves) == 0:

                                #Checkmate or stalemate
                                enemy_moves = self.board.get_all_enemy_moves(Color.WHITE)

                                if piece.current_pos in enemy_moves: #Checkmate
                                    print("WHITE is in CHECKMATE")
                                    self.board.set_checkmate()
                                    self.board.set_mate_color(Color.BLACK)
                                    return 
                                
                                else:
                                    #Stalemate
                                    print("WHITE is in STALEMATE")
                                    self.board.set_stalemate()
                                    return
                    
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
                    self.board.remove_prev()
                    self.board.move_piece_and_update_sprites(file, rank)
                    self.board.move_piece_and_update_bot()
                    self.board.print_board()

                    self.game.turn = Color.BLACK

                    #Bot turn

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

                    self.board.grid[bot_moves[0][0]][bot_moves[0][1]].prev_move()
                    self.board.grid[bot_moves[1][0]][bot_moves[1][1]].prev_move()

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

        if self.board.checkmate or self.board.stalemate:
            return
        
        #Check if white in checkmate


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

    def move_piece_and_update_bot(self):

        if not self.board.is_curr_pos():
            return
        
        if self.board.checkmate or self.board.stalemate:
            return
        
        #TODO: update to work various of colors
        move_list = self.board.get_all_enemy_moves(color=Color.BLACK)
        if len(move_list) == 0:
            #Stalemate or checkmate

            #Get all player moves
            all_moves = self.board.get_all_moves()

            #Get position of king
            for rank in range(8):
                for file in range(8):
                    piece = self.board.grid[rank][file].piece_here

                    if (piece and piece.color == Color.WHITE and piece.piece_type == PieceType.KING):

                        #If king in moves (checkmate)
                        if self.board.grid[rank][file] in all_moves:

                            #Checkmate
                            print("BLACK is in CHECKMATE")
                            self.board.set_checkmate()
                            self.board.set_mate_color(Color.WHITE)
                            #call function to display that
                            return
                        else:
                            print("BLACK is in STALEMATE")
                            self.board.set_stalemate()
                            #call function to display that
                            return

        
        """ Moves the bot """
        # Bot's turn
        bot_moves = self.bot.next_move(fen=self.board.board_state())
        self.board.selected_piece = (
            self.board.grid[bot_moves[0][0]][bot_moves[0][1]].piece_here
        )
        self.board.move_piece(bot_moves[1][1], bot_moves[1][0])
        self.board.grid[bot_moves[0][0]][bot_moves[0][1]].prev_move()
        self.board.grid[bot_moves[1][0]][bot_moves[1][1]].prev_move()

        # Rebuild sprites again after bot move
        #self.wait()
        self.sprites.build_from_board(
            self.board, self.square, self.origin_x, self.origin_y
        )
        self.board.grid[bot_moves[0][0]][bot_moves[0][1]].prev_move()
        self.board.grid[bot_moves[1][0]][bot_moves[1][1]].prev_move()

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
                    self.move_piece_and_update_bot()
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
    
    def wait(self):
        """ Function waits a second prior to making bot move """
        counter = 1
        start = time.time()
        while time.time() < start + 2:
            pass
    
    def on_key_press(self, symbol, modifiers):
        ''' 
        Handles reactions to key press events
        
        Args:
            symbol: which key was pressed
            modifiers: active keyboard modifiers
        '''
        if symbol == arcade.key.DOWN:
            self.show_prev_move()
        if symbol == arcade.key.UP:
            self.show_next_move()

    def show_prev_move(self):
        ''' Goes backwards one move in history'''
        if self.board.current_index > 0:
            self.board.current_index -= 1
            move = self.board.move_history[self.board.current_index]
            self.board.load_fen(move["FEN"])
            self.sprites.build_from_board(self.board, self.square, self.origin_x, self.origin_y)

    def show_next_move(self):
        ''' Goes forward one move in history '''
        if self.board.current_index < len(self.board.move_history) - 1:
            self.board.current_index += 1
            move = self.board.move_history[self.board.current_index]
            self.board.load_fen(move["FEN"])
            self.sprites.build_from_board(self.board, self.square, self.origin_x, self.origin_y)
