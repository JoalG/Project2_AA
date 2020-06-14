from Point import *

class FuenteDeLuz :
    Fuente = Point(0,0)
    color = (0,0,0)

    def __init__(self, x , y, _color):
        self.Fuente = Point(x, y)
        self.color = _color

    def draw(self,surface):
        self.Fuente.draw(surface,self.color)