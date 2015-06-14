from vecmath import *
from light import *

class Material:
  def shade(self, t, ray, normal, lights):
    raise NotImplementedError

class ConstantShader(Material):
  def __init__(self, color):
    self.color = color
  def shade(self, t, ray, normal, lights):
    return self.color
    
class PhongDiffuse(Material):
  def __init__(self, diffuse_color):
    self.diffuse_color = diffuse_color
  def shade(self, t, ray, normal, light):
    lightColor, lightPos = light.sample()
    hit = ray.evaluate(t)
    dirToLight = normalized(lightPos-hit)
    d = dot(dirToLight, normal)
    d = d if d > 0 else 0.0
    return d*lightColor*self.diffuse_color + 0.1*self.diffuse_color
