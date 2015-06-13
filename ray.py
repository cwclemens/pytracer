from vecmath import *

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    def evaluate(self, t):
        return self.origin + self.direction*t

