import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
        self.tile_countX = len(self.data[0])-1
        self.tile_countY = len(self.data)
        self.width = self.tile_countX * TILESIZE
        self.height = self.tile_countY * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect((0, 0, width, height))
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREENWIDTH*TILESIZE / 2)
        y = -target.rect.centery + int(SCREENHEIGHT*TILESIZE / 2)

        x = max(-(self.width - SCREENWIDTH*TILESIZE),min(0,x))
        y = max(-(self.height - SCREENHEIGHT * TILESIZE), min(0, y))
        self.camera = pg.Rect(x, y, self.width, self.height)