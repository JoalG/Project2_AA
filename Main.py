import numpy as np 
import pygame
import random
from PIL import Image

import math
import threading
from Line import *
from Point import *






def pathTracing(source,px,boundarys,surface):
    for i in range (5) :
        point = Point(random.uniform(0,500),random.uniform(0,500))
        
        b = Line(point.x,point.y,source.x,source.y)
        
        d = source.distance(point)
       
        for j in boundarys:
            if j.instersect(b):
                print("Sí bro")
          

       
       
       
       
        
        b.draw(surface)

        d = source.distance(point)
        #print(d)













def getFrame(px):
    # grabs the current image and returns it
    pixels = np.roll(px,(1,2),(0,1))
    return pixels

def _main_():
    #pygame stuff
    h,w=550,550
    border=50
    pygame.init()
    screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
    pygame.display.set_caption("2D Raytracing")
    done = False
    clock = pygame.time.Clock()
    i = Image.new("RGB", (500, 500), (0, 0, 0) )
    px = np.array(i)




    sources = Point(195, 200)


    boundarys = [Line(350,100,350,400)]




    while True:
        #print("f")
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        npimage=(px)

        # Convert to a surface and splat onto screen offset by border width and height
        surface = pygame.surfarray.make_surface(npimage)
        #b = Boundary(350,100,350,400)
        boundarys[0].draw(surface)
        sources.draw(surface)
        b.draw(surface)
        pathTracing(sources,px,boundarys,surface)
        screen.blit(surface, (border, border))
        

        pygame.display.flip()
        #while(True):

        clock.tick(60)
    


_main_()