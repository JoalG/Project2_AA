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
        


    def pintarRayo(self, source, point, surface, px,intence,reflejo,ref,sourceColor,intensidades, totalDistance, colores, puntosPintados, numRebote, espejo): 

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
                        intesity = self.getLimitedIntensity(intensidades, intesity, max(intensidades[pixelPosX][pixelPosY], 0.8), pixelPosX, pixelPosY)
                        if colores[pixelPosX][pixelPosY] == [0,0,0]:
                            self.pintarPuntoPrimeraVez(px, ref, colores, sourceColor, pixelPosX, pixelPosY, intesity)
                        else:
                            self.pintarPuntoRecurente(px, ref, colores, sourceColor, pixelPosX, pixelPosY, intesity)

                        puntosPintados[pixelPosX][pixelPosY][0] = True
                        intensidades[pixelPosX][pixelPosY] = intesity        
            
                else:

                    if not espejo:
                        intesity = self.getLimitedIntensity(intensidades, intesity, max(intensidades[pixelPosX][pixelPosY], 0.8), pixelPosX, pixelPosY)
                    else:
                        intesity = 1

                    if numRebote <= 3:
                        if not puntosPintados[pixelPosX][pixelPosY][numRebote]:
                            if colores[pixelPosX][pixelPosY] == [0,0,0]:                      
                                self.pintarPuntoPrimeraVez(px, ref, colores, sourceColor, pixelPosX, pixelPosY, intesity)
                            else:
                                self.pintarPuntoRecurente(px, ref, colores, sourceColor, pixelPosX, pixelPosY, intesity)
                            
                            if not puntosPintados[pixelPosX][pixelPosY][1]:
                                puntosPintados[pixelPosX][pixelPosY][1] = True
                            elif not puntosPintados[pixelPosX][pixelPosY][2]:
                                puntosPintados[pixelPosX][pixelPosY][2] = True
                            else:
                                puntosPintados[pixelPosX][pixelPosY][3] = True
                        elif espejo:
                            px[pixelPosX][pixelPosY]=px[pixelPosX][pixelPosY][:3]*intesity
                        intensidades[pixelPosX][pixelPosY] = intesity
         
    def getLimitedIntensity(self, intensidades, intesity, maxIntesity, pixelPosX, pixelPosY):
        intesity += intensidades[pixelPosX][pixelPosY]
        if(intesity > maxIntesity):
            intesity = maxIntesity
        return intesity        

    def pintarPunto(self, px, ref, color, pixelPosX, pixelPosY, intesity):
        px[pixelPosX][pixelPosY]=ref[pixelPosX][pixelPosY][:3]*intesity
        px[pixelPosX][pixelPosY][0] *= (color[0]/255)
        px[pixelPosX][pixelPosY][1] *= (color[1]/255)
        px[pixelPosX][pixelPosY][2] *= (color[2]/255)       

    def pintarPuntoPrimeraVez(self, px, ref, colores, color, pixelPosX, pixelPosY, intesity):
        self.pintarPunto(px, ref, color, pixelPosX, pixelPosY, intesity)
        colores[pixelPosX][pixelPosY] = [color[0],color[1],color[2]]
                
    def pintarPuntoRecurente(self, px, ref, colores, color, pixelPosX, pixelPosY, intesity):
        combinedColors = self.get_color(colores[pixelPosX][pixelPosY], color)
        colores[pixelPosX][pixelPosY] = combinedColors

        r = combinedColors[0]
        g = combinedColors[1]
        b = combinedColors[2]

        self.pintarPunto(px, ref, [r, g, b], pixelPosX, pixelPosY, intesity)

    def get_color(self, colorRGBA1, colorRGBA2):
        red   = (colorRGBA1[0] + colorRGBA2[0]) / 2
        green = (colorRGBA1[1] + colorRGBA2[1]) / 2
        blue  = (colorRGBA1[2] + colorRGBA2[2]) / 2
        return [int(red), int(green), int(blue)]

    def iluminar(self,sources,px,boundarys,surface,gMin, gMax, ref):
        #Solo funciona con una fuente de Luz
        startTime = time.time()

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
        
        puntosPintadosPorSource = []
        for source in sources :
            
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

            
            puntosPintadosPorSource += [puntosPintados]
             
        
        for j in range(gMax*9):
        
            distancia = random.uniform(300,400)
            direccion = random.uniform(0,360)
            
          
            for k in range(len(sources)):
                source = sources[k]
                puntosPintados = puntosPintadosPorSource[k]
                sourceColor = list(source.color)
                point = Point(source.Fuente.x + math.cos(math.radians(direccion))*distancia, source.Fuente.y + math.sin(math.radians(direccion))*distancia)
                
    
                        
                point.x = (point.x)
                point.y = (point.y)
                ray = Line(source.Fuente.x,source.Fuente.y,point.x,point.y)
                distance = source.Fuente.distance(point)

                self.PathTracing(boundarys,ray,surface,px,distance,False,ref,sourceColor,intensidades,0,colores, puntosPintados,0) #distancia total en cero
                    
        print(time.time()-startTime)


    def PathTracing(self,boundarys,ray,surface,px,distance,reflejo,ref,sourceColor,intensidades, totalDistance, colores, puntosPintados, numRebote, espejo = False): 
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
            if numRebote < 3:
                self.PathTracing(boundarys,rayRebote,surface,px,distance,True,ref,colorBleeding,intensidades,ray.distance()+totalDistance, colores, puntosPintados, numRebote+1, interBound.especularidad)
                                                           #entre más grande más iluminado, le damos 1000         
        self.pintarRayo(ray.Point1, ray.Point2, surface, px,707,reflejo,ref,sourceColor,intensidades,totalDistance, colores, puntosPintados, numRebote, espejo)



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

        #sources = [FuenteDeLuz(86, 358, (210,85,20)),FuenteDeLuz(411, 226, (210,85,20)),FuenteDeLuz(362, 33, (255,255,255)), FuenteDeLuz(150, 150, (210,85,20)),  FuenteDeLuz(160, 160, (210,85,20)), FuenteDeLuz(440, 440, (255,255,255))]     #,FuenteDeLuz(161, 358, (210,150,20))
        sources = [FuenteDeLuz(86, 358, (210,85,20)),FuenteDeLuz(411, 226, (210,85,20)),FuenteDeLuz(362, 33, (255,255,255))] 

        boundarys = [Borde(74, 499, 74, 332, False),
                    Borde(74, 332, 100, 332, False),
                    Borde(100, 332, 100, 66, False),
                    Borde(100, 66, 224, 66, False),
                    Borde(224, 66, 224, 32, False),
                    Borde(224, 32, 324, 32, False),
                    Borde(324, 32, 324, 0, False),
                    Borde(399, 0, 399, 32, False),
                    Borde(399, 32, 499, 32, False),
                    Borde(175, 499, 175, 332, False),
                    Borde(175, 332, 150, 332, False),
                    Borde(150, 332, 150, 233, False),
                    Borde(150, 233, 224, 233, False),
                    Borde(224, 233, 224, 467, False),
                    Borde(224, 467, 499, 467, False),
                    Borde(224, 300, 324, 300, False),
                    Borde(324, 300, 324, 366, False),
                    Borde(324, 366, 224, 366, False),
                    Borde(499, 300, 399, 300, False),
                    Borde(399, 300, 399, 366, False),
                    Borde(399, 366, 499, 366, False),
                    Borde(275, 133, 324, 133, False),
                    Borde(324, 133, 324, 199, False),
                    Borde(275, 133, 275, 199, False),
                    Borde(275, 199, 324, 199, False),
                    Borde(399, 133, 450, 133, False),
                    Borde(450, 133, 450, 199, False),
                    Borde(399, 133, 399, 199, False),
                    Borde(399, 199, 450, 199, False),
                    Borde(324, 32, 324, 133, True)
                    ]

        first= True
        done = False
        
        
        while not done:
            #print("f")
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        

            screen.fill((255, 255, 255))
            # Convert to a surface and splat onto screen offset by border width and height
            npimage=(px)
            surface = pygame.surfarray.make_surface(npimage)
            #b = Boundary(350,100,350,400)
    
            if first:
                t = threading.Thread(target = self.iluminar, args=(sources,px,boundarys,surface,0,360,ref) ) # f being the function that tells how the ball should move
                t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
                t.start()
                first=False



                
            screen.blit(surface, (border, border))
            pygame.display.flip()
        
      
        
p = PathTracing()
p.main()