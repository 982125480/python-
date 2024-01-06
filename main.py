import pygame,pyzrun
width=800
height=600
screen=pygame.display.set_mode((800,600))
x=width/2
y=height/2
speed_x= 3
speed_y = 5
r= 30
def draw():
    screen.fill((0,0,0))
    pygame.draw.circle(screen,(0,0,0),(100,100),100,2)

def update():
    global x,y,speed_x,speed_y
    x=x+speed_x
    y=y+speed_y
    if x>width - r or x <=r:
        speed_x = -speed_x
    if y>=height -r or y <=r:
        speed_y = -speed_y
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
pgzrun.go()