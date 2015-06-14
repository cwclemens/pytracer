from vecmath import *

class SceneObject:
  def intersect(self, ray, tmin):
    raise NotImplementedError

class Sphere(SceneObject):
  def __init__(self, radius, center, material):
    self.radius = radius
    self.center = center
    self.material = material
  def intersect(self, ray, tmin):
    Ro = ray.origin - self.center
    Rd = ray.direction
    a = norm(Rd)**2
    b = 2*dot(Rd,Ro)
    c = norm(Ro)**2 - self.radius**2
    d = b**2 - 4*a*c
    if d <= 0:
      return None
    d = d**0.5
    try:
      t = min(x for x in ((-b+d)/(2*a), (-b-d)/(2*a)) if x >= tmin)
    except ValueError:
      return None # neither root is greater than tmin
    return (t, self.material, normalized(Ro+Rd*t))


class Plane(SceneObject):
  def __init__(self, normal, origin, material):
    self.normal = normalized(normal)
    self.origin = origin
    self.material = material
  def intersect(self, ray, tmin):
    det = dot(ray.direction, self.normal)
    if abs(det) < epsilon:
      return None # ray is parallel to plane
    dist = dot(ray.origin - self.origin, self.normal)
    t = -dist / det
    if t > tmin:
      return (t, self.material, self.normal if dist > 0 else -self.normal)

class Triangle(SceneObject):
  def __init__(self, a, b, c, material):
    self.a, self.b, self.c = a, b, c
    self.na = self.nb = self.nc = normalized(cross(b-a, c-a))
    self.material = material
  def __init__(self, a, b, c, na, nb, nc, material):
    self.a, self.b, self.c = a, b, c
    self.na, self.nb, self.nc = normalized(na), normalized(nb), normalized(nc)
    self.material = material

class Group(SceneObject):
  def __init__(self, objects):
    self.objects = objects

class Transformation(SceneObject):
  def __init__(self, matrix, obj):
    self.object = obj
    self.M = matrix
