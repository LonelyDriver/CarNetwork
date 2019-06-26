import pygame as pg
from settings import *


class Basetile(pg.sprite.Sprite):
    def __init__(self, image, sprite_group, posX, posY):
        super().__init__()
        sprite_group.add(self)
        self.image = image
        self.rect = pg.rect.Rect(0, 0, TILESIZE, TILESIZE)
        self.setPosition(posX, posY)

    def processEvents(self):
        pass

    def update(self):
        pass

    def render(self,screen):
        screen.blit(self.image, self.rect)

    def setPosition(self, posX, posY):
        self.rect.x = posX * TILESIZE
        self.rect.y = posY * TILESIZE


class FinishTile1(Basetile):
    def __init__(self,image, sprite_group, posX, posY):
        super().__init__(image, sprite_group, posX, posY)

    def onCollision(self):
        pass

class FinishTile2(Basetile):
    def __init__(self,image, sprite_group, posX, posY):
        super().__init__(image, sprite_group, posX, posY)

    def onCollision(self):
        pass

class FinishTile3(Basetile):
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
        # Sprite is 128x128 pixels at 0,0 on the spritesheet
        # distance between sprites is 130x130 pixels
        self.initTile('finish1', ((TILESIZE+2)*16, (TILESIZE+2)*3, TILESIZE, TILESIZE))
        self.initTile('finish2', ((TILESIZE + 2) * 16, (TILESIZE + 2) * 1, TILESIZE, TILESIZE))
        self.initTile('finish3', ((TILESIZE + 2) * 16, (TILESIZE + 2) * 2, TILESIZE, TILESIZE))
        self.initTile('grass', ((TILESIZE+2)*8,(TILESIZE+2) * 10 , TILESIZE, TILESIZE))

    def getTile(self, name):
        return self.__tile_type[name]

    # def initTile(self, name, countX, countY):
    #     surface = pg.Surface((TILESIZE, TILESIZE))
    #     surface.blit(self.manager.getSprite('sheet'),
    #                  dest=(0,0),
    #                  area=pg.rect.Rect(TILESIZE * countX, TILESIZE * countY, TILESIZE, TILESIZE))
    #     self.__tile_type[name] = surface

    def initTile(self, name, rectangle):
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.image, (0, 0), rect)
        self.__tile_type[name] = image