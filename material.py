"""Materials describe how light interacts with objects."""
from vecmath import *
from light import *
from ray import *

def clamp(x, pow=None):
  ret = x if x>0 else 0
  if pow != None and ret > 0:
    ret = ret**pow
  return ret

class Material:
  """Abstract Material class"""

  def shade(self, t, ray, normal, light, ambient_light=0.1):
    """All material types must implement a shader"""
    raise NotImplementedError

class ConstantShader(Material):
  """Simple uniform shading"""

  def __init__(self, color):
    self.color = color

  def shade(self, t, ray, normal, light, ambient_light=0.1):
    return self.color
    
class NormalVisualizer(Material):
  """Displays the components of the normal as colors"""

  def __init__(self):
    pass

  def shade(self, t, ray, normal, light, ambient_light=0.1):
    return abs(normal)

class PhongDiffuse(Material):
  """Implements the diffuse component of the Phong model"""

  def __init__(self, diffuse_color):
    self.diffuse_color = diffuse_color

  def shade(self, t, ray, normal, light, ambient_light=0.1):
    hitPos = ray.evaluate(t)
    lightColor, lightPos = light.sample(hitPos)
    vecToLight = lightPos-hitPos # TODO: cast shadow rays
    distToLight = norm(vecToLight)
    dirToLight = vecToLight / distToLight
    d = clamp(dot(dirToLight, normal)) # shade proportional to cosine (i.e. Phong diffuse)
    return d*lightColor*self.diffuse_color + 0.1*self.diffuse_color

class Phong(Material):
  """Implements the full Phong illumination model"""

  def __init__(self, diffuse_color, specular_color=vector(1,1,1), shininess=20, ambient_light=0.1):
    self.diffuse_color = diffuse_color
    self.specular_color = specular_color
    self.shininess = shininess

  def shade(self, t, ray, normal, light, ambient_light=0.1):
    hitPos = ray.evaluate(t)
    lightColor, lightPos = light.sample(hitPos)
    vecToLight = lightPos-hitPos # TODO: cast shadow rays
    distToLight = norm(vecToLight)
    dirToLight = vecToLight / distToLight
    reflect = 2*(ray.direction - dot(ray.direction, normal)*normal) - ray.direction 
    d = clamp(dot(dirToLight, normal))
    s = clamp(dot(dirToLight, reflect), self.shininess)
    pixel = ambient_light*self.diffuse_color # ambient light hack
    pixel += d*lightColor*self.diffuse_color # Diffuse component
    pixel += s*lightColor*self.specular_color # Specular component
    return pixel
