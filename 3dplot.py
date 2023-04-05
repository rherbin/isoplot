import pygame as pg
import sys
from math import sqrt,sin,cos,pi,floor

winsize = 500
display = pg.display.set_mode((winsize,winsize))
clock = pg.time.Clock()

func = lambda x,y:sin(x**2)+cos(y**2)
rx = [[1,0,0],
      [0,0,-1],
      [0,1,0]]

ry = [[0,0,-1],
      [0,1,0],
      [1,0,0]]

rz = [[1,0,0],
      [0,0,-1],
      [0,1,0]]

def iso(coords):
    x = 1/sqrt(2) * (coords[0] - coords[1])
    y = 1/sqrt(6) * (coords[0] + 2*coords[2] + coords[1])
    x2 = 1/sqrt(2) * (coords[0] - coords[1])
    y2 = 1/sqrt(6) * (coords[0] + coords[1])
    #z = 1/sqrt(6) * sqrt(2) * (coords[0] - coords[1] + coords[2])
    return (x+winsize/2,y+winsize/2),(x2+winsize/2,y2+winsize/2)

def plot(func=func ,delta=2, divdensity=2, height=1, rotate=0, zoom=1):
    values = [[( (x*delta*divdensity) / (100) , (y*delta*divdensity) / (100) , func((x*delta*divdensity) / (100),(y*delta*divdensity) / (100))) for x in range(-100//divdensity,100//divdensity+1)] for y in range(-100//divdensity,100//divdensity+1)]
    print(values[0][0],values[-1][-1])
    for x in range(len(values)):
        for y in range(len(values[x])):
            #cx,cy = iso(values[x][y])[0]
            #cz = 0.0
            
            fx,fy = values[x][y][0],values[x][y][1]
            cosr,sinr = cos(rotate),sin(rotate)
            fx,fy = fx*cosr-fy*sinr,fx*sinr+fy*cosr

            cx = (fx - fy) * zoom + winsize/2
            cy = ((fx + fy)/2) * zoom  + winsize/2
            cz = values[x][y][2] * height * zoom
            #pg.draw.line(display,"black",(cx,cy-cz),(cx,cy),1)
            pg.draw.circle(display,"white",(cx,cy-cz),1)

rotate = 0

while True:
    display.fill((0,0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        rotate += pi/16
    if keys[pg.K_LEFT]:
        rotate -= pi/16

    plot(divdensity=4,height=1,rotate=rotate,zoom=30, delta=4)

    clock.tick(10)
    pg.display.update()