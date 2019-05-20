import pygame
from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
import math
import pymunk


def round_d(n: float, s : int):
    return round(n * math.pow(10, s)) / math.pow(10, s)


def cpoint(a: float, d: float, s: Vector2):
    return Vector2(
        s.x + round_d(math.cos(a) * d, 3),
        s.y + round_d(math.sin(a), 3) * d
    )


class Coin:
    pos: Vector2
    move = 5
    dir = False
    frame = 0
    poly: pymunk.Poly
    body: pymunk.Body
    state = 'active'

    def __init__(self, pos, collid, frame=0):
        self.pos = pos
        self.frame = frame
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.body.collected = False
        p = []
        for i in range(6):
            p.append(cpoint(math.radians(i * 60 + 180), 5, Vector2.zero()))
        self.poly = pymunk.Poly(self.body, p)
        self.poly.sensor = True
        self.poly.collision_type = collid

    def update(self, s):
        if self.state == 'active':
            if self.dir:
                self.frame += s
                if self.frame >= self.move:
                    self.dir = False
            else:
                self.frame -= s
                if self.frame <= -self.move:
                    self.dir = True
            self.body.position.x = self.pos + (0, self.frame)
            if self.body.collected:
                self.state = 'collect'
                self.frame = 0
        elif self.state == 'collect':
            self.frame -= s
            if self.frame < -5:
                self.state = 'inactive'


    def add(self, space):
        space.add(self.body, self.poly)

    def __call__(self, screen: pygame.display, color: pygame.Color, m, *args, **kwargs):
        if self.state != 'inactive':
            p = []
            for i in range(6):
                p.append(cpoint(math.radians(i * 60 + 90), 5, self.pos + m + (0, self.frame)))
            if self.state == 'active':
                pygame.draw.polygon(screen, color, p, 3)
            else:
                pygame.draw.polygon(screen, [255 / 5 * -self.frame for i in range(3)], p, 3)