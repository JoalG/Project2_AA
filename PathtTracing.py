import numpy as np 
import pygame
import random
from PIL import Image


import math
import threading
from Line import *
from Point import *
from Borde import *
from FuenteDeLuz import * 
import time

from bresenham import bresenham

class PathTracing:


    #Reflexion Espejo

    def reboteHorizontal(self,point, dx, dy, distance ):
        res = Point(0,0)
        res.x = (point.x+(dx*distance))
        res.y = (point.y+(dy*-1*distance))
        return res

    def reboteVertical(self,point, dx, dy, distance ):
        res = Point(0,0)
        res.x = (point.x+(dx*-1*distance))
        res.y = (point.y+(dy*distance))
        return res


    #boundary is a line
    #ray is a line
    def getReflectionVector(self, ray, boundary, sizeX, sizeY,distance):

        destiny = Point(0,0)

        if boundary.line.Point1.x == boundary.line.Point2.x:
            if ray.Point1.x < boundary.line.Point1.x:
                grados = random.uniform(90,270)
                point = Point(ray.Point2.x + math.cos(math.radians(grados))*distance, ray.Point2.y + math.sin(math.radians(grados))*distance)
                destiny = point
            else:
                grados = random.uniform(270,270+180)
                point = Point(ray.Point2.x + math.cos(math.radians(grados))*distance, ray.Point2.y + math.sin(math.radians(grados))*distance)
                destiny = point            #destiny.y = int(random.uniform(0,sizeY))
        
        if boundary.line.Point1.y == boundary.line.Point2.y:
            #print("Puntos", ray.Point1.y, boundary.line.Point1.y)
            if ray.Point1.y < boundary.line.Point1.y:
                grados = random.uniform(180,360)
                point = Point(ray.Point2.x + math.cos(math.radians(grados))*distance, ray.Point2.y + math.sin(math.radians(grados))*distance)
                destiny = point
            else:
                grados = random.uniform(0,180)
                point = Point(ray.Point2.x + math.cos(math.radians(grados))*distance, ray.Point2.y + math.sin(math.radians(grados))*distance)

                destiny = point

        destiny.x = (destiny.x)
        destiny.y = (destiny.y)        
        return destiny
        



    def pintarRayo(self, source, point, surface, px,intence,reflejo,ref,sourceColor,puntosPintados, totalDistance): 

        puntos = list(bresenham(int(source.x),int(source.y),int(point.x),int(point.y)))
        #print(puntos)
        distance = source.distance(point)

        for pixel in puntos:

            destiny = Point(pixel[0],pixel[1])
            distance = source.distance(destiny) + totalDistance
            intesity = (1-(distance/intence))**2

            if(pixel[0]>=0 and pixel[0]<500 and pixel[1]>=0 and pixel[1]<500):

                if not reflejo:
                    if not puntosPintados[int(pixel[0])][int(pixel[1])]:
                        px[int(pixel[0])][int(pixel[1])]=ref[int(pixel[0])][int(pixel[1])][:3]*intesity
                        puntosPintados[int(pixel[0])][int(pixel[1])] = True
                    else:
                        intesity += px[int(pixel[0])][int(pixel[1])][0]/ref[int(pixel[0])][int(pixel[1])][0]
                        if(intesity > 1):
                            intesity = 1
                        px[int(pixel[0])][int(pixel[1])]=ref[int(pixel[0])][int(pixel[1])][:3]*intesity
                        
                else:
                    if not puntosPintados[int(pixel[0])][int(pixel[1])]:
                        px[int(pixel[0])][int(pixel[1])]=ref[int(pixel[0])][int(pixel[1])][:3]*intesity
                        puntosPintados[int(pixel[0])][int(pixel[1])] = True
                    else:
                        intesity += px[int(pixel[0])][int(pixel[1])][0]/ref[int(pixel[0])][int(pixel[1])][0]
                        if(intesity > 1):
                            intesity = 1
                        px[int(pixel[0])][int(pixel[1])]=ref[int(pixel[0])][int(pixel[1])][:3]*intesity
                





    def get_color(colorRGBA1, colorRGBA2):
        red   = (colorRGBA1[0] + colorRGBA2[0]) / 2
        green = (colorRGBA1[1] + colorRGBA2[1]) / 2
        blue  = (colorRGBA1[2] + colorRGBA2[2]) / 2
        return [int(red), int(green), int(blue)]

    def iluminar(self,sources,px,boundarys,surface,gMin, gMax, ref):
        #Solo funciona con una fuente de Luz
 
        puntosPintados = []
        for k in range(500):
            fila = []
            for l in range(500):
                fila += [False]
            puntosPintados += [fila]        
        for source in sources:
            
            for j in range(gMin,gMax*10):

                for i in range (1):

                    point = Point(source.Fuente.x + math.cos(math.radians(j/10))*500, source.Fuente.y + math.sin(math.radians(j/10))*500)
                    

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
                    
                    
                    point.x = (point.x)
                    point.y = (point.y)
                    ray = Line(source.Fuente.x,source.Fuente.y,point.x,point.y)
                    distance = source.Fuente.distance(point)

                    self.PathTracing(boundarys,ray,surface,px,distance,False,ref,source.color,puntosPintados,0) #distancia total en cero
                    



    def PathTracing(self,boundarys,ray,surface,px,distance,reflejo,ref,sourceColor,puntosPintados, totalDistance):
        #print(sourceColor)

        dx = ray.cambioX()
        dy = ray.cambioY()
        Interseco = False
        pInterseccion = ray.Point2
        #No elige el Boundary mas cercano 
        tempTotalDistance = ray.distance()
        for boundary in boundarys:

            if boundary.line.isInstersect(ray):
                Interseco=True
                

                
                pInterseccionTemp = boundary.line.calcInstersect(ray)
                pInterseccionTemp.x = (pInterseccionTemp.x)
                pInterseccionTemp.y = (pInterseccionTemp.y)

                if(ray.Point1.distance(pInterseccionTemp)<ray.Point1.distance(pInterseccion)):
                    pInterseccion = pInterseccionTemp
                    interBound = boundary

        if(Interseco):
            ray.Point2 = pInterseccion
            distance = distance-ray.distance()
            pointFinal = self.getReflectionVector(ray,interBound,500,500,distance)
            rayRebote = Line(pInterseccion.x,pInterseccion.y,pointFinal.x,pointFinal.y)
            self.PathTracing(boundarys,rayRebote,surface,px,distance,True,ref,ref[int(pInterseccion.x)][int(pInterseccion.y)][:3],puntosPintados,ray.distance()+totalDistance)
                                                           #entre más grande más iluminado, le damos 1000         
        self.pintarRayo(ray.Point1, ray.Point2, surface, px,400,reflejo,ref,sourceColor,puntosPintados,totalDistance)



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
        ref2 = np.array(im_file)
         
        for i in range(500):
            for j in range(500):
                ref[i][j]=ref2[j][i]




        i = Image.new("RGB", (500, 500), (0, 0, 0) )
        ph = np.array(i)
        px = np.array(i)


        

        sources = [FuenteDeLuz(100, 300, (0,255,255)),FuenteDeLuz(350, 50, (0,255,255))]
        #boundarys = [Line(200,400,450,400),Line(200,100,450,100),Line(200,100,200,400),Line(400,100,400,400)]
        #boundarys = [Borde(200,99,200,401,False),Borde(400,99,400,401,False),Borde(0,100,401,100,False),Borde(0,400,401,400,False)]
        boundarys = [Borde(200,200,400,200,False), Borde(200,400,400,400,False), Borde(200,200,200,400,False), Borde(400,200,400,400,False)]


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
            for bound in boundarys:
                bound.draw(surface)
            

            for source in sources:
                source.draw(surface)
         
    
            if first:
                t = threading.Thread(target = self.iluminar, args=(sources,px,boundarys,surface,0,360,ref) ) # f being the function that tells how the ball should move
                t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
                t.start()
                first=False


                
            screen.blit(surface, (border, border))
            pygame.display.flip()
            clock.tick(60)

p = PathTracing()
p.main()