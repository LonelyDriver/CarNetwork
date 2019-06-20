import pygame as pg
import numpy as np
import math as m
import time

T = 60
BACKGROUND_COLOR = (0,240,0)
CAR_COLOR = (200, 50, 20)
WIDTH = 1000
HEIGHT = 800

class Car(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rotate = 0
        self.isMoving = False
        self.acc = .1
        self.vel = [0, 0]
        self.angle = 270

        self.image = pg.Surface([40, 80])
        self.image.fill(CAR_COLOR)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = [WIDTH/2, HEIGHT/2]

    def processEvents(self):
        keys = pg.key.get_pressed()
        self.isMoving = False
        self.isMoving += keys[pg.K_w]

        self.rotate = 0
        self.rotate -= keys[pg.K_a]
        self.rotate += keys[pg.K_d]

    def update(self,deltaTime):
        if self.rotate != 0:
            self.angle = (self.angle + self.rotate * deltaTime * 20) % 360
            vel_mag = m.sqrt(self.vel[0]*self.vel[0] + self.vel[1] * self.vel[1])

            self.vel[0] = m.cos(m.radians(self.angle)) * vel_mag
            self.vel[1] = m.sin(m.radians(self.angle)) * vel_mag
        if self.isMoving:
            self.vel[0] += m.cos(m.radians(self.angle)) * self.acc * deltaTime
            self.vel[1] += m.sin(m.radians(self.angle)) * self.acc * deltaTime

        #self.vel[0] = min(max(self.vel[0] * deltaTime * 10,-1),1)
        #self.vel[1] = min(max(self.vel[1] * deltaTime * 10,-1),1)
        print("vx - {} : vy - {} : angle - {}".format(self.vel[0], self.vel[1], self.angle))

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.rect.center = (self.pos[0], self.pos[1])

    def render(self, screen):
        screen.blit(self.image,self.rect)

class World():
    def __init__(self):
        self.entities = {}

    def addEntity(self, name, entity):
        self.entities.update([(name,entity)])

    def processEvents(self):
        if(len(self.entities)):
            for entity in self.entities.values():
                entity.processEvents()
            #for entity in self.entities:
             #   entity.processEvents()
        else:
            print("World is empty!")


    def update(self, deltaTime):
        if(len(self.entities)):
            for entity in self.entities.values():
                entity.update(deltaTime)

    def render(self,screen):
        for key, entity in self.entities.items():
            entity.render(screen)





class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption("Car Network")

        self.running = False
        self.world = World()
        car = Car()
        self.world.addEntity('car',car)

    def processEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))

        self.world.processEvents()

    def update(self, deltaTime):
        self.world.update(deltaTime)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.world.render(self.screen)
        pg.display.flip()

    def run(self):
        self.running = True
        timePerFrame = 1/T
        lastTime = time.time()

        while(self.running):
            self.processEvents()
            curTime = time.time()
            timeSinceLastUpdate = curTime - lastTime
            lastTime = curTime

            while(timeSinceLastUpdate > timePerFrame):
                timeSinceLastUpdate -= timePerFrame
                self.update(timePerFrame)

            self.update(timePerFrame)
            self.render()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
