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

    def getReflectionVectorEspejo(self, ray, boundary, dx, dy,distance):

        if boundary.line.Point1.x == boundary.line.Point2.x:
            return self.reboteVertical(ray.Point2, dx, dy, distance)
        
        else:
            return self.reboteHorizontal(ray.Point2, dx, dy, distance)
        


    def pintarRayo(self, source, point, surface, px,intence,reflejo,ref,sourceColor,intensidades, totalDistance, colores, puntosPintados, numRebote): 

        puntos = list(bresenham(int(source.x),int(source.y),int(point.x),int(point.y)))
        #print(puntos)
        distance = source.distance(point)

        for pixel in puntos:

            destiny = Point(pixel[0],pixel[1])
            distance = source.distance(destiny) + totalDistance

            intesity = (1-(distance/intence))**2
            if(pixel[0]>=0 and pixel[0]<500 and pixel[1]>=0 and pixel[1]<500):

                pixelPosX = int(pixel[0])
                pixelPosY = int(pixel[1])

                if not reflejo:
                    
                    if not puntosPintados[pixelPosX][pixelPosY][0]:
                        intesity += intensidades[pixelPosX][pixelPosY]
                        if(intesity > 1):
                            intesity = 1

                        if colores[pixelPosX][pixelPosY] == [0,0,0]:                      
                            px[pixelPosX][pixelPosY]=ref[pixelPosX][pixelPosY][:3]*intesity
                            px[pixelPosX][pixelPosY][0] *= (sourceColor[0]/255)
                            px[pixelPosX][pixelPosY][1] *= (sourceColor[1]/255)
                            px[pixelPosX][pixelPosY][2] *= (sourceColor[2]/255)
                            colores[pixelPosX][pixelPosY] = [sourceColor[0],sourceColor[1],sourceColor[2]]
                        else:
                            combinedColors = self.get_color(colores[pixelPosX][pixelPosY], sourceColor)
                            colores[pixelPosX][pixelPosY] = combinedColors

                            r = combinedColors[0]/255
                            g = combinedColors[1]/255
                            b = combinedColors[2]/255

                            px[pixelPosX][pixelPosY]=ref[pixelPosX][pixelPosY][:3]*intesity
                            px[pixelPosX][pixelPosY][0] *= r
                            px[pixelPosX][pixelPosY][1] *= g
                            px[pixelPosX][pixelPosY][2] *= b

                        puntosPintados[pixelPosX][pixelPosY][0] = True
                        intensidades[pixelPosX][pixelPosY] = intesity        
            
                else:
                    if numRebote <= 3:
                        if not puntosPintados[pixelPosX][pixelPosY][numRebote]:
                            intesity += intensidades[pixelPosX][pixelPosY]
                            if intesity > 1:
                                intesity = 1

                            if colores[pixelPosX][pixelPosY] == [0,0,0]:                      
                                px[pixelPosX][pixelPosY]=ref[pixelPosX][pixelPosY][:3]*intesity
                                px[pixelPosX][pixelPosY][0] *= (sourceColor[0]/255)
                                px[pixelPosX][pixelPosY][1] *= (sourceColor[1]/255)
                                px[pixelPosX][pixelPosY][2] *= (sourceColor[2]/255)
                                colores[pixelPosX][pixelPosY] = [sourceColor[0],sourceColor[1],sourceColor[2]]
                            else:
                                
                                combinedColors = self.get_color(colores[pixelPosX][pixelPosY], sourceColor)
                                colores[pixelPosX][pixelPosY] = combinedColors

                                r = combinedColors[0]/255
                                g = combinedColors[1]/255
                                b = combinedColors[2]/255

                                px[pixelPosX][pixelPosY]=ref[pixelPosX][pixelPosY][:3]*intesity
                                px[pixelPosX][pixelPosY][0] *= r
                                px[pixelPosX][pixelPosY][1] *= g
                                px[pixelPosX][pixelPosY][2] *= b
                            
                            if not puntosPintados[pixelPosX][pixelPosY][1]:
                                puntosPintados[pixelPosX][pixelPosY][1] = True
                            elif not puntosPintados[pixelPosX][pixelPosY][2]:
                                puntosPintados[pixelPosX][pixelPosY][2] = True
                            else:
                                puntosPintados[pixelPosX][pixelPosY][3] = True
                            intensidades[pixelPosX][pixelPosY] = intesity
          

                


    def get_color(self, colorRGBA1, colorRGBA2):
        red   = (colorRGBA1[0] + colorRGBA2[0]) / 2
        green = (colorRGBA1[1] + colorRGBA2[1]) / 2
        blue  = (colorRGBA1[2] + colorRGBA2[2]) / 2
        return [int(red), int(green), int(blue)]

    def iluminar(self,sources,px,boundarys,surface,gMin, gMax, ref):
        #Solo funciona con una fuente de Luz

        maxLightDistance = math.sqrt((500*2)+(500**2))
        intensidades = []
        colores = []
        for k in range(500):
            fila = []
            filaColores = []
            for l in range(500):
                fila += [0]
                elemColores = []
                elemColores += [0]
                elemColores += [0]
                elemColores += [0]
                filaColores += [elemColores]
            intensidades += [fila]
            colores += [filaColores]        
        for source in sources:
        
            puntosPintados = []
            for k in range(500):
                fila = []
                for l in range(500):
                    inside = []
                    inside += [False]
                    inside += [False]
                    inside += [False]
                    inside += [False]
                    fila += [inside]
                puntosPintados += [fila]

            sourceColor = list(source.color)
        
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

                    self.PathTracing(boundarys,ray,surface,px,distance,False,ref,sourceColor,intensidades,0,colores, puntosPintados) #distancia total en cero
                    



    def PathTracing(self,boundarys,ray,surface,px,distance,reflejo,ref,sourceColor,intensidades, totalDistance, colores, puntosPintados, numRebote = 0): 

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

            colorBleeding = [sourceColor[0], sourceColor[1], sourceColor[2]]

            if interBound.especularidad:
                pointFinal = self.getReflectionVectorEspejo(ray, interBound, dx, dy, distance)
            else:
                pointFinal = self.getReflectionVector(ray,interBound,500,500,distance)
                colorBleeding = self.get_color(ref[int(pInterseccion.x)][int(pInterseccion.y)], sourceColor)

            rayRebote = Line(pInterseccion.x,pInterseccion.y,pointFinal.x,pointFinal.y)
            self.PathTracing(boundarys,rayRebote,surface,px,distance,True,ref,colorBleeding,intensidades,ray.distance()+totalDistance, colores, puntosPintados, numRebote+1)
                                                           #entre más grande más iluminado, le damos 1000         
        self.pintarRayo(ray.Point1, ray.Point2, surface, px,707,reflejo,ref,sourceColor,intensidades,totalDistance, colores, puntosPintados, numRebote)



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
        im_file = Image.open("fondoMazmorraVerde.png")
        ref = np.array(im_file)
        ref2 = np.array(im_file)
         
        for i in range(500):
            for j in range(500):
                ref[i][j]=ref2[j][i]




        i = Image.new("RGB", (500, 500), (0, 0, 0) )
        ph = np.array(i)
        px = np.array(i)


        

        #sources = [FuenteDeLuz(50, 50, (255,255,255)),FuenteDeLuz(100, 50, (255,255,255))]
        #sources = [FuenteDeLuz(373, 224, (150,0,0)),FuenteDeLuz(220, 448, (0,0,150)),FuenteDeLuz(128, 133, (255,255,255))]        
        # boundarys = [Line(200,400,450,400),Line(200,100,450,100),Line(200,100,200,400),Line(400,100,400,400)]
        #boundarys = [Borde(200,99,200,401,False),Borde(400,99,400,401,False),Borde(0,100,401,100,False),Borde(0,400,401,400,False)]
        #boundarys = [Borde(200,200,400,200,False), Borde(200,400,400,400,False), Borde(200,200,200,400,False), Borde(400,200,400,400,False)]
        '''
        boundarys = [Borde(303, 146, 325, 146, True),
                    Borde(14, 23, 173, 23, True), 
                    Borde(14, 23, 14, 256, True), 
                    Borde(14, 256, 77, 256, True), 
                    Borde(77, 256, 77,483, True),  
                    Borde(77,483, 362, 483, True), 
                    Borde(362, 333, 362, 483, True), 
                    Borde(362, 333, 488, 333, True), 
                    Borde(488, 23, 488, 333, True), 
                    Borde(267, 23, 488, 23, True), 
                    Borde(267, 23, 267, 248, True), 
                    Borde(267, 248, 267, 369, True),
                    Borde(173, 248, 173,369 , True),
                    Borde(173, 23, 173, 248, True), 
                    Borde(173, 248, 267, 248, True)]
        '''

        sources = [FuenteDeLuz(86, 358, (210,85,20)),FuenteDeLuz(161, 358, (210,150,20)),FuenteDeLuz(411, 226, (210,85,20)),FuenteDeLuz(362, 33, (230,230,50))]
        #sources = [FuenteDeLuz(86, 358, (255,255,255)),FuenteDeLuz(161, 358, (255,255,255)),FuenteDeLuz(411, 226, (255,255,255)),FuenteDeLuz(362, 33, (255,255,255))]

        boundarys = [Borde(69, 325, 69, 500, False),
                    Borde(69, 325, 94, 325, False),
                    Borde(94, 325, 94, 58, False),
                    Borde(94, 58, 219, 58, False),
                    Borde(219, 58, 219, 25, False),
                    Borde(219, 25, 319, 25, False),
                    Borde(319, 25, 319, 0, False),
                    Borde(405, 0, 405, 25, False),
                    Borde(405, 25, 499, 25, False),
                    Borde(180, 500, 180, 325, False),
                    Borde(180, 325, 156, 325, False),
                    Borde(156, 325, 156, 241, False),
                    Borde(156, 241, 219, 241, False),
                    Borde(219, 241, 219, 474, False),
                    Borde(219, 474, 499, 474, False),
                    Borde(230, 307, 319, 307, False),
                    Borde(319, 307, 319, 358, False),
                    Borde(230, 307, 230, 358, False),
                    Borde(230, 358, 319, 358, False),
                    Borde(405, 307, 499, 307, False),
                    Borde(405, 307, 405, 358, False),
                    Borde(405, 358, 499, 358, False),
                    Borde(280, 141, 319, 141, False),
                    Borde(319, 141, 319, 192, False),
                    Borde(280, 141, 280, 192, False),
                    Borde(280, 192, 319, 192, False),
                    Borde(405, 141, 444, 141, False),
                    Borde(444, 141, 444, 192, False),
                    Borde(405, 141, 405, 192, False),
                    Borde(405, 192, 444, 192, False),
                    Borde(121, 347, 145, 347, True)
                    ]


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