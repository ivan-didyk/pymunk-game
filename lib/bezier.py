from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
import math
import pymunk
import pygame


def round_d(n: float, s : int):
    return round(n * math.pow(10, s)) / math.pow(10, s)


def hypotenuse(s1: float, s2: float):
    """
    Function, what calcs hypotenuse of triangle, using it's catheuses
      ___________
    \/ s1² + s2²

    :param s1: First catheus of triangle
    :param s2: Second catheus of triangle
    :return: Size of hypotenuse of triangle
    """
    from math import sqrt
    return sqrt(s1 ** 2 + s2 ** 2)


def angle_x(p1: Vector2, p2: Vector2):
    return math.atan2(p1.y - p2.y, p1.x - p2.x)


def cpoint(a: float, d: float, s: Vector2):
    return Vector2(
        s.x + round_d(math.cos(a) * d, 3),
        s.y + round_d(math.sin(a), 3) * d
    )


def bezier(a: Vector2, b: Vector2, c: Vector2, d: Vector2, j: int):
    r = []
    for i in range(j):
        t = 1 / j * i
        r.append(Vector2(
            #(1-t)**3*a.x + 3 * (1 - t)**2*t*b.x + 3 * (1 - t)**2*t*c.x + t**3*d.x,
            pow(1 - t, 3) * a.x +
            3 * pow(1 - t, 2) * t * b.x +
            3 * (1 - t) * pow(t, 2) * c.x +
            pow(t, 3) * d.x,
            #(1 - t) ** 3 * a.y + 3 * (1 - t) ** 2 * t * b.y + (3 * (1 - t) * t) ** 2 * c.y + t ** 3 * d.y,
            pow(1 - t, 3) * a.y +
            3 * pow(1 - t, 2) * t * b.y +
            3 * (1 - t) * pow(t, 2) * c.y +
            pow(t, 3) * d.y
        ))
    r.append(d)
    return r


class BezierCollider:
    lines = []
    points = []
    color = '#ffffff'
    width: float = 1
    d: int = 3

    def __init__(self, body: pymunk.body, bz, w: float = 1, d: int = 3):
        #print(bz)
        self.lines = []
        for i in range(len(bz) - 1):
            s = pymunk.Segment(body, bz[i], bz[i + 1], w / 2)
            s.friction = 1.5
            self.lines.append(s)
        self.points = bz
        self.width = w
        self.d = d

    def add(self, space):
        for i in self.lines:
            try:
                space.add(i)
            except:
                pass
                #print('EE<')

    def __call__(self, screen: pygame.display, m: Vector2, *args, **kwargs):
        for i in range(len(self.points) - 1):

            pygame.draw.lines(screen, pygame.Color('#000000'), False, [
                (self.points[i].x + m.x, self.points[i].y + m.y),
                (self.points[i + 1].x + m.x, self.points[i + 1].y + m.y)
            ], int(self.width))

            if i % self.d == 0:
                a = 30
                l = 10
                p = cpoint(angle_x(self.points[i + 1], self.points[i]) - math.radians(a) - math.pi, l, self.points[i])
                pygame.draw.lines(screen, pygame.Color('#000000'), False, [
                    (self.points[i].x + m.x, self.points[i].y + m.y),
                    (p.x + m.x, p.y + m.y)
                ], self.width)