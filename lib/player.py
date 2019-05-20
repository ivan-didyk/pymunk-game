import pymunk
import pygame
from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
from math import degrees

def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

class Ball:
    body: pymunk.body
    collider: pymunk.Circle
    space: pymunk.space
    img: pygame.image
    imagerect = None

    def __init__(self, x: int, y: int, radius: int, space: pymunk.space, img, collid):
        wheel_color = 52, 219, 119
        mass = 100
        moment = pymunk.moment_for_circle(mass, 0, radius)
        wheel1_b = pymunk.Body(mass, moment)
        wheel1_s = pymunk.Circle(wheel1_b, radius)
        wheel1_s.friction = 10
        wheel1_s.color = wheel_color
        wheel1_b.position = Vector2(x, y)
        wheel1_s.collision_type = collid
        space.add(wheel1_b, wheel1_s)
        self.body = wheel1_b
        self.collider = wheel1_s
        self.space = space
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (20, 20))
        self.imagerect = self.img.get_rect()

    def draw(self, screen, pos):
        w, h = self.img.get_size()
        blitRotate(screen, self.img, pos, (w/2, h/2), -degrees(self.body.angle))
