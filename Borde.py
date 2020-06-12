from Line import *
import numpy as np 
import pygame

class Borde:
    Line = Line(0,0,0,0)
    especularidad = False

    def __init__(self, x1, y1, x2, y2, _especularidad):
        self.Line.Point1 =  Point(x1, y1)
        self.Line.Point2 =  Point(x2, y2)
        self.especularidad = _especularidad   