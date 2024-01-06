#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/27 14:15
# @Author  : Ryu
# @Site    : 
# @File    : 激光迷宫.py
# @Software: PyCharm
import pygame as pg
import random
import math
sc= pg.display.set_mode((700,700))
sc.fill((0,0,0))
pg.display.update()
colors=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

class Ms():
    d=0
    def __init__(self):
        mpos = pg.mouse.get_pos()
        self.x=(mpos[0]-50)//100*100
        self.y=(mpos[1]-50)//100*100
        self.pos1=[[self.x,self.y],[self.x+100,self.y]]
        self.pos2=[[self.x+100,self.y+100],[self.x,self.y+100]]
ms=[Ms()]

red=(255,0,0)
pos=[50,0]
speed=[0,1]
start=0

def distanceTo(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def isIn(pos1,pos2,pos3):
    a=distanceTo(pos1[0],pos1[1],pos2[0],pos2[1])
    b=distanceTo(pos1[0],pos1[1],pos3[0],pos3[1])
    c=distanceTo(pos2[0],pos2[1],pos3[0],pos3[1])
    if a==b and c ==a+b:
        return True
    else:
        return False

while True:
    event=pg.event.poll()
    if event.type ==pg.QUIT:
        pg.quit()
        exit()

    keys=pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        start=1
        sc.fill((0,0,0))
        for i in range(len(ms)-1):
            pg.draw.line(sc,colors,ms[i].pos1[ms[1].d],ms[i].pos2[ms[i].d],10)

    if start:
        pg.draw.circle(sc,red,pos,5)
        pos[0]+=speed[0]
        pos[1]+=speed[1]
        for i in range(len(ms)-1):
            pos1=ms[i].pos1[ms[i].d]
            pos2=ms[i].pos2[ms[i].d]
            if isIn(pos,pos1,pos2):
                if pos1[0]<pos2[0]:
                    speed[0],speed[1]=speed[1],speed[0]
                else:
                    speed[0],speed[1]=0-speed[1],0-speed[0]

    else:
        mpos=pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            ms.append(Ms())
            pg.time.wait(300)

        ms[len(ms)-1].__init__()
        if pg.mouse.get_pressed()[2]:
            ms[len(ms)-1].d+=1
            ms[len(ms)-1].d%=2
            pg.time.wait(300)

        sc.fill((0, 0, 0))
        for i in range(len(ms)):
            pg.draw.line(sc, colors, ms[i].pos1[ms[i].d], ms[i].pos2[ms[i].d], 10)

        #pg.draw.circle(sc,(0,0,0),mpos,10)
    #if pg.mouse.get_pressed()[1]:
    #    colors=(random.randint(0,255),random.randint(0,255),random.randint(0,255))


    pg.display.update()