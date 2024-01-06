import pygame as pg
import pymunk
pg.init()
sc=pg.display.set_mode((800,500))
space = pymunk.Space()#创建空间
space.gravity = (0,0)#重力分x和y
gray=(123,125,125)
stage=(51,51,51)
white=(236,240,241)

def draw():
    sc.fill(white)
    pg.draw.line(sc,gray,(20,200),(680,200),360)
    pg.draw.line(sc,stage,(40,200),(660,200),320)
fps=pg.time.Clock()
while True:
    fps.tick(60)
    event=pg.event.poll()
    if event.type == pg.QUIT:
        pg.quit()
        exit()
    draw()
    pg.display.update()
