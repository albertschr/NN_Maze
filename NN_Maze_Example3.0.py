#-*- coding:utf-8 -*-

mazeA=[ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]



#导入pygame库
import pygame
from pygame.locals import *


#from random import *

pygame.init()
#初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((640, 480), 0, 32)
#创建了一个窗口
pygame.display.set_caption("NN_Maze")
#设置窗口标题
#填充屏幕
screen.fill((255, 255, 255))

#迷宫起始点
begin_pos=[240,220]

#设置物件颜色
#墙体：黑色
rc_wall =[0,0,0]
#通道：白色
rc_space=[255,255,255]
#目标位置为绿色
rc_apple=[0,255,0]
#机器人为红色
rc_hero=[255,0,0]

#设置机器人朝向，初始值为right
face_fact="right"

#方格大小
rs = [10,10]

from Network2 import *
#初始化神经网络对象！
the_network=Network()


#draw_screen
def screen_draw():
    global hero_pos
    rp = [begin_pos[0], begin_pos[1]]

    row_num=0
    rp[1]=begin_pos[1]
    for i in mazeA:
        rp[0] = begin_pos[0]
        col_num = 0
        for j in i:


            if j == 1:
                pygame.draw.rect(screen, rc_wall, Rect(rp, rs))
            elif j == 0:
                pygame.draw.rect(screen, rc_space, Rect(rp, rs))
            elif j == 2:
                pygame.draw.rect(screen, rc_apple, Rect(rp, rs))
            elif j == 3:
                pygame.draw.rect(screen,rc_hero,Rect(rp,rs))
                hero_pos=[row_num,col_num]
            rp[0] += 10
            col_num += 1
        rp[1] += 10
        row_num += 1

screen_draw()
pygame.display.update()

#=======以下为机器人神经网络外的各个部分==========
'''
#sensorA：通过check判断物件
def check_wall():
    if mazeA[hero_pos[0]][hero_pos[1] + 1]==0:
        return 1
    else:
        return 0
'''

#⬇️sensorA升级->变成what_sensor和camera_sensor的组合
#========================
# sensorWhat：传感器更新 -> 根据三种物件输出不同的电位
def what_sensor(thing):
    if thing == 0:
        return 1
    elif thing==1:
        return 0.5
    elif thing==2:
        return 0

# sensorCamera：判断正前方的物品
def camera_sensor():
    global face_fact
    if face_fact=="right":
        return mazeA[hero_pos[0]][hero_pos[1] + 1]
    elif face_fact=="left":
        return mazeA[hero_pos[0]][hero_pos[1] - 1]
    elif face_fact=="up":
        return mazeA[hero_pos[0]-1][hero_pos[1]]
    elif face_fact=="down":
        return mazeA[hero_pos[0]+1][hero_pos[1]]

#=========================

'''
#神经网络判断的结果传导到move函数上，让其决定是否移动。
def move(result):
    if result==1:
        mazeA[hero_pos[0]][hero_pos[1]], \
        mazeA[hero_pos[0]][hero_pos[1] + 1] = mazeA[hero_pos[0]][hero_pos[1] + 1], \
                                              mazeA[hero_pos[0]][hero_pos[1]]

        # print mazeA[hero_pos[0]][hero_pos[1] + 1]
        print mazeA
        return mazeA[hero_pos[0]][hero_pos[1]]
'''

#⬇️move函数升级为包括「左转」和「前进」两种结果的action函数
def action(result):
    #result结构->[move,turn_left]
    global face_fact
    if result[0] == 1:
        #按照朝向向前移动一格
        move_to = eval(face_fact)()
        print mazeA
        return move_to
        #左转
    elif result[1]==1:
        turn_left()

#左转函数
def turn_left():
    global face_fact
    if face_fact == "right":
        face_fact = "up"
    elif face_fact == "up":
        face_fact = "left"
    elif face_fact == "left":
        face_fact = "down"
    elif face_fact == "down":
        face_fact = "right"

#上下左右移动函数
def left():
    mazeA[hero_pos[0]][hero_pos[1]], \
    mazeA[hero_pos[0]][hero_pos[1] - 1] = mazeA[hero_pos[0]][hero_pos[1] - 1], \
                                          mazeA[hero_pos[0]][hero_pos[1]]

    return mazeA[hero_pos[0]][hero_pos[1]]
def right():

    mazeA[hero_pos[0]][hero_pos[1]], \
    mazeA[hero_pos[0]][hero_pos[1] + 1] = mazeA[hero_pos[0]][hero_pos[1] + 1], \
                                          mazeA[hero_pos[0]][hero_pos[1]]

    #print mazeA[hero_pos[0]][hero_pos[1] + 1]
    return mazeA[hero_pos[0]][hero_pos[1]]

def up():
    mazeA[hero_pos[0]][hero_pos[1]], \
    mazeA[hero_pos[0]-1][hero_pos[1]] = mazeA[hero_pos[0]-1][hero_pos[1]], \
                                          mazeA[hero_pos[0]][hero_pos[1]]
    return mazeA[hero_pos[0]][hero_pos[1]]
def down():
    mazeA[hero_pos[0]][hero_pos[1]], \
    mazeA[hero_pos[0]+1][hero_pos[1]] = mazeA[hero_pos[0]+1][hero_pos[1]], \
                                          mazeA[hero_pos[0]][hero_pos[1]]
    return mazeA[hero_pos[0]][hero_pos[1]]

#============================================

#==========以下为系统判定======================
#check_crash判断是否相撞
def check_crash(move_to):
    if move_to==1:
        return "crash"
    else:
        screen_draw()
        pygame.time.delay(500)
#=============================================

#主循环事件
begin=False
while True:
    if begin == True:

        #正式运行部分。
        move_to = action(the_network.run(what_sensor(camera_sensor())))
        #判别是否Crash。
        result = check_crash(move_to)
        if result=="crash":
            print "crash!"
            break
    for event in pygame.event.get():

        if event.type == QUIT:
            #接收到退出事件后退出程序
            exit()
        if event.type == KEYDOWN:
            begin=True

    pygame.display.update()



