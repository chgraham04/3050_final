''' This module creates the _sprites and draws the _board '''
from __future__ import annotations
import os
from typing import Dict, Tuple
import arcade

piece_names = ["king", "queen", "bishop", "knight", "rook", "pawn"]
color_names = ["white", "black"]

class Spritesheet:
    """
    Simplified spritesheet loader for 12 unique PNGs.
    Loads textures from _assets/_sprites/ and provides them via get_texture().
    """
    def __init__(self, sprites_dir: str = "_assets/_sprites"):
        base_dir = os.path.dirname(__file__)
        self.dir = os.path.normpath(os.path.join(base_dir, "..", sprites_dir))
        self._textures: Dict[Tuple[str, str], arcade.Texture] = {}
        self._load_textures()

    def __repr__(self):
        return "_assets/_sprites"

    def _load_textures(self):
        for color in color_names:
            for piece in piece_names:
                filename = f"{color}_{piece}.png"
                full_path = os.path.join(self.dir, filename)
                if not os.path.exists(full_path):
                    raise FileNotFoundError(f"Missing sprite image: {full_path}")
                tex = arcade.load_texture(full_path)
                self._textures[(color.upper(), piece.upper())] = tex
        print(f"[Spritesheet] Loaded {len(self._textures)} piece textures successfully.")

    def get_texture(self, color, piece_type) -> arcade.Texture:
        """
        Retrieve the correct texture for a piece.
        Accepts either Enum objects or strings for color/piece_type.
        """
        color_name = getattr(color, "name", str(color)).upper()
        piece_name = getattr(piece_type, "name", str(piece_type)).upper()
        return self._textures[(color_name, piece_name)]


class ChessSprites:
    """Manages an Arcade SpriteList for all _board _pieces."""
    def __init__(self, sheet: Spritesheet, cell_pixel_width: int):
        self.sheet = sheet
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.cell_pixel_width = cell_pixel_width
        self._by_piece_id: Dict[int, arcade.Sprite] = {}

    @staticmethod
    def _tile_center(origin_x: int, origin_y: int, square: int,
                      rank: int, file: int) -> tuple[float, float]:
        return (
            origin_x + file * square + square / 2,
            origin_y + rank * square + square / 2,
        )

    def build_from_board(self, board, square: int, origin_x: int, origin_y: int):
        pad: float = 0.88
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self._by_piece_id.clear()

        board.remove_prev()

        desired_w = square * pad
        scale = desired_w / self.cell_pixel_width  # scale against PNG pixel width

        for rank in range(8):
            for file in range(8):
                tile = board.grid[rank][file]
                if not tile.has_piece():
                    continue

                piece = tile.piece_here

                #Checks if piece already has sprite
                if id(piece) in self._by_piece_id:
                    spr = self._by_piece_id[id(piece)]
                    spr.center_x, spr.center_y = self._tile_center(
                        origin_x, origin_y, square, rank, file)

                else:

                    tex = self.sheet.get_texture(piece.color, piece.piece_type)

                    spr = arcade.Sprite(tex, scale=scale)
                    spr.center_x, spr.center_y = self._tile_center(
                        origin_x, origin_y, square, rank, file)
                    self.sprite_list.append(spr)
                    self._by_piece_id[id(piece)] = spr

    def sync_from_board(self, board, square: int, origin_x: int, origin_y: int):
        pad: float = 0.88
        self.build_from_board(board, square, origin_x, origin_y)

        desired_w = square * pad
        scale = desired_w / self.cell_pixel_width

        for rank in range(8):
            for file in range(8):
                tile = board.grid[rank][file]
                if tile.has_piece():
                    piece = tile.piece_here

                    if id(piece) not in self._by_piece_id:
                        tex = self.sheet.get_texture(piece.color, piece.piece_type)

                        spr = arcade.Sprite(tex, scale=scale)
                        spr.center_x, spr.center_y = self._tile_center(
                            origin_x, origin_y, square, rank, file)
                        self.sprite_list.append(spr)
                        self._by_piece_id[id(piece)] = spr
                else:
                    self.remove_sprite_by_piece(tile.piece_here)


    def draw(self):
        self.sprite_list.draw()

    def remove_sprite_by_piece(self, piece: "Piece"):
        sprite = self._by_piece_id.get(id(piece))
        if sprite:
            self._by_piece_id.pop(id(piece))
            self.sprite_list.remove(sprite)
