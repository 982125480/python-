import pygame as pg
import random
import math

import pygame.draw

pg.init()
sc=pg.display.set_mode((700,700))
sc.fill((0,0,0))

class Food():
    def __init__(self):
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.r=5
        self.x=random.randint(0,700)
        self.y=random.randint(0,700)
foods=[]
for i in range(100):
    foods.append(Food())

class Ball():
    def __init__(self):
        self.color=(0,255,0)
        self.x=350
        self.y=350
        self.r=15
#me=Ball()

us=[]
for i in range(3):
    us.append(Ball())

def draw():
    sc.fill((0,0,0))
    for i in foods:
        pygame.draw.circle(sc,i.color,(i.x,i.y),i.r,0)
    #pg.draw.circle(sc,me.color,(me.x,me.y),me.r,0)
    for i in us:
        pg.draw.circle(sc, i.color, (i.x, i.y), i.r, 0)
    pg.display.update()

lastker=4
def control():
    global lastker
    keys = pg.key.get_pressed()
    speed=1
    if (keys[pg.K_w] == 1 and lastker!=2) or lastker==1:
        #me.y-=speed
        us[0].y-=speed
        lastker = 1
    if (keys[pg.K_s] == 1 and lastker!=1)or lastker==2:
        #me.y += speed
        us[0].y += speed
        lastker =2
    if (keys[pg.K_a] == 1 and lastker!=4)or lastker==3:
        #me.x -= speed
        us[0].x -= speed
        lastker =3
    if (keys[pg.K_d]==1 and lastker!=3)or lastker==4:
        #me.x += speed
        us[0].x += speed
        lastker = 4

    for i in range(len(us)-1):
        if disTo(us[i].x,us[i].y,us[i+1].x,us[i+1].y)>20:
            us[i+1].x = int((us[i].x+us[i+1].x*3)/4)
            us[i + 1].y = int((us[i].y + us[i + 1].y*3) / 4)

def disTo(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def istouching(x1,y1,x2,y2,dis):
    if disTo(x1,y1,x2,y2) <= dis:
        return True

def eat():
    for i in range(len(foods)):
        #if istouching(me.x,me.y,foods[i].x,foods[i].y,me.r):
        #    me.r+=1
        if istouching(us[0].x,us[0].y,foods[i].x,foods[i].y,us[0].r):
            new=Ball()
            new.x=us[len(us)-1].x
            new.y=us[len(us)-1].y
            if len(us)<25:
                new.color=(255-len(us)*10,0,0)
            else:
                new.color = (0,0,0)
            us.append(new)
            foods.pop(i)
            break

def more():
    if pg.time.get_ticks()%10000<10:#pg.time.get_ticks是返回pg.init后个，经过了多少毫秒除以1000是过去了多少秒，再除以10是过去10秒钟
        for i in range(30):
            foods.append(Food())

clock =pg.time.Clock()
while True:
    clock.tick(60)
    event =pygame.event.poll()
    if event.type == pg.QUIT:
        pg.quit()
        exit()
    control()
    more()
    eat()
    draw()