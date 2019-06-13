import pygame as pg
import numpy as np

T = 60
BACKGROUND_COLOR = (0,240,0)


class Car(pg.Rect):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.color = (200,10,20)

    def processEvents(self):
        pass

    def update(self,deltaTime):
        pass

    def render(self, screen):
        pg.draw.rect(screen,self.color,self)

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
            if key == "car":
                pg.draw.rect(screen, entity.color,(entity.left,entity.top,entity.width,entity.height))





class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption("Car Network")

        self.running = False
        self.world = World()
        car = Car(300,400,40,80)
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
        clock = pg.time.Clock()
        timePerFrame = 1/T
        timeSinceLastUpdate = clock.tick_busy_loop()

        while(self.running):
            self.processEvents()
            timeSinceLastUpdate -= clock.tick_busy_loop()
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
