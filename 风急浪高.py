#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 20:08
# @Author  : Ryu
# @Site    : 
# @File    : 风急浪高.py
# @Software: PyCharm
import pygame as pg
import math,random
pg.init()
sc=pg.display.set_mode((1000,800))

pos=[500,600]

fps=pg.time.Clock()
wavex=0
wavey=0
v=1
boat=pg.image.load("boat.png")
boat=pg.transform.scale(boat,[100,100])
boatx=470

def disTO(pos1,pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

while True:
    keys=pg.key.get_pressed()
    if keys[pg.K_a]:
        boatx -= 3.14*2
    if keys[pg.K_d]:
        boatx += 3.14*2
    wavex+=0.1
    fps.tick(60)
    event=pg.event.poll()
    if event.type == pg.QUIT:
        pg.qiut()
        exit()
    sc.fill((255,255,255))
    wavex+=random.uniform(0.01,0.1)
    wavex+=0.01
    wavey+=v
    if wavey>=50:
        v=-1
    elif wavey<=-50:
        v=1
    for i in range(250):
        pos[0]=i*4
        for j in range(10):
            pos[1]=450+j*10+int(math.sin(i/40+wavex)*40)+wavey

            pg.draw.circle(sc,(0,55,120),pos,10)
        for j in range(10):
            pos[1] = 550 + j * 10 + int(math.sin(i / 40 + wavex) * 40) + wavey

            pg.draw.circle(sc, (20, 75, 140), pos, 10)


    sc.blit(boat,(boatx,(450+j*10+int(math.sin(i/40+(1000-wavex))*40)+wavey)))

    for i in range(250):
        pos[0]=i*4
        for j in range(10):
            pos[1]=650+j*10+int(math.sin(i/40+wavex)*40)+wavey

            pg.draw.circle(sc,(20,95,160),pos,10)
        for j in range(10):
            pos[1] = 750 + j * 10 + int(math.sin(i / 40 + wavex) * 40) + wavey

            pg.draw.circle(sc, (60, 115, 180), pos, 10)
    #pg.draw.circle(sc,(0,0,0),(500,400),200,1)
    pg.draw.line(sc,(60,115,180),(0,1050+wavey),(1000,1050+wavey),400)
    pg.display.update()
