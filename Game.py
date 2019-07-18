import pygame as pg
from World import World
from settings import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREENWIDTH*TILESIZE, SCREENHEIGHT*TILESIZE))
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