# ========================= IMPORTS ========================= #

import pygame  # Pygame as core

import pymunk  # Import physics engine

from pymunk.vec2d import Vec2d as Vector2  # I like more this syntax (Sometime, I worked in Unity)
import pymunk.pygame_util

from json import loads  # Needed for computing level maps
import warnings  # For @deprecated
import functools  # For @deprecated
import random

import lib.bezier as bezier
from lib.firtree import Firtree
from lib.coin import Coin
from lib.xjson import readcom
from lib.player import Ball
from lib.portal import Portal

# ========================= SETTINGS ========================= #

config = loads(readcom('config.json'))
level = loads(readcom('levels/' + config['startLevel'] + '/level.json'))

# ========================= VARIABLES ========================= #

space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0, 3600     # Set its gravity

r = 0

state = 'play'


# ========================= COLLISION CALLBACKS ========================= #


def coin(arbiter: pymunk.Arbiter, space, data):
    for i in arbiter.shapes:
        if type(i) == pymunk.shapes.Poly:
            i.body.collected = True
    return False


c = space.add_collision_handler(config['collid']['body'], config['collid']['coin'])
c.begin = coin

def portalc(arbiter: pymunk.Arbiter, sp, data):
    global state
    state = 'redir'
    return False


c2 = space.add_collision_handler(config['collid']['portal'], config['collid']['body'])
c2.begin = portalc

# ========================= HELPERS ========================= #


def space_c():
    global lines, trees, coins, portal, car

    for i in space.shapes:
        space.remove(i)

    print('+++++++>', space.shapes, space.bodies)

    lines = []
    trees = []
    coins = []


def etype(o):
    return str(type(o)).split('\'')[1]


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return y


# ========================= LEVEL VARS ========================= #

lines = []
trees = []
coins = []
portal = ''
car = ''

cam = Vector2(level['ball']['x'], level['ball']['y'])

ls = True

# ========================= LEVEL  ========================= #
def load():
    global car, lines, trees, coins, portal
    lines = []
    trees = []
    coins = []
    # ----- Player ----- #
    car = Ball(level['ball']['x'], level['ball']['y'], 10, space, 'img/player.png', config['collid']['body'])
    car.body.angular_velocity = 0
    # ----- Ground ----- #
    for l in level['lines']:
        i = []
        for j in l:
            i.append(Vector2(j[0], j[1]))

        l = bezier.bezier(i[0], i[1], i[2], i[3], 100)

        line = pymunk.Body(0, 0, body_type=pymunk.Body.STATIC)
        space.add(line)

        line.position = (0, 0)
        lineb = bezier.BezierCollider(line, l, 3)
        lineb.add(space)

        lines.append(lineb)

    # ----- Trees ----- #
    for i in level['trees']:
        trees.append(Firtree(Vector2(i[0], i[1]), increase=1, move=5, frame=i[2]))

    # ----- Coins ----- #
    for i in level['coins']:
        c = Coin(Vector2(i[0], i[1]), config['collid']['coin'], frame=random.randint(-5, 5))
        c.add(space)
        coins.append(c)

    # ----- Portal ----- #

    portal = Portal(Vector2(level["portal"]["pos"][0], level["portal"]["pos"][1]), config['collid']['portal'])
    portal.add(space)

load()

# ========================= START RENDER  ========================= #

pygame.init()
pygame.display.init()
pygame.font.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyBall")

scr = pygame.Surface((700, 500))
draw_options = pymunk.pygame_util.DrawOptions(scr)
pymunk.pygame_util.positive_y_is_up = False

run = True
font = pygame.font.SysFont('Arial', 30)


# ========================= GAME LOOP  ========================= #

while run:
    if state == 'play':
        pygame.time.delay(10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            r -= config['player']['acc']
        elif keys[pygame.K_RIGHT]:
            r += config['player']['acc']

        if r > 0:
            r -= config['player']['decc']
        elif r < 0:
            r += config['player']['decc']

        if keys[pygame.K_SPACE]:
            print(space._bodies)
            """for property, value in vars(dict(space._bodies)).iteritems():
               #print(i)
               print(property, ": ", value)
               #  space._bodies.remove(str(i[1]))
            """
            for i in space.shapes:
                space.remove(i)

        r = max(-config['player']['max'], min(config['player']['max'], r))

        car.body.angular_velocity += r
        space.reindex_shapes_for_body(car.body)

        space.step(0.001)
        screen.fill((255, 255, 255))
        for tree in trees:
            tree.update(0.1)
            tree.draw(screen, pygame.Color('#7c7c7c'), cam)

        #pygame.draw.circle(screen, pygame.Color('#000000'), (int(cam.x + car.body.position.x), int(cam.y + flipy(car.body.position.y))), 10)

        scr.fill((255, 255, 255))
        #space.debug_draw(draw_options)
        screen.blit(scr, cam)

        for i in lines:
            i(screen, cam)

        for i in coins:
            i.update(0.1)
            i(screen, pygame.Color('#000000'), cam)

        for i in level['text']:
            screen.blit(font.render(i[0], False, pygame.Color('#000000')), cam + (i[1], i[2]))


        cam = car.body.position * -1 + Vector2(size[0] / 2, size[1] / 2)

        portal(screen, cam, pygame.Color('#555555'))
        car.draw(screen, (350, 250))
        #for i in lines:
        #    i.draw(Vector2(0, 300), screen, pygame.Color('#374d5f'))


        #pygame.display.update()
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
    elif state == 'redir':
        print('[ INFO ]   Redirecting to', level['portal']['target'])
        #space_c()
        #input()
        space.add()
        for i in space.shapes + space.bodies:
            space.remove(i)
        space.step(0.001)
        space.reindex_static()
        level = loads(readcom('levels/' + level['portal']['target'] + '/level.json'))
        ls = False
        load()

        state = 'play'
    elif state == 'mmenu':



pygame.quit()