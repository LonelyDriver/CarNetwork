import pygame as pg
from settings import *


class Basetile(pg.sprite.Sprite):
    def __init__(self, image, posX, posY, *sprite_groups):
        pg.sprite.Sprite.__init__(self, *sprite_groups)
        self.image = image
        self.image.set_colorkey((0, 0, 0))
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


    def getPosition(self):
        return self.rect.center


class Street(Basetile):
    def __init__(self, image, posX, posY, *sprite_groups):
        Basetile.__init__(self, image, posX, posY, *sprite_groups)


    def onCollision(self):
        pass


class Gras(Basetile):
    def __init__(self,image, posX, posY, *sprite_groups):
        Basetile.__init__(self, image, posX, posY, *sprite_groups)


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
        # finish line
        self.initTile('street100', ((TILESIZE+2)*16, (TILESIZE+2)*3, TILESIZE, TILESIZE))
        self.initTile('street101', ((TILESIZE + 2) * 16, (TILESIZE + 2) * 1, TILESIZE, TILESIZE))
        self.initTile('street102', ((TILESIZE + 2) * 16, (TILESIZE + 2) * 2, TILESIZE, TILESIZE))
        # street only
        self.initTile('street000', ((TILESIZE + 2) * 19, (TILESIZE + 2) * 5, TILESIZE, TILESIZE))
        # poller durchgehend rechts, links, oben, unten
        self.initTile('street200', ((TILESIZE + 2) * 19, (TILESIZE + 2) * 4, TILESIZE, TILESIZE))
        self.initTile('street201', ((TILESIZE + 2) * 19, (TILESIZE + 2) * 6, TILESIZE, TILESIZE))
        self.initTile('street202', ((TILESIZE + 2) * 20, (TILESIZE + 2) * 8, TILESIZE, TILESIZE))
        self.initTile('street203', ((TILESIZE + 2) * 18, (TILESIZE + 2) * 2, TILESIZE, TILESIZE))
        # kurven
        self.initTile('street210', ((TILESIZE + 2) * 20, (TILESIZE + 2) * 6, TILESIZE, TILESIZE))
        self.initTile('street211', ((TILESIZE + 2) * 20, (TILESIZE + 2) * 5, TILESIZE, TILESIZE))
        self.initTile('street212', ((TILESIZE + 2) * 19, (TILESIZE + 2) * 3, TILESIZE, TILESIZE))
        self.initTile('street213', ((TILESIZE + 2) * 19, (TILESIZE + 2) * 2, TILESIZE, TILESIZE))
        # eckpoller rechtsoben, linksoben, linksunten, rechtsunten
        self.initTile('street230', ((TILESIZE + 2) * 17, (TILESIZE + 2) * 11, TILESIZE, TILESIZE))
        self.initTile('street231', ((TILESIZE + 2) * 17, (TILESIZE + 2) * 12, TILESIZE, TILESIZE))
        self.initTile('street232', ((TILESIZE + 2) * 18, (TILESIZE + 2) * 14, TILESIZE, TILESIZE))
        self.initTile('street233', ((TILESIZE + 2) * 19, (TILESIZE + 2) * 0, TILESIZE, TILESIZE))
        # Box
        self.initTile('street240', ((TILESIZE + 2) * 16, (TILESIZE + 2) * 11, TILESIZE, TILESIZE))
        # Gras only
        self.initTile('gras000', ((TILESIZE+2)*7, (TILESIZE+2)*2, TILESIZE, TILESIZE))
        # self.initTile('streetDotRU', ((TILESIZE + 2) * 18, (TILESIZE + 2) * 2, TILESIZE, TILESIZE))


    def getTile(self, name):
        return self.__tile_type[name]


    def initTile(self, name, rectangle):
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.image, (0, 0), rect)
        self.__tile_type[name] = image