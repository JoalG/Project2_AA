from Point import *

class FuenteDeLuz :
    Fuente = Point(0,0)
    color = (0,0,0)

    def __init__(self, x , y, _color, _intensidad):
        self.Fuente = Point(x, y)
        self.color = [_color[0]*_intensidad, _color[1]*_intensidad, _color[2]*_intensidad]

    def draw(self,surface):
        self.Fuente.draw(surface,self.color)