#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 13:33
# @Author  : Ryu
# @Site    : 
# @File    : 安如磐石.py
# @Software: PyCharm
import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pu
from pymunk import Vec2d

sc=pg.display.set_mode((600,600))
space = pm.Space()
space.gravity = (0,900)

shape = pm.Segment(space.static_body,(0,500),(600,500),1)
shape.friction = 1
space.add(shape)
draw_options = pu.DrawOptions(sc)

def init():
    global draw_options
    shape = pm.Segment(space.static_body, (0, 500), (600, 500), 1)
    shape.friction = 1
    space.add(shape)
    draw_options = pu.DrawOptions(sc)
    from pymunk import Vec2d
    a = Vec2d(540, 490)
    b = Vec2d(0, 0)
    dX = Vec2d(10, 20)
    dY = Vec2d(20, 0)
    for i in range(25):
        b = Vec2d(*a)
        for j in range(i, 25):
            points = [(-10, -10), (-10, 10), (10, 10), (10, -10)]
            body = pm.Body(1, 2000)
            body.position = b
            shape = pm.Poly(body, points)  # 创建多边形
            shape.friction = 1
            space.add(body, shape)
            b -= dY
        a -= dX
init()
def draw():
    sc.fill("white")
    space.debug_draw(draw_options)
    pg.display.update()

def dis(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def kick():
    if pg.mouse.get_pressed()[0]:
        mpos=pg.mouse.get_pos()
        for i in range(len(space.bodies)):
            if space.bodies[i] and dis(mpos,space.bodies[i].position)<10:
                space.remove(space.shapes[i+1])
                space.remove(space.bodies[i])
                break

def reset():
    if pg.mouse.get_pressed()[2]:
        space.remove(*space.shapes)
        space.remove(*space.bodies)
        init()

score=0
def count():
    global score
    for b in space.bodies:
        if b.position[1]<18:
            score =325-len(space.bodies)


fps = pg.time.Clock()
while True:
    fps.tick(60)
    event = pg.event.poll()
    if event.type == pg.QUIT:
        pg.quit()
        exit()
    draw()
    kick()
    count()
    reset()
    space.step(1/60)
    pg.display.set_caption("score"+str(score))