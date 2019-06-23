import os
import pygame as pg

class Manager:
    def __init__(self):
        self.map = []
        self.sprites = {}
        self.directory = os.path.join(os.path.dirname(__file__),"assets")


        car_sprite = pg.image.load(os.path.join(self.directory,"PNG\Cars\car5_red.png"))
        self.sprites.update([('car', car_sprite)])

    def loadSprite(self, name):
        return self.sprites[name]