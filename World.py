import pygame as pg
from TileMap import Tileset, Street, Gras
import ResourceManager
from settings import *
from Car import Car, Line
from Camera import Camera, Map


class World:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map("map.txt")
        self._worldX = self.map.width
        self._worldY = self.map.height
        self.camera = Camera(self.map.width, self.map.height)
        self.init()


    def init(self):
        self.entities = pg.sprite.Group()
        self.street = pg.sprite.Group()
        self.grass = pg.sprite.Group()
        self.manager = ResourceManager.Manager()
        self.tileset = Tileset(self.manager)
        self.coords = []
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'a':
                    Street(self.tileset.getTile('street100'), col, row, [self.entities, self.street])
                elif tile == 'b':
                    Street(self.tileset.getTile('street101'), col, row, [self.entities, self.street])
                elif tile == 'c':
                    Street(self.tileset.getTile('street102'), col, row, [self.entities, self.street])
                elif tile == 'd':
                    Street(self.tileset.getTile('street000'), col, row, [self.entities, self.street])
                elif tile == 'e':
                    Street(self.tileset.getTile('street200'), col, row, [self.entities, self.street])
                elif tile == 'f':
                    Street(self.tileset.getTile('street201'), col, row, [self.entities, self.street])
                elif tile == 'g':
                    Street(self.tileset.getTile('street202'), col, row, [self.entities, self.street])
                elif tile == 'h':
                    Street(self.tileset.getTile('street203'), col, row, [self.entities, self.street])
                elif tile == 'i':
                    Street(self.tileset.getTile('street210'), col, row, [self.entities, self.street])
                elif tile == 'j':
                    Street(self.tileset.getTile('street211'), col, row, [self.entities, self.street])
                elif tile == 'k':
                    Street(self.tileset.getTile('street212'), col, row, [self.entities, self.street])
                elif tile == 'l':
                    Street(self.tileset.getTile('street213'), col, row, [self.entities, self.street])
                elif tile == 'm':
                    Street(self.tileset.getTile('street230'), col, row, [self.entities, self.street])
                elif tile == 'n':
                    Street(self.tileset.getTile('street231'), col, row, [self.entities, self.street])
                elif tile == 'o':
                    Street(self.tileset.getTile('street232'), col, row, [self.entities, self.street])
                elif tile == 'p':
                    Street(self.tileset.getTile('street233'), col, row, [self.entities, self.street])
                elif tile == 'q':
                    Street(self.tileset.getTile('street240'), col, row, [self.entities, self.street])
                elif tile == '1':
                    Gras(self.tileset.getTile('gras000'), col, row, self.entities)
                elif tile == '2':
                    Gras(self.tileset.getTile('gras000'), col, row, [self.entities, self.grass])

        self.corners = [[(1*TILESIZE, 2*TILESIZE),(1*TILESIZE, 13*TILESIZE)],
                        [(1*TILESIZE, 13*TILESIZE),(7*TILESIZE, 13*TILESIZE)],
                        [(7*TILESIZE, 13*TILESIZE),(7*TILESIZE, 10*TILESIZE)],
                        [(7*TILESIZE, 10*TILESIZE),(9*TILESIZE, 10*TILESIZE)],
                        [(9*TILESIZE, 10*TILESIZE),(9*TILESIZE, 12*TILESIZE)],
                        [(9*TILESIZE, 12*TILESIZE),(16*TILESIZE, 12*TILESIZE)],
                        [(16*TILESIZE, 12*TILESIZE),(16*TILESIZE, 1*TILESIZE)],
                        [(16*TILESIZE, 1*TILESIZE),(9*TILESIZE, 1*TILESIZE)],
                        [(9*TILESIZE, 1*TILESIZE),(9*TILESIZE, 5*TILESIZE)],
                        [(9*TILESIZE, 5*TILESIZE),(7*TILESIZE, 5*TILESIZE)],
                        [(7*TILESIZE, 5*TILESIZE),(7*TILESIZE, 2*TILESIZE)],
                        [(7*TILESIZE, 2*TILESIZE),(1*TILESIZE, 2*TILESIZE)],
                        [(4*TILESIZE, 4*TILESIZE),(5*TILESIZE, 4*TILESIZE)],
                        [(5*TILESIZE, 4*TILESIZE),(5*TILESIZE, 7*TILESIZE)],
                        [(4*TILESIZE, 4*TILESIZE),(4*TILESIZE, 7*TILESIZE)],
                        [(3*TILESIZE, 7*TILESIZE),(4*TILESIZE, 7*TILESIZE)],
                        [(5 * TILESIZE, 7 * TILESIZE), (11 * TILESIZE, 7 * TILESIZE)],
                        [(11*TILESIZE, 7*TILESIZE),(11*TILESIZE, 3*TILESIZE)],
                        [(11*TILESIZE, 3*TILESIZE),(14*TILESIZE, 3*TILESIZE)],
                        [(14*TILESIZE, 3*TILESIZE),(14*TILESIZE, 10*TILESIZE)],
                        [(14*TILESIZE, 10*TILESIZE),(11*TILESIZE, 10*TILESIZE)],
                        [(11*TILESIZE, 10*TILESIZE),(11*TILESIZE, 8*TILESIZE)],
                        [(11*TILESIZE, 8*TILESIZE),(5*TILESIZE, 8*TILESIZE)],
                        [(5*TILESIZE, 8*TILESIZE),(5*TILESIZE, 11*TILESIZE)],
                        [(5*TILESIZE, 11*TILESIZE),(3*TILESIZE, 11*TILESIZE)],
                        [(3*TILESIZE, 11*TILESIZE),(3*TILESIZE, 7*TILESIZE)]]
        self.car = Car(self.manager, self.entities, self._worldX, self._worldY)
        self.line = Line(self.camera, self.car, self.corners)


    def processEvents(self):
        if(len(self.entities)):
            for entity in self.entities:
                entity.processEvents()
        else:
            print("World is empty!")


    def update(self):
        self.entities.update()
        # collision check
        collisions = pg.sprite.spritecollide(self.car, self.grass, False)
        if collisions:
            self.car.reset()
        self.camera.update(self.car)
        self.line.update()


    def render(self, screen):
        offset = self.camera.getOffset()
        # render tiles
        for entity in self.entities:
            screen.blit(entity.image, self.camera.apply(entity))
        # render lines
        # for line in self.corners:
        #     coords = [(line[0][0]+offset[0], line[0][1]+offset[1]),
        #               (line[1][0]+offset[0], line[1][1]+offset[1])]
        #     pg.draw.lines(screen, RED, True, coords, 2)
        self.line.render(screen)