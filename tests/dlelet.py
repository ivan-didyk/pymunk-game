import pygame  # Pygame as core

import pymunk  # Import physics engine
from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
import pymunk.pygame_util
from random import randint

a = []

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyBall")

draw_options = pymunk.pygame_util.DrawOptions(screen)
pymunk.pygame_util.positive_y_is_up = False

run = True

space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0, 3600     # Set its gravity

while run:
    pygame.time.delay(100)
    space.step(0.01)
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)

    b = pymunk.Body(1, 12)
    c = pymunk.Circle(b, 10)
    b.position = randint(0, 700), 0
    c.color = 0, 0, 0
    space.add(b, c)
    a.append([c, b])
    d = []
    for i in range(len(a)):
        if a[i][1].position.y > 500:
            d.append(i)

    d.reverse()

    for i in d:
        del a[i]

    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print(space._bodies)
        """for property, value in vars(dict(space._bodies)).iteritems():
           #print(i)
           print(property, ": ", value)
           #  space._bodies.remove(str(i[1]))
        """
        for i in space.shapes:
            space.remove(i)

pygame.quit()