from vecmath import *
from ray import Ray

class Camera:
    tmin = 0.0
    def generateRay(self, point):
        raise NotImplementedError

class PerspectiveCamera(Camera):
    def __init__(self, location, forward, up, angle=90.0, aspect=1.0):
        self.location = location
        self.forward = normalized(forward)
        self.up = normalized(up - dot(up, self.forward)*self.forward)
        self.right = cross(self.forward, self.up)
        self.field_of_view = pi*angle/180.0
        self.aspect = aspect
        d = 1.0 / math.tan(field_of_view/2.0) # distance to image plane
        self.center = d*self.forward # relative location of center of image plane
    def generateRay(self, point):
        return Ray(self.location, normalized(self.center + self.right*getX(point) + self.up*aspect*getY(point)))

