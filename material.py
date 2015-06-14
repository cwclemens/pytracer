"""Materials describe how light interacts with objects."""
from vecmath import *
from light import *

class Material:
  """Abstract Material class"""

  def shade(self, t, ray, normal, light):
    """All material types must implement a shader"""
    raise NotImplementedError

class ConstantShader(Material):
  """Simple uniform shading"""

  def __init__(self, color):
    self.color = color

  def shade(self, t, ray, normal, light):
    return self.color
    

class PhongDiffuse(Material):
  """Implements the diffuse component of the Phong model"""

  def __init__(self, diffuse_color):
    self.diffuse_color = diffuse_color

  def shade(self, t, ray, normal, light):
    hitPos = ray.evaluate(t)
    illumination, lightPos = light.sample(hitPos)
    vecToLight = lightPos-hitPos # TODO: cast shadow rays
    distToLight = norm(vecToLight)
    dirToLight = vecToLight / distToLight
    d = dot(dirToLight, normal) # shade proportional to cosine (i.e. Phong diffuse)
    d = d if d > 0 else 0.0 # clamp d above zero -- only shade if facing light
    return d*illumination*self.diffuse_color + 0.1*self.diffuse_color
