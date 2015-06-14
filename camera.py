"""Cameras create rays in the object space when given points the image space."""
from vecmath import *
from ray import Ray

class Camera:
    """Abstract camera class."""
    tmin = 0.0 # minimum distance for ray intersection. may be overridden.

    def generateRay(self, point):
        raise NotImplementedError


class PerspectiveCamera(Camera):
    """Camera that uses a flat image plane."""

    def __init__(self, location, forward, up, angle=90.0, aspect=1.0):
        self.location = location
        self.forward = normalized(forward)
        self.up = normalized(up - dot(up, self.forward)*self.forward)
        self.right = cross(self.forward, self.up)
        self.field_of_view = pi*angle/180.0
        self.aspect = aspect
        d = 1.0 / math.tan(self.field_of_view/2.0) # distance to image plane
        self.center = d*self.forward # **relative** location of center of image plane

    def generateRay(self, point):
        return Ray(self.location, normalized(self.center + self.right*getX(point) + self.up*self.aspect*getY(point)))

