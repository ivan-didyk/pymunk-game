import pygame
from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
import pymunk

class Portal:
    pos: Vector2
    colid: int
    body: pymunk.Body
    sensor: pymunk.Circle

    def __init__(self, pos, cid):
        self.pos = pos
        self.colid = cid
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.sensor = pymunk.Circle(self.body, 10)
        self.sensor.sensor = True
        self.sensor.collision_type = cid

    def add(self, space):
        space.add(self.body, self.sensor)

    def __call__(self, screen, m, color=pygame.Color('#000000'), *args, **kwargs):
        pygame.draw.circle(screen, color, Vector2(int(self.pos.x + m.x), int(self.pos.y + m.y)), 20, 3)