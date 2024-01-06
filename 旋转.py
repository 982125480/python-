#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 13:15
# @Author  : Ryu
# @Site    : 
# @File    : 旋转.py
# @Software: PyCharm
import pygame as pg
pg.init()

sc = pg.display.set_mode((900, 800))
clock = pg.time.Clock()
sc.fill((255,255,255))
a=0
b=1
while True:
    clock.tick(60)
    event = pg.event.poll()
    if event.type == pg.QUIT:
        pg.quit()
        exit()

    a+=b
    if a>90:
        b=-1
    if a<-90:
        b=1



    cannon=pg.image.load("cannon.png")
    cannon=pg.transform.scale(cannon,(100,100))
    cannon=pg.transform.rotate(cannon,a)
    cannon_rect=cannon.get_rect()
    cannon_rect.center = (350,625)
    sc.blit(cannon,cannon_rect)
    pg.display.update()
    sc.fill((255, 255, 255))
    print(a,b)