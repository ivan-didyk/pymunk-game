import pygame
from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
import math, cmath

# P = (1−t)³P1 + 3(1−t)²tP2 +3(1−t)t²P3 + t³P4

pygame.init()
pygame.display.init()
size = (320, 320)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bezier")
run = True


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
    a = math.atan2(p1.y - p2.y, p1.x - p2.x)
    if p1.x < p2.x:
        a += 0#math.pi
    return a


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
    return r


bz = bezier(
    Vector2(150, 0),
    Vector2(0, 300),
    Vector2(300, 300),
    Vector2(150, 0),
    10
)

print(math.degrees(angle_x(Vector2(0, 0), Vector2(12, 12))))
d = 1

a = 90
l = 10

screen.fill(pygame.Color('#ffffff'))
for i in range(len(bz) - 1):
    print(math.degrees(angle_x(bz[i + 1], bz[i]) - math.radians(a) - math.pi))
    pygame.draw.lines(screen, pygame.Color('#000000'), False, [
        (bz[i].x + 10, bz[i].y + 10),
        (bz[i + 1].x + 10, bz[i + 1].y + 10)
    ], 3)
    if i % d == 0:
        p = cpoint(angle_x(bz[i + 1], bz[i]) - math.radians(a), l, bz[i])
        pygame.draw.lines(screen, pygame.Color('#ff0000'), False, [
            (bz[i].x + 10, bz[i].y + 10),
            (p.x + 10, p.y + 10)
        ], 3)

while run:
    pygame.time.delay(100)


    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False