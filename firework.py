import pygame
from random import randint,uniform,choice
import math
from tkinter import *
import tkinter.messagebox

#全局变量
vector = pygame.math.Vector2 #引入向量
gravity = vector(0,0.3) #重力向量
DISPLAY_WIDTH = DISPLAY_HEIGHT = 800 #屏幕宽度为800
'''
fps = 60  #设置刷新速度
switch_T = 0 #自动放烟花开关
T = 0.25 #放烟花周期
user = "1" #账号
password = "1" #密码
text1 = "新春快乐" #主要显示文字
len_text1 = 4  #文字长度
text2 = "作者"  #
bg = ""

try:
    DISPLAY_WIDTH,DISPLAY_HEIGHT = imagesize.get(bg) #屏幕高宽
except:
    tkinter.messagebox.showerror("提示","找不到系统背景文件，请确保文件不被删除或修改后重新尝试！")
gravity = vector(0,0.3*DISPLAY_HEIGHT/800) #重力向量
launch = "launch.mp3"
explode = "explode.mp3"
'''
trail_colours = [(45, 45, 45), (60, 60, 60), (75, 75, 75),
                 (125, 125, 125), (150, 150, 150)]  # 飞行路径（尾迹）颜色参数
dynamic_offset = 1  # 爆炸前产生尾迹需要的时间
static_offset =5   # 爆炸后产生尾迹需要的时间

#烟花类
class Firework:
    def __init__(self):
        # 随机颜色 颜色变量为元组
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))  # 产生一种随机颜色作为烟花爆炸前的烟花粒子颜色（升空)
        self.colours = (
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255))
        )  # 产生三种随机颜色作为颜色爆炸后的烟花粒子颜色
        self.firework = Particle(randint(0, DISPLAY_WIDTH), DISPLAY_HEIGHT, True,
                                 self.colour)  # 创造一个烟花粒子
        self.exploded = False #是否已经爆炸
        self.particles = []  #爆炸后的烟花粒子
        #self.min_particles = 100  # 爆炸烟花粒子数量区间最小值
        #self.max_particles = 255   # 爆炸烟花粒子数量区间最大值
        self.max_min_particles = vector(100,255)  # 爆炸烟花粒子数量区间最大值最小值
        '''
        self.launch_mp3 = pygame.mixer.Sound(launch)
        self.exploded_mp3 = pygame.mixer.Sound(explode)
'''
    # 更新烟花，即绘制该烟花的所有粒子，及更新烟花粒子的状态参数（如是否消失而该被移除）
    def update(self,win):
        #未爆炸情况
        if not self.exploded:
            '''
            if self.firework.life == 0:
                self.launch_mp3.play()
                '''
            self.firework.apply_force(gravity)  # 为烟花粒子添加重力
            self.firework.move()  # 移动烟花粒子位置
            # 遍历烟花粒子的全部尾迹粒子
            for tf in self.firework.trails:
                tf.show(win)  # 绘制尾迹粒子
            self.show(win)  # 绘制烟花粒子

            # 达到最高点（速度从初始方向衰减到0或指向地面）
            if self.firework.vel.y >= 0:
                self.exploded = True # 爆炸判断参数修改
                self.explode()  # 烟花爆炸
            # 爆炸后情况
        else:
            #  遍历爆炸产生的烟花粒子
            for particle in self.particles:
            # 添加一定比例的爆炸的冲击力和重力，y轴方向上力始终为指向地面方向
                particle.apply_force(vector(gravity.x + uniform(-1, 1) / 20,
                                        gravity.y / 2 + (randint(1, 8) / 100)))
                particle.move()  # 移动烟花粒子
            # 遍历烟花粒子的尾迹粒子
                for t in particle.trails:
                    t.show(win)  # 绘制尾迹粒子
                particle.show(win)  # 绘制烟花粒子


        # 烟花爆炸，生成爆炸的烟花粒子
    def explode(self):
        amount = randint(self.max_min_particles.x, self.max_min_particles.y) # 产生区间范围内的爆炸烟花粒子数
        #self.explode_mp3.play()
        # 遍历烟花粒子数
        for i in range(amount):
            self.particles.append(
                Particle(self.firework.pos.x,self.firework.pos.y,False, self.colours))  # 添加爆炸烟花粒子))

    # 绘制升空期的烟花粒子
    def show(self,win):
    # 绘制烟花粒子（圆）
        pygame.draw.circle(win,self.colour,(int(self.firework.pos.x),int(self.firework.pos.y)),self.firework.size)
# 移除该烟花爆炸后所以消失需移除的烟花粒子（其尾迹粒子跟着移除），再返回该烟花是否已经完全放完需要移除（即所以爆炸烟花粒子已经消失移除）
    def remove(self):
        # 是否爆炸（因为仅用于爆炸烟花粒子）
        if self.exploded:
            # 遍历爆炸烟花粒子
            for p in self.particles:
            # 判断烟花粒子是否已经消失需移除
                if p.remove is True:
                    self.particles.remove(p)
                    # 从烟花粒子列表中移除已经消失了的烟花粒子

            if len(self.particles) == 0:
                return True
            else:
                return False


#烟花粒子类
class Particle:
    def __init__(self,x,y,firework,colour):
        self.firework = firework  # 是否为烟花阶段（未爆炸阶段）
        self.pos = vector(x,y)  # 当前位置坐标
        self.origin = vector(x,y) # 初始位置坐标（仅用于作为爆炸粒子的烟花粒子）
        self.radius = 20  #半径
        self.remove = False  # 该粒子是否需移除（仅用于作为爆炸粒子的烟花粒子）
        self.explosion_radius = randint(5,18) * 5 #爆炸半径（仅用于作为爆炸粒子的烟花粒子）
        self.life = 0  # 存活时间（仅用于作为爆炸粒子的烟花粒子）
        self.acc = vector(0, 0)  # 由于受力产生的加速度
        # 跟踪变量
        self.trails = []  # 储存粒子尾迹物体
        # 上十帧烟花粒子坐标，用作尾迹粒子坐标，（-10，-10）表示画在屏幕外，即尾迹未产生
        self.prev_posx = [-10] * 10  # 存储最后10个位置
        self.prev_posy = [-10] * 10  # 存储最后10个位置

        # 设置升空期烟花粒子参数
        if self.firework:
            self.vel = vector(0,-randint(17,20))# 升空速度，y上17-20
            self.size = 5  # 烟花粒子大小（半径）
            self.colour = colour  # 烟花粒子颜色
            for i in range(5):
                self.trails.append(Trail(i,self.size,True))# 创建尾迹粒子类的五个尾迹粒子
        # 设置爆炸产生的烟花粒子参数
        else:
            self.vel = vector(uniform(-1,1),uniform(-1,1)) # 爆炸速度添加基础系数（大小[-1,1]），符号表示爆炸方向，大小为权值系数
            # 速度越小的概率越大，所以靠近烟花中心的爆炸粒子会更加多而密集
            self.vel.x *= randint(7, self.explosion_radius + 2)  # 为x上速度系数乘上速度值（最小值很为7，最大值在7到18低概率随机）
            self.vel.y *= randint(7, self.explosion_radius + 2)  # 为y上速度系数乘上速度值（最小值很为7，最大值在7到18低概率随机）
            self.size = randint(2, 4)  # 爆炸粒子大小[2,4]，故其尾迹为[0,2]
            self.colour = choice(colour)  # 在三种爆炸颜色中选择一种（爆炸前为1种颜色，爆炸产生共3种颜色的爆炸粒子）
            # 存入尾迹粒子
            for i in range(5):
                self.trails.append(Trail(i, self.size, False))  # 创建尾迹粒子类的五个尾迹粒子

    # 加速度设置
    def apply_force(self, force):
        self.acc += force

        # 绘制烟花粒子（仅用于作为爆炸粒子的烟花粒子，升空期的烟花粒子绘制在firework类中定义）

    def show(self, win):
        pygame.draw.circle(win, (self.colour[0], self.colour[1], self.colour[2], 0),
                           (int(self.pos.x), int(self.pos.y)), self.size)
        # 绘制烟花粒子（圆）参数：win窗口，color颜色透明的0，坐标pos，半径size，边框不设置默认0即无

    def move(self):
        # 没爆炸一直上升
        if not self.firework:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc  # 速度加上加速度
        self.pos += self.vel  # 位置加上速度
        self.acc *= 0

        if self.life == 0 and not self.firework:  # 检查颗粒是否在爆炸半径之外
            distance = math.sqrt(
                (self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()
        self.trail_update()
        self.life += 1

    # 判断烟花粒子是否衰退而消失需要移除，只是修改是否需要移除的参数，不会移除烟花粒子（仅用于作为爆炸粒子的烟花粒子）
    def decay(self):
        if 50 > self.life > 10:  # 存活时间在（10，50）时1/30概率衰减消散
            ran = randint(0, 30)  # 随机数
            if ran == 0:  # 判断是否命中消失的1/30
                self.remove = True  # 消失移除参数修改
        elif self.life > 50:  # 存活时间大于50时
            ran = randint(0, 5)  # 随机数1/5概率消失
            if ran == 0:  # 判断是否命中消失的1/5
                self.remove = True  # 消失移除参数修改

    # 更新尾迹粒子数据
    def trail_update(self):
        self.prev_posx.pop()  # 移除最久远前的x坐标位置记录
        self.prev_posx.insert(0, int(self.pos.x))  # 添加单位时间（一帧）前的x坐标位置在最前
        self.prev_posy.pop()  # 移除最久远前的y坐标位置记录
        self.prev_posy.insert(0, int(self.pos.y))  # 添加单位时间（一帧）前的y坐标位置在最前

        for n, t in enumerate(self.trails):
            if t.dynamic:
                t.get_pos(self.prev_posx[n + dynamic_offset], self.prev_posy[n + dynamic_offset])
            else:
                t.get_pos(self.prev_posx[n + static_offset], self.prev_posy[n + static_offset])


'''
        # 很奇怪，这句没用，前面life==0使得只判断一次distance是0的情况，所以爆炸不会因为超过半径消失，半径提供速度，因为时间消失
        if self.life == 0 and not self.firework:  # check if particle is outside explosion radius
            distance = math.sqrt((self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()

        self.trail_update()

        self.life += 1
'''


# 尾迹粒子（升空烟花粒子，和爆炸粒子的尾迹颜色与大小不同，5个尾迹粒子，升空尾迹大小逐渐变小，爆炸的大小相同）
class Trail:
    def __init__(self,n,size,dynamic):
        self.pos_in_line = n
        self.pos = vector(-10,-10)
        self.dynamic = dynamic

        if self.dynamic:
            self.colour = trail_colours[n]
            self.size = int(size - n / 2)
        else:
            self.colour = (255,255,200)
            self.size = size - 2
            if self.size < 0:
                self.size = 0

    def get_pos(self,x,y):
        self.pos = vector(x,y)

    def show(self,win):
        pygame.draw.circle(win, (self.colour[0], self.colour[1], self.colour[2], 0),
                           (int(self.pos.x), int(self.pos.y)), self.size)

# 更新所有烟花（绘制所以烟花，移除已经放完的烟花），更新屏幕
def update(win,fireworks):
    for fw in fireworks:
        fw.update(win)######################?????????# 更新并绘制烟花
        if fw.remove():
            fireworks.remove(fw)

    pygame.display.update()

def main():
    pygame.init()
    pygame.display.set_caption("Fireworks in Pygame")
    win = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_WIDTH))
    clock = pygame.time.Clock()

    fireworks = [Firework() for i in range(2)]   #创建第一个烟花
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN: #用数字键改变游戏速度
                if event.key == pygame.K_1:
                    fireworks.append(Firework())
                if event.key == pygame.K_2:
                    for i in range(10):
                        fireworks.append(Firework())
        win.fill((20,20,30))

        if randint(0,20) == 1: #创建新烟花
            fireworks.append(Firework())

        update(win,fireworks)

    pygame.quit()
    quit()

main()































