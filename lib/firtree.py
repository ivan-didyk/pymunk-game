import pygame
from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)

class Firtree:
    frame: int
    dir: bool = False
    levels: int
    levelIncrease: int = 5
    pos: Vector2
    height: int
    spacing: int
    levelSize: int
    move: int

    def __init__(self, pos: Vector2, levels: int = 4, height: int = 70, spacing: int = 10, increase: int = 3, levelSize: int = 10, move: int = 10, frame: int=0):
        self.pos = pos
        self.levelIncrease = increase
        self.levels = levels
        self.height = height
        self.spacing = spacing
        self.levelSize = levelSize
        self.move = move
        self.frame = frame

    def update(self, s):
        if self.dir:
            self.frame += s
            if self.frame >= self.move:
                self.dir = False
        else:
            self.frame -= s
            if self.frame <= -self.move:
                self.dir = True

    def draw(self, screen, color, m : Vector2):
        p = Vector2(0, self.height)
        p.rotate_degrees(self.frame + 180)
        p += self.pos + m
        pygame.draw.line(screen, color, self.pos + m, p, 3)
        for i in range(self.levels):
            for j in -1, 1:
                epos = Vector2((self.levelSize + self.levelIncrease * i) * j, self.height - i * self.spacing - self.levelIncrease * i * 0.5 - self.levelSize)
                epos.rotate_degrees(self.frame + 180)
                epos += self.pos + m
                spos = Vector2(0, self.height - i * self.spacing)
                spos.rotate_degrees(self.frame + 180)
                spos += self.pos + m
                pygame.draw.line(screen, color, spos, epos, 3)