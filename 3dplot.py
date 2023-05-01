import pygame as pg
import sys
from math import sqrt,sin,cos,pi,factorial
import numpy as np

winsize = 500
display = pg.display.set_mode((winsize,winsize))
clock = pg.time.Clock()

pg.font.init()
display_font = pg.font.SysFont('Arial', 15)
text = []
text.append(display_font.render("Increase/Decrease delta : E/R",True,"white"))
text.append(display_font.render("Increase/Decrease height : up/down arrow",True,"white"))
text.append(display_font.render("Increase/Decrease density : F/G",True,"white"))
text.append(display_font.render("Rotate : left/right arrow",True,"white"))
text.append(display_font.render("Zoom : mouse wheel",True,"white"))

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

def weakmat(focal,coords,cam):
    coords -= cam
    x = coords[0] * focal/coords[1]
    y = coords[1] * focal/coords[2]
    return np.array([x,y])

isomat = np.array([[1,-1,0],[1/2,1/2,-1]])

def iso(coords):
    x = 1/sqrt(2) * (coords[0] - coords[1])
    y = 1/sqrt(6) * (coords[0] + 2*coords[2] + coords[1])
    x2 = 1/sqrt(2) * (coords[0] - coords[1])
    y2 = 1/sqrt(6) * (coords[0] + coords[1])
    return (x+winsize/2,y+winsize/2),(x2+winsize/2,y2+winsize/2)

class Graph:

    def __init__(self):
        self.stpnb = False
        self.vertex = np.array([])
        self.edges = []
    
    def evaluate(self,func=lambda x,y:0,delta=2,divdensity=2):

        if self.stpnb:
            values = []
            for y in range(-100//divdensity,100//divdensity+1):
                line = []
                for x in range(-100//divdensity,100//divdensity+1):
                    rx = (x*delta*divdensity)/(100)
                    ry = (y*delta*divdensity)/(100)
                    line.append([rx, ry, func(rx,ry)])
                values += line
            self.vertex = np.array(values)

        else:
            values = []
            delta = int(delta*100)
            for y in range(-(delta)//(divdensity),(delta)//(divdensity)+1):
                line = []
                for x in range(-(delta)//(divdensity),(delta)//(divdensity)+1):
                    rx = (x*divdensity)/(100)
                    ry = (y*divdensity)/(100)
                    line.append([rx, ry, func(rx,ry)])
                values += line
            self.vertex = np.array(values)

    def createVertex(self,list):
        self.vertex = np.array(list)
    
    def createEdges(self,list):
        self.edges = list

    def plot(self, height=1, rotate=0, zoom=1):
        axis = [[[-1000,0,0],[1000,0,0]],[[0,-1000,0],[0,1000,0]],[[0,0,-1000],[0,0,1000]]]
        rot = rot_mat(rotate)
        for x in self.vertex:
            
            coords = np.matmul(rot,x)
            coords[2] *= height
            coords = np.matmul(isomat,coords)*zoom

            coords += winsize/2

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
    
    def plot2(self,rotate,zoom):
        axis = np.array([[[-1000,0,0],[1000,0,0]],[[0,-1000,0],[0,1000,0]],[[0,0,-1000],[0,0,1000]]])
        rot = rot_mat(rotate)
        todraw = []
        global cam
        """for c in self.vertex:
            coords = np.matmul(rot,c-cam)
            if coords[0] < 0:
                continue
            x = coords[1] * 400/coords[0] * zoom + winsize/2
            y = coords[2] * 400/coords[0] * zoom + winsize/2
            todraw.append((x,y))
        for point in todraw:
            pg.draw.circle(display,"white",point,3)
        for edge in self.edges:
            try:
                pg.draw.line(display,"white",todraw[edge[0]],todraw[edge[1]])
            except:
                pass"""
        
        for c in self.edges:
            coords1 = np.matmul(rot,self.vertex[c[0]]-cam)
            coords2 = np.matmul(rot,self.vertex[c[1]]-cam)

            if coords1[0] < 0 or coords2[0] <0:
                continue
            
            x1 = coords1[1] * 400/coords1[0] * zoom + winsize/2
            y1 = coords1[2] * 400/coords1[0] * zoom + winsize/2

            
            x2 = coords2[1] * 400/coords2[0] * zoom + winsize/2
            y2 = coords2[2] * 400/coords2[0] * zoom + winsize/2

            
            pg.draw.line(display,"white",(x1,y1),(x2,y2))


rotate = 0
zoom = 1
height = 1
delta = 2
density = 8
cam = np.array([0,0,0])

def inputfunc():
    global func
    try:
        func = eval("lambda x,y:"+input("Input a function to plot (with x and y variables) : "))
    except SyntaxError:
        func = lambda x,y:cos(x**2)+sin(y**2)

#inputfunc()

graph = Graph()
#graph.evaluate(func,delta,density)

graph.createVertex([[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]])
graph.createEdges([(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,6),(4,5),(5,7),(6,7)])

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
        graph.evaluate(func,delta,density)
    if keys[pg.K_r]:
        delta -= .1
        graph.evaluate(func,delta,density)
    if keys[pg.K_g] and density > 1:
        density -= 1
        graph.evaluate(delta,density)
    if keys[pg.K_f]:
        density += 1
        graph.evaluate(delta,density)
    if keys[pg.K_q]:
        cam[1] -= 1
    if keys[pg.K_d]:
        cam[1] += 1
    if keys[pg.K_s]:
        cam[0] -= 1
    if keys[pg.K_z]:
        cam[0] += 1

    #graph.plot(height=height,rotate=rotate,zoom=zoom)
    graph.plot2(rotate,zoom)

    for i in range(len(text)):
        display.blit(text[i],(0,i*20))

    clock.tick(30)
    pg.display.update()