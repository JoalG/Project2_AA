from Line import *
import numpy as np 
import pygame

class Borde:
    line = Line(0,0,0,0)

    especularidad = False

    def __init__(self, x1, y1, x2, y2, _especularidad):
        self.line = Line(x1, y1, x2, y2)
        self.especularidad = _especularidad   


    def draw(self,surface):
        self.line.draw(surface)
        