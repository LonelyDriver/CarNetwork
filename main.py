import pygame as pg
import numpy as np
import math as m
import TileMap
import ResourceManager
from settings import *
from Camera import Camera, Map


class Car(pg.sprite.Sprite):
    def __init__(self, manager, sprite_group):
        super().__init__()
        sprite_group.add(self)
        self.rotate = 0
        self.isMoving = False
        self.acc = 0.5
        self.vel = [0, 0]
        self.angle = 270
        self.rot_speed = 3
        self.friction = .95

        self.true_image = manager.getSprite('car')

        self.true_image = pg.transform.rotate(self.true_image, 270)
        self.image = self.true_image.copy()

        self.rect = self.true_image.get_rect()
        self.rect.center = (SCREENWIDTH/2, SCREENHEIGHT/2)
        self.pos = [SCREENWIDTH*100, SCREENHEIGHT*100]

    def processEvents(self):
        keys = pg.key.get_pressed()
        self.isMoving = False
        self.isMoving += keys[pg.K_w]

        self.rotate = 0
        if self.isMoving:
            self.rotate -= keys[pg.K_a]
            self.rotate += keys[pg.K_d]

    def update(self):
        self.angle = (self.angle + self.rotate * self.rot_speed) % 360
        vel_mag = m.sqrt(self.vel[0]*self.vel[0] + self.vel[1] * self.vel[1])

        self.vel[0] = m.cos(m.radians(self.angle)) * vel_mag
        self.vel[1] = m.sin(m.radians(self.angle)) * vel_mag

        self.image = pg.transform.rotate(self.true_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        if self.isMoving:
            self.vel[0] += m.cos(m.radians(self.angle)) * self.acc
            self.vel[1] += m.sin(m.radians(self.angle)) * self.acc

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] *= self.friction
        self.vel[1] *= self.friction

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

class World():
    def __init__(self, screen):
        self.screen = screen
        self.map = Map("map.txt")
        self.init()
        self.camera = Camera(self.map.width, self.map.height)

    def init(self):
        self.entities = pg.sprite.Group()
        self.manager = ResourceManager.Manager()
        self.tileset = TileMap.Tileset(self.manager)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'a':
                    TileMap.Street(self.tileset.getTile('street100'), self.entities, col, row)
                elif tile == 'b':
                    TileMap.Street(self.tileset.getTile('street101'), self.entities, col, row)
                elif tile == 'c':
                    TileMap.Street(self.tileset.getTile('street102'), self.entities, col, row)
                elif tile == 'd':
                    TileMap.Street(self.tileset.getTile('street000'), self.entities, col, row)
                elif tile == 'e':
                    TileMap.Street(self.tileset.getTile('street200'), self.entities, col, row)
                elif tile == 'f':
                    TileMap.Street(self.tileset.getTile('street201'), self.entities, col, row)
                elif tile == 'g':
                    TileMap.Street(self.tileset.getTile('street202'), self.entities, col, row)
                elif tile == 'h':
                    TileMap.Street(self.tileset.getTile('street203'), self.entities, col, row)
                elif tile == 'i':
                    TileMap.Street(self.tileset.getTile('street210'), self.entities, col, row)
                elif tile == 'j':
                    TileMap.Street(self.tileset.getTile('street211'), self.entities, col, row)
                elif tile == 'k':
                    TileMap.Street(self.tileset.getTile('street212'), self.entities, col, row)
                elif tile == 'l':
                    TileMap.Street(self.tileset.getTile('street213'), self.entities, col, row)
                elif tile == 'm':
                    TileMap.Street(self.tileset.getTile('street230'), self.entities, col, row)
                elif tile == 'n':
                    TileMap.Street(self.tileset.getTile('street231'), self.entities, col, row)
                elif tile == 'o':
                    TileMap.Street(self.tileset.getTile('street232'), self.entities, col, row)
                elif tile == 'p':
                    TileMap.Street(self.tileset.getTile('street233'), self.entities, col, row)
        self.car = Car(self.manager, self.entities)


    def processEvents(self):
        if(len(self.entities)):
            for entity in self.entities:
                entity.processEvents()
        else:
            print("World is empty!")

    def update(self):
        self.entities.update()
        self.camera.update(self.car)

    def render(self, screen):
        for entity in self.entities:
            screen.blit(entity.image, self.camera.apply(entity))





class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREENWIDTH*TILESIZE,SCREENHEIGHT*TILESIZE))
        pg.display.set_caption("Car Network")

        self.running = False
        self.world = World(self.screen)

    def processEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))

        self.world.processEvents()

    def update(self):
        self.world.update()

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.world.render(self.screen)
        pg.display.flip()

    def run(self):
        self.running = True
        clock = pg.time.Clock()

        while(self.running):
            clock.tick(60)
            self.processEvents()
            self.update()
            self.render()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
