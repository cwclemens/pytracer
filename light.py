"""Lights represent the sources of light in a scene."""
from vecmath import *

class Light:
  """Abstract Light class"""

  def __init__(self, intensity):
    """Virtual constructor"""
    self.intensity = intensity

  def sample(self, viewerPos):
    """All lights allow sampling the illumination at a location"""
    raise NotImplementedError

  def distanceLaw(self, dist):
    """Computes the intensity at a distance from the source"""
    return self.intensity/(0.05*dist**2 + 3)


class PointLight(Light):
  """Represents a point source of light."""

  def __init__(self, location, intensity, color=vector(1,1,1)):
    self.color = color
    self.location = location
    Light.__init__(self, intensity)

  def sample(self, viewerPos):
    return (self.color*self.distanceLaw(norm(self.location-viewerPos)), self.location)


