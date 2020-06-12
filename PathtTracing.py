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

class PathTracing:

    #Reflexion Espejo

    def reboteHorizontal(self,point, dx, dy, distance ):
        res = Point(0,0)
        res.x = int(point.x+(dx*distance))
        res.y = int(point.y+(dy*-1*distance))
        return res

    def reboteVertical(self,point, dx, dy, distance ):
        res = Point(0,0)
        res.x = int(point.x+(dx*-1*distance))
        res.y = int(point.y+(dy*distance))
        return res






    def pintarRayo(self, source, point, surface, px,intence,reflejo): 
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




    def iluminar(self,source,px,boundarys,surface,gMin, gMax):
        #Solo funciona con una fuente de Luz
        
        for i in range (1):
            
            recursos = 5000
            
            for j in range(gMin,gMax):
                
                pR  = j
               # print(pR)
                
                point = Point(source.x + math.cos(math.radians(pR))*300, source.y + math.sin(math.radians(pR))*300)
                
                

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
                point.x = int(point.x)
                point.y = int(point.y)
                ray = Line(source.x,source.y,point.x,point.y)
                distance = source.distance(point)
                self.PathTracing(boundarys,ray,surface,px,distance,False)
                

                
        print("Finish")



    def PathTracing(self,boundarys,ray,surface,px,distance,reflejo):

        Interseco = False
        #No elige el Boundary mas cercano 
        for boundary in boundarys:
            if boundary.isInstersect(ray):
                Interseco=True
                
                dx = ray.cambioX()
                dy = ray.cambioY()
                
                pI = boundary.calcInstersect(ray)
                pI.x = int (pI.x)
                pI.y = int (pI.y)
                ray.Point2 = pI
                distance = distance-ray.distance()
                
                pointF = self.reboteVertical(pI, dx, dy , distance)
                rayR = Line(pI.x,pI.y,pointF.x,pointF.y)
                self.PathTracing(boundarys,rayR,surface,px,distance,True)
                #self.pathTracing(pI,px,boundarys,surface,90, 270) 
                
                

        self.pintarRayo(ray.Point1, ray.Point2, surface, px,1.26,reflejo)



    def getFrame(self,px):
        # grabs the current image and returns it
        pixels = np.roll(px,(1,2),(0,1))
        return pixels

    def main(self):
            
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
        ph = np.array(i)
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
                t = threading.Thread(target = self.iluminar, args=(sources,px,boundarys,surface,0,360) ) # f being the function that tells how the ball should move
                t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
                t.start()
                first=False
                
            screen.blit(surface, (border, border))
            pygame.display.flip()
            clock.tick(60)

p = PathTracing()
p.main()