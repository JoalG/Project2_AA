import numpy as np 
import pygame
import random
from PIL import Image

import math
import threading
from Line import *
from Point import *
import time

from bresenham import bresenham





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




def reflejo(source, point, surface, px,intence,reflejo): 
    #print("pichaaa")

    im_file = Image.open("fondo.png")
    ref = np.array(im_file)

    puntos = list(bresenham(source.x,source.y,point.x,point.y))
    #print(puntos)
    
    for pixel in puntos:
        if(pixel[0]>=0 and pixel[0]<500 and pixel[1]>=0 and pixel[1]<500):
            px[int(pixel[0])][int(pixel[1])]=px[int(pixel[0])][int(pixel[1])]*intence
            if reflejo:
                px[int(pixel[0])][int(pixel[1])]=px[int(pixel[0])][int(pixel[1])]*[1,0.5,1]





  #  x = source.x
 #   y = source.y
    
    


  
  #  distanciaX = abs(point.x-source.x)
   # distanciaY = abs(point.y-source.y)
   # xParaY = distanciaX

    #if(distanciaY!=0):
     #   xParaY = int(distanciaX/distanciaY)

 #   while(distanciaX != 0 and distanciaY !=0):
        
        #print("BIG F")
   #     for i in range(xParaY):
  #
    #        if(x>=0 and x<500 and y>=0 and y<500):
     #           px[int(x)][int(y)]=px[int(x)][int(y)][:3]*intence
      #      if(source.x >point.x):
       #         x-=1
        #    else:
         #       x+=1
          #  distanciaX-=1
 #       if(source.y >point.y):
  #          y-=1
   #     else:
    #        y+=1
     #   distanciaY-=1
      
    
        
            

        
      
    
        
            

        






def pathTracing2(source,px,boundarys,surface,xmin,xmax,ymin,ymax):
    print("FF")
    pintados = []
    for i in range(500):
        fila =[]
        for j in range(500):
            fila+=[False]
        pintados+=[fila]

    bordes=[]




    for i in range (500):
        
        #print(i)
        #print(i)
        for j in range(500):
            
            if (i!=0 and j !=0) and  (i!=499 and j !=499):
                continue
           
            aleatorios = np.random.normal(0,500,2)
            
            point = Point(i,j)
            if(point.x<0):
                point.x = 0
            if(point.x>499):
                point.x = 499
            if(point.y<0):
                point.y = 0
            if(point.y>499):
                point.y =499 

            if(point.y == point.x):
                continue 

            if(point.y == 499 and point.x ==0)   :
                continue       
            if(point.x == 499 and point.y ==0)   :
                continue        
 
          #  print("verga")
            point.x = int(point.x)
            point.y = int(point.y)
            ray = Line(source.x,source.y,point.x,point.y)
           # print(ray.Point2)
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
                    

                   # t = threading.Thread(target = reflejo, args=(pI, pointF, surface, px, 8) ) # f being the function that tells how the ball should move
                  #  t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
                 #   t.start()

                  #  print(pI)
                   # print(pointF)
                    reflejo(pI, pointF, surface, px,1.3,True)
                    
                    #px[int(pointF.x)][int(pointF.y)]=ref[int(pointF.x)][int(pointF.y)][:3]*1.5
                    #rayR.draw(surface)

                    

                 #print(ray.Point2)

            #if(not Interseco):

                
                #px[int(point.x)][int(point.y)]=ref[int(point.x)][int(point.y)][:3]*1
                
            

        
        
         #   print(ray.Point1)
          #  print(ray.Point2)
            reflejo(ray.Point1, ray.Point2, surface, px,1.2,False)
            #print("aiuda")
            #if(not Interseco):
             #   ray.draw(surface)
                
               # px[int(point.x)][int(point.y)]=ref[int(point.x)][int(point.y)][:3]*2

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

    im_file = Image.open("fondo.png")
    ref = np.array(im_file)
    i = Image.new("RGB", (500, 500), (0, 0, 0) )
    px = np.array(i)
    for i in range(500):
        for j in range(500):
            px[i][j]= ref[i][j][:3]*0.6






    sources = Point(220, 200)


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
            t = threading.Thread(target = pathTracing2, args=(sources,px,boundarys,surface,0,500,0,500) ) # f being the function that tells how the ball should move
            t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
            t.start()
            first=False
            
        
        screen.blit(surface, (border, border))
        

        pygame.display.flip()
        #while(True):

        clock.tick(60)
    


_main_()