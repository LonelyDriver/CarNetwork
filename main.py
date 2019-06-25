import pygame as pg
import numpy as np
import math as m
import TileMap
import ResourceManager
from settings import *



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

        self.image = manager.getSprite('car')
        # self.image = pg.image.load("assets/PNG/cars/car5_red.png")
        self.image = pg.transform.rotate(self.image, 270)
        self.rot_image = self.image.copy()
        # self.rot_image = pg.transform.rotate(self.image, 270)
        # self.rect = self.rot_image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = [WIDTH/2, HEIGHT/2]

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

        self.rot_image = pg.transform.rotate(self.image, -self.angle)
        self.rect = self.rot_image.get_rect()
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

    def render(self, screen):
        screen.blit(self.rot_image,self.rect)

class World():
    def __init__(self):
        self.entities = pg.sprite.Group()
        self.manager = ResourceManager.Manager()
        self.map = TileMap.Tileset(self.manager)

        for x in range(3):
            for y in range(3):
                if y % 2:
                    TileMap.StreetTile(self.map.getTile('street'),self.entities, x, y)
                else:
                    TileMap.GrasTile(self.map.getTile('gras'), self.entities, x, y)

        Car(self.manager, self.entities)
        stop=1

    def processEvents(self):
        if(len(self.entities)):
            for entity in self.entities:
                entity.processEvents()
        else:
            print("World is empty!")

    def update(self):
        # if(len(self.entities)):
        #     for entity in self.entities:
        #         entity.update()
        self.entities.update()

    def render(self,screen):
        for entity in self.entities:
            entity.render(screen)





class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption("Car Network")

        self.running = False
        self.world = World()

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
