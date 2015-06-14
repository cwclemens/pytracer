

class Material:
  def shade(self, t, ray, lights):
    raise NotImplementedError

class ConstantShader(Material):
  def __init__(self, color):
    self.color = color
  def shade(self, t, ray, lights):
    return self.color
    
