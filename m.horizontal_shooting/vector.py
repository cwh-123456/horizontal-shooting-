class Vector(tuple):
    def __init__(self, xy):
        '''实现位置的移动'''
        self.x, self.y = xy

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return tuple(self.x, self.y)