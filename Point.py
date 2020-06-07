

import numpy as np 
import pygame
import math


class Point:
    x=0.0
    y=0.0

    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __add__(self, other):
        

        return Point(self.x+other.x, self.y+other.y)
    
    def dot(self, p2):
        return (self.x*p2.x) + (self.y*p2.y)

    def cross(self, p2):
        return (self.x*p2.y) - (self.y*p2.x)

        
    def __str__(self):
        return "[ {}, {}]".format(self.x, self.y) 


    def draw(self, surface):
        pygame.draw.circle(surface, (40,200,200),(self.x,self.y),5,0)


    def distance(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
    
print(Point(2,4)+Point(8,9))