import numpy as np 
import pygame
import random
from PIL import Image

import math
import threading
from Boundary import *

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


    #reference image for background color
    im_file = Image.open("fondo.png")
    ref = np.array(im_file)

    #light positions
    #sources = [ Point(195, 200), Point( 294, 200) ]

    #light color
    light = np.array([1, 1, 0.75])

    while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        for i in range(500):
            for j in range(500):
                if(i>250):
                    px[i][j]= ref[j][i][:3]*3
                else:
                    px[i][j]= ref[j][i][:3]
                    px[i][j][0]= px[i][j][0]*1
                    px[i][j][1]= px[i][j][1]*1
                    px[i][j][2]= px[i][j][2]*0.1

        # Clear screen to white before drawing 
        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        npimage=(px)

        # Convert to a surface and splat onto screen offset by border width and height
        surface = pygame.surfarray.make_surface(npimage)
        b = Boundary(195,200,294,200)
        b.draw(surface)
        screen.blit(surface, (border, border))

        pygame.display.flip()
        
        clock.tick(60)
    


_main_()