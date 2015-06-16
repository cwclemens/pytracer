"""Lights represent the sources of light in a scene."""
from vecmath import *

class Light:
  """Abstract Light class"""

  def sample(self, viewerPos):
    """All lights allow sampling the illumination at a location"""
    raise NotImplementedError


class PointLight(Light):
  """Represents a point source of light."""

  def __init__(self, location, color=vector(1,1,1)):
    self.color = color
    self.location = location

  def sample(self, viewerPos):
    return (self.color, self.location)


