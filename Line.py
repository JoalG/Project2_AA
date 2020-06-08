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

    def instersect(self, other):
        x1 = self.Point1.x
        y1 = self.Point1.y
        x2 = self.Point2.x
        y2 = self.Point2.y
        x3 = other.Point1.x
        y3 = other.Point1.y
        x4 = other.Point2.x
        y4 = other.Point2.y


        

        d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

        if(d==0):
            print("ohhh")
            return False



        t = (((x1-x3)*(y3-y4))-((y1-y3)*(x3-x4)))/d
 

        u = -1*(((x1-x2)*(y1-y3))-((y1-y2)*(x1-x3)))/d



        if( t>0 and t<1 and u>0 and u<1):

            return True
        else:
            
            return False






 
