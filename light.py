

class Light:
  def sample(self):
    raise NotImplementedError

class PointLight(Light):
  def __init__(self, color, location):
    self.color = color
    self.location = location
  def sample(self):
    return (self.color, self.location)
