import pygame as pg
import os
import ResourceManager
from settings import *



class Basetile(pg.sprite.Sprite):
    def __init__(self, image, sprite_group, posX, posY):
        super().__init__()
        sprite_group.add(self)
        self.image = image
        self.rect = pg.rect.Rect(0, 0, TILESIZE[0], TILESIZE[1])
        self.setPosition(posX, posY)

    def processEvents(self):
        pass

    def update(self):
        pass

    def render(self,screen):
        screen.blit(self.image, self.rect)

    def setPosition(self, posX, posY):
        self.rect.x = posX * TILESIZE[0]
        self.rect.y = posY * TILESIZE[1]


class StreetTile(Basetile):
    def __init__(self,image, sprite_group, posX, posY):
        super().__init__(image, sprite_group, posX, posY)

    def onCollision(self):
        pass

class GrasTile(Basetile):
    def __init__(self, image, sprite_group, posX, posY):
        super().__init__(image, sprite_group, posX, posY)

    def onCollision(self):
        pass


class Tileset:
    def __init__(self, manager):
        self.manager = manager
        self.image = manager.getSprite('sheet')
        self.__tile_type = {}
        self.initialize()

    def initialize(self):
        self.initTile('street', 8, 0)
        self.initTile('gras', 12, 7)

    def getTile(self, name):
        return self.__tile_type[name]

    def initTile(self, name, countX, countY):
        surface = pg.Surface(TILESIZE)
        surface.blit(self.manager.getSprite('sheet'), (0, 0),
                     pg.rect.Rect(TILESIZE[0] * countX, TILESIZE[0] * countY, TILESIZE[0], TILESIZE[1]))
        self.__tile_type[name] = surface



class Map:
    def __init__(self):
        pass

