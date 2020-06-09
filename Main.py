import numpy as np 
import pygame
import random
from PIL import Image

import math
import threading
from Line import *
from Point import *






def reboteHorizontal(point, dx, dy, distance ):
    res = Point(0,0)
    res.x = int(point.x+(dx*distance))
    res.y = int(point.y+(dy*-1*distance))
    return res

def reboteVertical(point, dx, dy, distance ):
    res = Point(0,0)
    res.x = int(point.x+(dx*-1*distance))
    res.y = int(point.y+(dy*distance))
    return res






def pathTracing(source,px,boundarys,surface):
    #print("p")
    im_file = Image.open("fondo.png")
    ref = np.array(im_file)
    for i in range (500) :
        for j in range(500):
            point = Point(i,j)
            
            ray = Line(source.x,source.y,point.x,point.y)
            
            distance = source.distance(point)
            Inter = False
        
            for boundary in boundarys:
                if boundary.instersect(ray):
                    Inter=True



                    dx = ray.cambioX()
                    dy = ray.cambioY()
                    pI = boundary.calcInstersect(ray)
                    ray.Point2 = boundary.calcInstersect(ray)
                    if(boundary.orientacion()==0):
                        pointF = reboteVertical(pI, dx, dy , distance-ray.distance())
                    else:
                        pointF = reboteHorizontal(pI, dx, dy , distance-ray.distance())
                    #ray.Point2 = boundary.calcInstersect(ray)

                    rayR = Line(pI.x,pI.y,pointF.x,pointF.y)
                
                    px[int(pointF.x)][int(pointF.y)]=ref[int(pointF.x)][int(pointF.y)][:3]*1.5
                    #rayR.draw(surface)

                    break

                # print(ray.Point2)
            if not (Inter):
                px[int(point.x)][int(point.y)]=ref[int(point.x)][int(point.y)][:3]*1.5
                
            

        
        
        
        
            
            #ray.draw(surface)

            distance = source.distance(point)
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


    boundarys = [Line(350,400,350,100),Line(100,400,100,100),Line(350,400,100,400),Line(350,100,100,100)]



    first= True
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
        for i in boundarys:
            i.draw(surface)
        
        sources.draw(surface)
        if first:
            t = threading.Thread(target = pathTracing, args=(sources,px,boundarys,surface) ) # f being the function that tells how the ball should move
            t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
            t.start()
            first=False 
        
        screen.blit(surface, (border, border))
        

        pygame.display.flip()
        #while(True):

        clock.tick(60)
    


_main_()