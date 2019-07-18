from settings import *
import math as m
import pygame as pg


class Line:
    def __init__(self, camera, car, corners):
        self.car = car
        self.camera = camera
        self.corners = corners
        self.line = []
        self.intersections = []


    def getStateVec(self):
        a = m.sqrt(self.intersections[0][0] * self.intersections[0][0] + self.intersections[0][1] * self.intersections[0][1])
        b = m.sqrt(self.intersections[1][0] * self.intersections[1][0] + self.intersections[1][1] * self.intersections[1][1])
        c = m.sqrt(self.intersections[2][0] * self.intersections[2][0] + self.intersections[2][1] * self.intersections[2][1])
        return [a, b, c]


    def update(self):
        angles = [self.car.getAngle(), self.car.getAngle() + 34, self.car.getAngle() - 34, self.car.getAngle() + 89, self.car.getAngle() - 89]
        if angles[0] == 270 or angles[0] == 90:
            angles[0] +=1

        # calc line
        # start point
        self.line = self.car.getRect().center
        # end points
        for angle in angles:
            dx = m.cos(m.radians(angle)) * 10
            dy = m.sin(m.radians(angle)) * 10

            closestIntersection = [(), 0]
            ray = [(self.line[0], self.line[1]), (self.line[0]+dx, self.line[1]+dy)]
            for segment in self.corners:
                param = self.getIntersection(ray, segment)
                if param == 0:
                    continue
                if closestIntersection[1] == 0 or param[1] < closestIntersection[1]:
                    closestIntersection = param
            if closestIntersection[1]>0:
                self.intersections.append(closestIntersection[0])


    def getIntersection(self, ray, segment):
        '''
        Calculates intersection point between two lines.
        Every line can be represented by a Point P1(x1,y1) and the direction vector D, then
        r_p = P1(x1,y1) + D * t.
        In scalar components its,
        x = x1 + xd * t
        y = y1 + yd * t
        '''
        # ray in parametric form
        r_x = ray[0][0]
        r_y = ray[0][1]
        r_dx = ray[1][0] - ray[0][0]
        r_dy = ray[1][1] - ray[0][1]

        # segments in parametric
        s_x = segment[0][0]
        s_y = segment[0][1]
        s_dx = segment[1][0] - segment[0][0]
        s_dy = segment[1][1] - segment[0][1]

        # check for parellel (same unit vector)
        r_mag = m.sqrt(r_dx * r_dx + r_dy*r_dy)
        s_mag = m.sqrt(s_dx * s_dx + s_dy * s_dy)

        if(r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag):
            return 0

        # for checking intersection you set x1 equal x2 and y1 equal y2 and solve for t1 and t2
        a = (s_dx*r_dy - s_dy*r_dx)
        # check for divided by zero
        if a == 0 or r_dx == 0:
            return 0
        t2 = (r_dx*(s_y-r_y) + r_dy*(r_x-s_x)) / a
        t1 = (s_x+s_dx*t2-r_x) / r_dx

        # check t1>0 and 0<t2<1 or there is no intersection
        if t1 <= 0:
            return 0
        if t2 > 1 or t2 < 0:
            return 0
        #point of intersection
        return [(r_x+r_dx*t1, r_y+r_dy*t1), t1]


    def render(self, screen):
        offset = self.camera.getOffset()
        start = (self.line[0]+offset[0], self.line[1]+offset[1])
        end = [(int(x + offset[0]), int(y + offset[1])) for x, y in self.intersections]

        for line in end:
            pg.draw.line(screen, RED, start, line, 2)
            pg.draw.circle(screen, RED, line, 4)
        self.intersections = []


class Car(pg.sprite.Sprite):
    def __init__(self, manager, sprite_group, worldX, worldY):
        super().__init__()
        sprite_group.add(self)
        self._worldX = worldX
        self._worldY = worldY
        self.rotate = 0
        self.isMoving = False
        self.acc = 1.0
        self.vel = [0, 0]
        self.velVec = [0, 0]
        self.pos = [0, 0]
        self.rot_speed = 3
        self.friction = .9
        self.initImage(manager)
        self.manager = manager


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
        # self.isMoving -= keys[pg.K_s]

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