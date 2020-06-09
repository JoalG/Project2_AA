from Point import *
import numpy as np 
import pygame



class Line:
    Point1 =  Point(0,0)
    Point2 =  Point(0,0)

    def __init__(self, x1, y1, x2, y2):
        self.Point1 =  Point(x1, y1)
        self.Point2 =  Point(x2, y2)


    def draw(self,surface ):
        pygame.draw.line(surface, (40,200,200), (self.Point1.x, self.Point1.y), (self.Point2.x, self.Point2.y), 3)
    
    def __str__(self):
        return "[ {}, {}]".format(self.Point1.x, self.Point1.y)

    
    def distance(self):
        return math.sqrt((self.Point1.x-self.Point2.x)**2 + (self.Point1.y-self.Point2.y)**2)

    
    #Formula para determinar si existe una interseccion entre 2 lineas
    def instersect(self, other):
        x1 = self.Point1.x
        y1 = self.Point1.y
        x2 = self.Point2.x
        y2 = self.Point2.y
        x3 = other.Point1.x
        y3 = other.Point1.y
        x4 = other.Point2.x
        y4 = other.Point2.y

        denominator = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

        if(denominator==0):
           
            return False

        t = (((x1-x3)*(y3-y4))-((y1-y3)*(x3-x4)))/denominator
 
        u = -1*(((x1-x2)*(y1-y3))-((y1-y2)*(x1-x3)))/denominator

        if( t>0 and t<1 and u>0 and u<1):

            return True
        else:
            
            return False

    
    
    #Formula para calcular la interseccion de 2 lineas , si no existe se cae /0
    def calcInstersect(self, other):
        x1 = self.Point1.x
        y1 = self.Point1.y
        x2 = self.Point2.x
        y2 = self.Point2.y
        x3 = other.Point1.x
        y3 = other.Point1.y
        x4 = other.Point2.x
        y4 = other.Point2.y

        denominator = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

        t = (((x1-x3)*(y3-y4))-((y1-y3)*(x3-x4)))/denominator

        xIntersection = x1+t*(x2-x1)
        yIntersection = y1+t*(y2-y1)

        return Point(xIntersection,yIntersection)


    # O = vertical 1 = horizontal , 2 creciente, 3 decreciente 
    def orientacion(self):

        if(self.Point1.x == self.Point2.x):
            return 0
        if(self.Point1.y == self.Point2.y):
            return 1
        if(self.Point1.x < self.Point2.x):
            if(self.Point1.y < self.Point2.y):
                return 2
            else:
                return 3
        else:
            if(self.Point1.y > self.Point2.y):
                return 2
            else:
                return 3
    


    
    def cambioX (self):
        xC=(self.Point2.x-self.Point1.x)/(self.Point1.distance(self.Point2))
        return xC

    def cambioY (self):
        yC=(self.Point2.y-self.Point1.y)/(self.Point1.distance(self.Point2))
        return yC















 
