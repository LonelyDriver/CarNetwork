import pygame as pg
import math as m
from TileMap import Tileset, Street, Gras
import ResourceManager
from settings import *
from Camera import Camera, Map

class IntersectLine:
    def __init__(self, car, camera):
        self.car = car
        self.camera = camera
        self.maxDistance = 300
        # line polynom y = ax + b
        self.rect = self.car.getRect()
        self.rectB = pg.rect.Rect(0, 0, 20, 20)
        self.angle = 0
    def reset(self):
        self.maxDistance = 300

    def update(self):
        # self.rect = self.car.getRect()
        self.rect = self.camera.apply(self.car)
        self.angle = self.car.getAngle()
        # calc endpoint
        self.rectB.x = (m.cos(m.radians(self.angle)) * self.maxDistance) + self.rect.x
        self.rectB.y = (m.sin(m.radians(self.angle)) * self.maxDistance) + self.rect.y

    def render(self, screen):
        pg.draw.line(screen, RED, self.rect.center, self.rectB.center, 2)



class Line:
    def __init__(self, car):
        super().__init__()
        self.car = car
        self.rect = pg.rect.Rect(0, 0, 20, 20)
        self.rectEnd = self.rect
        self.angle = []
        self.maxDistance = 300

    def reset(self):
        self.maxDistance = 300

    def checkCollision(self, grassTiles):
        for tile in grassTiles:
            pos = tile.getPosition()
            vec = [pos[0] - self.rectEnd.x, pos[1] - self.rectEnd.y]
            distance = m.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
            if distance <= HALFTILESIZE:
                print("True")
                # buttom collision
                # if self.rectEnd.x > pos[0] - HALFTILESIZE and \
                #     self.rectEnd.x < pos[0] + HALFTILESIZE and \
                #     self.rectEnd.y > pos[1] - HALFTILESIZE and \
                #     self.rectEnd.y < pos[1] + HALFTILESIZE:



    def update(self):
        self.rect.topleft = self.car.getPos()
        self.angle = self.car.getAngle()

        self.rectEnd.x = m.cos(m.radians(self.angle)) * self.maxDistance
        self.rectEnd.y = m.sin(m.radians(self.angle)) * self.maxDistance


    def render(self, screen, camera):
        a = camera.apply(self)
        b = pg.rect.Rect(0,0, TILESIZE, TILESIZE)
        b.x = self.rectEnd.x + a.x
        b.y = self.rectEnd.y + a.y
        # self.rectEnd.x = self.rectEnd.x + self.rect.x
        # self.rectEnd.y = self.rectEnd.y + self.rect.y
        pg.draw.line(screen, RED, a.topleft, b.topleft, 2)


class Car(pg.sprite.Sprite):
    def __init__(self, manager, sprite_group, worldX, worldY):
        super().__init__()
        sprite_group.add(self)
        self._worldX = worldX
        self._worldY = worldY
        self.rotate = 0
        self.isMoving = False
        self.acc = 0.6
        self.vel = [0, 0]
        self.velVec = [0, 0]
        self.pos = [0, 0]
        self.rot_speed = 3
        self.friction = .9

        self.initImage(manager)
        self.manager = manager
        # line x, y values
        # self.line = pg.rect.Rect(self.pos[0], self.pos[1], worldX, worldY)
        # pygame angle counterclockwise
        # self.abs_angle = 270

    def getRect(self):
        return self.rect

    def getPos(self):
        return self.pos

    def getAngle(self):
        return self.angle

    def getVelVec(self):
        return self.velVec

    def initImage(self, manager):
        self.angle = 270
        self.true_image = manager.getSprite('car')

        self.true_image = pg.transform.rotate(self.true_image, self.angle)
        self.image = self.true_image.copy()

        self.rect = self.true_image.get_rect()
        self.rect.center = (SCREENWIDTH / 2, SCREENHEIGHT / 2)
        self.pos = [SCREENWIDTH * 30, SCREENHEIGHT * 120]

    def processEvents(self):
        keys = pg.key.get_pressed()

        self.isMoving = 0
        self.isMoving += keys[pg.K_w]
        self.isMoving -= keys[pg.K_s]

        # self.isMoving = max(-1, min(1, self.isMoving))

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

        if self.isMoving != 0:
            self.vel[0] = self.vel[0] + m.cos(m.radians(self.angle)) * self.acc * self.isMoving
            self.vel[1] = self.vel[1] + m.sin(m.radians(self.angle)) * self.acc * self.isMoving

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] *= self.friction
        self.vel[1] *= self.friction

        self.rect.center = self.pos

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
        self.isMoving = 0
        self.initImage(self.manager)


class World():
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

        self.car = Car(self.manager, self.entities, self._worldX, self._worldY)
        # self.line = IntersectLine(self.car, self.camera)

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
            self.line.reset()

        self.camera.update(self.car)
        self.line.update()
        # self.line.checkCollision(self.grass)


    def render(self, screen):
        for entity in self.entities:
            screen.blit(entity.image, self.camera.apply(entity))

        # self.line.rect = self.camera.apply(self.line)
        self.line.render(screen)






class Game():
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


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
