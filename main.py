import pygame as pg
import math as m
from TileMap import Tileset, Street, Gras
import ResourceManager
from settings import *
from Camera import Camera, Map


class Car(pg.sprite.Sprite):
    def __init__(self, manager, sprite_group, worldX, worldY):
        super().__init__()
        sprite_group.add(self)
        self._worldX = worldX
        self._worldY = worldY
        self.rotate = 0
        self.isMoving = False
        self.acc = 0.5
        self.vel = [0, 0]

        self.rot_speed = 2
        self.friction = .94
        self.initImage(manager)
        self.manager = manager


    def initImage(self, manager):
        self.angle = 270
        self.true_image = manager.getSprite('car')

        self.true_image = pg.transform.rotate(self.true_image, self.angle)
        self.image = self.true_image.copy()

        self.rect = self.true_image.get_rect()
        self.rect.center = (SCREENWIDTH / 2, SCREENHEIGHT / 2)
        self.pos = [SCREENWIDTH * 30, SCREENHEIGHT * 120]#

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

        # collision with map dim
        if self.pos[0] <= self.rect.width / 2:
            self.pos[0] = self.rect.width / 2
        if self.pos[1] <= self.rect.height / 2:
            self.pos[1] = self.rect.height / 2
        if self.pos[0] >= self._worldX - self.rect.width / 2:
            self.pos[0] = self._worldX - self.rect.width / 2
        if self.pos[1] >= self._worldY- self.rect.height / 2:
            self.pos[1] = self._worldY - self.rect.height / 2

    def reset(self):
        self.pos = [SCREENWIDTH*30, SCREENHEIGHT*120]
        self.vel = [0, 0]
        self.initImage(self.manager)


class World():
    def __init__(self, screen):
        self.screen = screen
        self.map = Map("map.txt")
        self._worldX = self.map.width
        self._worldY = self.map.height
        self.init()
        self.camera = Camera(self.map.width, self.map.height)

    def init(self):
        self.entities = pg.sprite.Group()
        self.street = pg.sprite.Group()
        self.grass = pg.sprite.Group()
        self.manager = ResourceManager.Manager()
        self.tileset = Tileset(self.manager)
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
                    Gras(self.tileset.getTile('gras000'), col, row, [self.entities, self.grass])

        self.car = Car(self.manager, self.entities, self._worldX, self._worldY)




    def processEvents(self):
        if(len(self.entities)):
            for entity in self.entities:
                entity.processEvents()
        else:
            print("World is empty!")

    def update(self):
        self.entities.update()
        # collision check
        # for entity in self.grass:
        collisions = pg.sprite.spritecollide(self.car, self.grass, False)
        if collisions:
            self.car.reset()

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
