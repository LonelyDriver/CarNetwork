import os
import pygame as pg
from enum import Enum, unique


class Manager:
    def __init__(self):
        self.map = []
        self.sprites = {}
        self.directory = (os.path.dirname(__file__))
        sprite_sheet = self._loadImage(os.path.join(self.directory, "assets\Spritesheets\Other.png"))

        car_sprite = self._loadImage(os.path.join(self.directory,"assets\PNG\Cars\car5_red.png"))
        self.sprites['car'] = car_sprite
        self.sprites['sheet'] = sprite_sheet

    def getSprite(self, name):
        return self.sprites[name]

    def _loadImage(self, filename, colorkey=None):
        image = pg.image.load(filename)

        # if image.get_alpha():
        #     image = image.convert()
        # else:
        #     image = image.convert_alpha()
        #
        # if colorkey is not None:
        #     if colorkey is -1:
        #         colorkey = image.get_at((0,0))
        #     image.set_colorkey(colorkey, pg.RLEACCEL)
        return image