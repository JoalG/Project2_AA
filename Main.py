import numpy as np 
import pygame
import random
from PIL import Image

import math
import threading
from Line import *
from Point import *
import time





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



def reflejo(source, point, surface, px): 
    #print("pichaaa")

    im_file = Image.open("fondo.png")
    ref = np.array(im_file)
    x = source.x
    y = source.y
    
    
    distanciaX = abs(point.x-source.x)
    distanciaY = abs(point.y-source.y)
    xParaY = distanciaX

    if(distanciaY!=0):
        xParaY = int(distanciaX/distanciaY)

    while(distanciaX != 0 and distanciaY !=0):
        #print("BIG F")
        for i in range(xParaY):
            if(x>=0 and x<500 and y>=0 and y<500):
                px[int(x)][int(y)]=ref[int(x)][int(y)][:3]*10
            if(source.x >point.x):
                x-=1
            else:
                x+=1
            distanciaX-=1
        if(source.y >point.y):
            y-=1
        else:
            y+=1
        distanciaY-=1
      
    
        
            

        






def pathTracing2(source,px,boundarys,surface,xmin,xmax,ymin,ymax):
    im_file = Image.open("fondo.png")
    ref = np.array(im_file)
    for i in range (xmin,xmax):
        time.sleep(0.000001)
        #print(i)
        #print(i)
        for j in range(ymin,ymax):

            point = Point(i, j)
            
            

            ray = Line(source.x,source.y,point.x,point.y)
            #ray.draw(surface)

            distance = source.distance(point)
            
            Interseco = False
        
            for boundary in boundarys:
                if boundary.isInstersect(ray):
                    Interseco=True
                   # print("siiiii")


                    dx = ray.cambioX()
                    dy = ray.cambioY()
                    pI = boundary.calcInstersect(ray)
                    pI.x = int (pI.x)
                    pI.y = int (pI.y)

                    ray.Point2 = pI
                    
                    pointF = reboteVertical(pI, dx, dy , distance-ray.distance())
                    
                    

                    rayR = Line(pI.x,pI.y,pointF.x,pointF.y)
                    

                   # t = threading.Thread(target = reflejo, args=(pI, pointF, surface, px) ) # f being the function that tells how the ball should move
                  #  t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
                 #   t.start()
                    
                    reflejo(pI, pointF, surface, px)
                    
                    #px[int(pointF.x)][int(pointF.y)]=ref[int(pointF.x)][int(pointF.y)][:3]*1.5
                    #rayR.draw(surface)

                    

                 #print(ray.Point2)

            #if(not Interseco):

                
                #px[int(point.x)][int(point.y)]=ref[int(point.x)][int(point.y)][:3]*1
                
            

        
        
        

            #print("aiuda")
            if(not Interseco):
                #ray.draw(surface)
                px[int(point.x)][int(point.y)]=ref[int(point.x)][int(point.y)][:3]*2

            distance = source.distance(point)
            #print(d)


    #t1 = time.time() - start_time 
    print("Finalizo con 500")












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


    boundarys = [Line(350,400,350,100)]

            # Get a numpy array to display from the simulation





    first= True
    while True:
        #print("f")
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        screen.fill((255, 255, 255))


        # Convert to a surface and splat onto screen offset by border width and height
        npimage=(px)
        surface = pygame.surfarray.make_surface(npimage)

        #b = Boundary(350,100,350,400)
        for i in boundarys:
            i.draw(surface)
        
        sources.draw(surface)
   
        if first:
            t = threading.Thread(target = pathTracing2, args=(sources,px,boundarys,surface,0,250,0,250) ) # f being the function that tells how the ball should move
            t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
            t.start()
            t1 = threading.Thread(target = pathTracing2, args=(sources,px,boundarys,surface,250,500,250,500) ) # f being the function that tells how the ball should move
            t1.setDaemon(True) # Alternatively, you can use "t.daemon = True"
            t1.start()
            t2 = threading.Thread(target = pathTracing2, args=(sources,px,boundarys,surface,0,250,250,500) ) # f being the function that tells how the ball should move
            t2.setDaemon(True) # Alternatively, you can use "t.daemon = True"
            t2.start()
            t3 = threading.Thread(target = pathTracing2, args=(sources,px,boundarys,surface,250,500,0,250) ) # f being the function that tells how the ball should move
            t3.setDaemon(True) # Alternatively, you can use "t.daemon = True"
            t3.start()
            first=False
        
        screen.blit(surface, (border, border))
        

        pygame.display.flip()
        #while(True):

        clock.tick(60)
    


_main_()