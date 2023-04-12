import pygame as pg
import sys
from math import sqrt,sin,cos,pi,factorial
import numpy as np

winsize = 500
display = pg.display.set_mode((winsize,winsize))
clock = pg.time.Clock()

rx = [[1,0,0],
      [0,0,-1],
      [0,1,0]]

ry = [[0,0,-1],
      [0,1,0],
      [1,0,0]]

rz = [[1,0,0],
      [0,0,-1],
      [0,1,0]]

def rot_mat(angle):
    return np.array([[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]])

isomat = np.array([[1,-1,0],[1/2,1/2,-1]])

def iso(coords):
    x = 1/sqrt(2) * (coords[0] - coords[1])
    y = 1/sqrt(6) * (coords[0] + 2*coords[2] + coords[1])
    x2 = 1/sqrt(2) * (coords[0] - coords[1])
    y2 = 1/sqrt(6) * (coords[0] + coords[1])
    #z = 1/sqrt(6) * sqrt(2) * (coords[0] - coords[1] + coords[2])
    return (x+winsize/2,y+winsize/2),(x2+winsize/2,y2+winsize/2)

class Graph:

    def __init__(self,func=lambda x,y:0,delta=2,divdensity=2,stpnb=False):
        self.func = func
        self.stpnb = stpnb
        self.evaluate(delta,divdensity)
    
    def evaluate(self,delta=2,divdensity=2):

        if self.stpnb:
            values = []
            for y in range(-100//divdensity,100//divdensity+1):
                line = []
                for x in range(-100//divdensity,100//divdensity+1):
                    rx = (x*delta*divdensity)/(100)
                    ry = (y*delta*divdensity)/(100)
                    line.append([rx, ry, self.func(rx,ry)])
                values += line
            #self.values = [[( (x*delta*divdensity) / (100) , (y*delta*divdensity) / (100) , func((x*delta*divdensity) / (100),(y*delta*divdensity) / (100))) for x in range(-100//divdensity,100//divdensity+1)] for y in range(-100//divdensity,100//divdensity+1)]
            self.values = np.array(values)

        else:
            values = []
            delta = int(delta*100)
            for y in range(-(delta)//(divdensity),(delta)//(divdensity)+1):
                line = []
                for x in range(-(delta)//(divdensity),(delta)//(divdensity)+1):
                    rx = (x*divdensity)/(100)
                    ry = (y*divdensity)/(100)
                    line.append([rx, ry, self.func(rx,ry)])
                values += line
            self.values = np.array(values)

    def plot(self, height=1, rotate=0, zoom=1):
        axis = [[[-1000,0,0],[1000,0,0]],[[0,-1000,0],[0,1000,0]],[[0,0,-1000],[0,0,1000]]]
        rot = rot_mat(rotate)
        for x in self.values:
            
            coords = x
            coords = np.matmul(rot,coords)
            coords[2] *= height
            coords = np.matmul(isomat,coords)*zoom

            coords += winsize/2

            #cx = (fx - fy) * zoom + winsize/2
            #cy = ((fx + fy)/2) * zoom  + winsize/2
            #cz = self.values[x][y][2] * height * zoom

            pg.draw.circle(display,"white",coords,1)
        for x in axis:
            fx,fy = x[0][0],x[0][1]
            cosr,sinr = cos(rotate),sin(rotate)
            fx,fy = fx*cosr-fy*sinr,fx*sinr+fy*cosr

            cx = (fx - fy) + winsize/2
            cy = ((fx + fy)/2) + winsize/2
            cz = x[0][2]
            cord1 = (cx,cy-cz)

            fx,fy = x[1][0],x[1][1]
            cosr,sinr = cos(rotate),sin(rotate)
            fx,fy = fx*cosr-fy*sinr,fx*sinr+fy*cosr

            cx = (fx - fy) + winsize/2
            cy = ((fx + fy)/2) + winsize/2
            cz = x[1][2]
            cord2 = (cx,cy-cz)

            pg.draw.line(display,"white",cord1,cord2,1)

rotate = 0
zoom = 1
height = 1
delta = 2

try:
    func = eval("lambda x,y:"+input("Input a function to plot (with x and y variables) : "))
except SyntaxError:
    func = lambda x,y:cos(x**2)+sin(y**2)

graph = Graph(func=func,divdensity=8,delta=2,stpnb=False)

while True:
    display.fill((0,0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEWHEEL:
            if event.y == 1:
                zoom*=2
            elif event.y==-1:
                zoom*=(1/2)

    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        rotate += pi/32
    if keys[pg.K_LEFT]:
        rotate -= pi/32
    if keys[pg.K_UP]:
        height*=1.5
    if keys[pg.K_DOWN]:
        height*=1/1.5
    if keys[pg.K_e]:
        delta += .1
        graph.evaluate(delta,8)
    if keys[pg.K_r]:
        delta -= .1
        graph.evaluate(delta,8)

    graph.plot(height=height,rotate=rotate,zoom=zoom)

    clock.tick(30)
    pg.display.update()