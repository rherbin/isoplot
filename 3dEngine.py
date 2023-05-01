from random import randint
from time import time
import pygame as pg
import sys
from math import sqrt,sin,cos,pi,factorial
import numpy as np

winsize = 1000
display = pg.display.set_mode((winsize,winsize))
clock = pg.time.Clock()

pg.font.init()
display_font = pg.font.SysFont('Arial', 15)
text = []
text.append(display_font.render("Increase/Decrease delta : E/R",True,"white"))
text.append(display_font.render("Increase/Decrease height : up/down arrow",True,"white"))
text.append(display_font.render("Increase/Decrease density : F/G",True,"white"))
text.append(display_font.render("rx : left/right arrow",True,"white"))
text.append(display_font.render("Zoom : mouse wheel",True,"white"))

def rx_mat(angle):
    return np.array([[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]])

def rz_mat(angle):
    return np.array([[cos(angle),0,-sin(angle)],[0,1,0],[sin(angle),0,cos(angle)]])

def ry_mat(angle):
    return np.array([[1,0,0],[0,cos(angle),-sin(angle)],[0,sin(angle),cos(angle)]])

isomat = np.array([[1,-1,0],[1/2,1/2,-1]])

def iso(coords):
    x = 1/sqrt(2) * (coords[0] - coords[1])
    y = 1/sqrt(6) * (coords[0] + 2*coords[2] + coords[1])
    x2 = 1/sqrt(2) * (coords[0] - coords[1])
    y2 = 1/sqrt(6) * (coords[0] + coords[1])
    return (x+winsize/2,y+winsize/2),(x2+winsize/2,y2+winsize/2)

class Object:

    def __init__(self,color):
        self.vertex = np.array([])
        self.edges = []
        self.faces = []
        self.color = color

    def createVertex(self,list):
        self.vertex = np.array(list)
    
    def createEdges(self,list):
        self.edges = list
    
    def openOBJ(self,name,pos=[0,0,0]):
        vertex = []
        edges = []
        faces = []
        pos = np.array(pos)
        t1 = time()
        with open(name,"r") as f:
            for x in f.readlines():
                x = x.split(" ")
                if x[0] == "v":
                    vertex.append(np.array([float(x[1]),float(x[2]),float(x[3])])+pos)
                elif x[0] == "f":
                    edges.append((int(x[1].split("/")[0])-1,int(x[2].split("/")[0])-1))
                    edges.append((int(x[2].split("/")[0])-1,int(x[3].split("/")[0])-1))
                    edges.append((int(x[3].split("/")[0])-1,int(x[1].split("/")[0])-1))

                    faces.append(tuple(int(x[i].split("/")[0])-1 for i in range(1,4)))
            f.close()
        self.vertex = np.array(vertex)
        self.edges = edges
        self.faces = faces
        t2 = time()
        print(f"Done loading model in {t2-t1} seconds")
    
    def plot(self):
        rot = np.matmul(rz_mat(rz),rx_mat(rx))
        translated = []
        poly = []

        for c in self.vertex:
            coords = np.matmul(rot,c-cam)

            if coords[0] < 0:
                translated.append(None)
                continue
            
            x = coords[1] * 800/coords[0] * zoom + winsize/2
            y = coords[2] * 800/coords[0] * zoom + winsize/2

            translated.append((x,y))

        for c in self.edges:
            coords1 = translated[c[0]]
            coords2 = translated[c[1]]

            if coords1 == None or coords2 == None:
                continue
            
            pg.draw.line(display,"white",coords1,coords2)
        
        for c in self.faces:
            coords1 = translated[c[0]]
            coords2 = translated[c[1]]
            coords3 = translated[c[2]]

            avg = (self.vertex[c[0]]+self.vertex[c[1]]+self.vertex[c[2]])/3

            dist = sqrt(np.sum((avg-cam)**2))

            if coords1 == None or coords2 == None or coords3 == None:
                continue
            
            poly.append(([coords1,coords2,coords3],dist,self.color))

        return poly

rx = 0
rz = 0
ry = 0
zoom = 1
cam = np.array([-3.0,0.0,0.0])

objects = []

object = Object("white")
object.openOBJ("cube.obj")
objects.append(object)

object2 = Object("gray")
object2.openOBJ("cube.obj",[2,0,0])
objects.append(object2)

pg.mouse.set_visible(False)

while True:
    display.fill((0,0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.mouse.set_visible(False)
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEWHEEL:
            if event.y == 1:
                zoom*=2
            elif event.y==-1:
                zoom*=(1/2)

    keys = pg.key.get_pressed()

    dm = pg.mouse.get_rel()

    rx -= pi/32*dm[0]*1/32
    rz -= pi/32*dm[1]*1/32

    pg.mouse.set_pos(winsize/2,winsize/2)

    if keys[pg.K_RIGHT]:
        rx -= pi/32
    if keys[pg.K_LEFT]:
        rx += pi/32
    if keys[pg.K_UP]:
        rz += pi/32
    if keys[pg.K_DOWN]:
        rz -= pi/32
    if keys[pg.K_r]:
        ry -= pi/2
    if keys[pg.K_e]:
        ry += pi/2
    if keys[pg.K_q]:
        cam[1] -= 1*cos(rx)
        cam[0] -= 1*sin(rx)
    if keys[pg.K_d]:
        cam[1] += 1*cos(rx)
        cam[0] += 1*sin(rx)
    if keys[pg.K_s]:
        cam[0] -= 1*cos(rx)
        cam[1] += 1*sin(rx)
    if keys[pg.K_z]:
        cam[0] += cos(rx)
        cam[1] -= sin(rx)
    if keys[pg.K_SPACE]:
        cam[2] -= 1
    if keys[pg.K_LCTRL]:
        cam[2] += 1

    poly = []

    for object in objects:
        poly += object.plot()

    poly.sort(key=lambda x:-x[1])
    for c in poly:
        pg.draw.polygon(display,c[2],c[0])

    for i in range(len(text)):
        pass
        #display.blit(text[i],(0,i*20))

    clock.tick(30)
    pg.display.update()