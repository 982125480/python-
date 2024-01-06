#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 14:45
# @Author  : Ryu
# @Site    : 
# @File    : 举重若轻.py
# @Software: PyCharm
import pygame as pg
import math
import time
pg.init()
sc=pg.display.set_mode((900,800))
clock=pg.time.Clock()

power=0
part=1
a=1
direction = 0
b=1

class Ball():
    def __init__(self):
        self.pos=[50,625]
        self.color=[15,15,15]
        self.speedx=1
        self.speedy=-1
        self.size = [10,10]
ball=Ball()


while True:
    clock.tick(30)
    event = pg.event.poll()
    if event.type == pg.QUIT:
        pg.quit()
        exit()
    if part==1:
        power+=a
        if power>=10:
            a=-1
        if power <=0:
            a=1
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_presses = pg.mouse.get_pressed()
            if mouse_presses[0]:
                a=0
                pg.time.wait(300)
                part=2
                b=1
                continue


    sc.fill((255,255,255))
    pg.draw.line(sc,(0,0,0),(0,705),(900,705),1)
    pg.draw.line(sc,(0,0,0),(50,10),(50,110),20)
    pg.draw.line(sc, (200, 0, 0), (50, 110 - power * 10), (50, 110), 20)
    if part ==2:
        direction += b
        if direction >0:
            b = -1
        if direction <-90:
            b = 1
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_presses = pg.mouse.get_pressed()
            if mouse_presses[0]:
                b = 0
                part = 3
                pg.time.wait(300)
                continue

    cannon = pg.image.load("cannon.png")
    cannon = pg.transform.scale(cannon, (100, 100))
    cannon = pg.transform.rotate(cannon, direction)
    cannon_rect=cannon.get_rect()
    cannon_rect.center = (50,625)
    sc.blit(cannon, cannon_rect)

    if part == 3:
        if pg.mouse.get_pressed()[0]:
            ball=Ball()
            ball.speedy = power * math.cos(2 * math.pi / (360 / direction))*(-1)
            ball.speedx = power * math.sin(2 * math.pi / (360 / direction))*(-1)
            part=4
            continue

    if part ==4:
        ball.pos[0]+=int(ball.speedx)*2
        ball.pos[1]+=int(ball.speedy)*2
        ball.speedy+=0.09
        pg.draw.circle(sc,ball.color,ball.pos,10,0)
        if ball.pos[1]>720:
            ball.pos[1]=700
            part = 5
            continue

    if part == 5:
        if ball.size[0] == 10:
            pg.mixer.music.load("boom.mp3")
            pg.mixer.music.play()
        if ball.size[0]<120:
            boom = pg.image.load("boom.png")
            boom = pg.transform.scale(boom, ball.size)
            sc.blit(boom, (ball.pos[0] - int(ball.size[0] / 2), ball.pos[1] - int(ball.size[1] / 2)))
            ball.size[0] += 10
            ball.size[1] += 10
        else:
            part=1
            power=0
            a=1
    pg.display.update()
    print(part,direction,power,ball.speedx,ball.speedy)