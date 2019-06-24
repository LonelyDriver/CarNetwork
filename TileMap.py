import pygame as pg
import ResourceManager

TILESIZE = (64, 64)

class Basetile(pg.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image

class StreetTile(Basetile):
    def __init__(self,image):
        super().__init__(image)
        self.rect = pg.rect.Rect(0, 0, TILESIZE[0], TILESIZE[1])

    def onCollision(self):
        pass

    def processEvents(self):
        pass

    def update(self):
        pass

    def render(self,screen):
        screen.blit(self.image, self.rect)

class Tileset:
    def __init__(self, manager):
        self.tile_type = {}
        self.manager = manager
        self.image = manager.getSprite('sheet')
        self.initialize()

    def initialize(self):
        street = pg.Surface(TILESIZE)
        # ====>>> pg.rect.Rect(pos.x, pos.y, width, height)
        street.blit(self.manager.getSprite('sheet'),(0,0), pg.rect.Rect(64 * 8, 0, TILESIZE[0],TILESIZE[1]))

        self.tile_type['street'] = StreetTile(street)

    def getTile(self, name):
        return self.tile_type[name]


