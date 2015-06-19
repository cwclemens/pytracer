"""Object primitives and data structures to describe a scene"""
from vecmath import *

class SceneObject:
  """Abstract base class"""

  def intersect(self, ray, tmin):
    """All scene objects must compute ray intersection, returning 
    (distance_along_ray, material_at_intersection, surface_normal)
    """
    raise NotImplementedError


class Sphere(SceneObject):
  """Simple sphere representation"""

  def __init__(self, radius, center, material):
    self.radius = radius
    self.center = center
    self.material = material

  def intersect(self, ray, tmin):
    Ro = ray.origin - self.center
    Rd = ray.direction
    a = norm(Rd)**2 # a,b,c are the coefficients of a quadratic
    b = 2*dot(Rd,Ro)
    c = norm(Ro)**2 - self.radius**2
    d = b**2 - 4*a*c # determinant
    if d <= 0:
      return None
    d = d**0.5
    try:
      t = min(x for x in ((-b+d)/(2*a), (-b-d)/(2*a)) if x >= tmin)
    except ValueError:
      return None # neither root is greater than tmin
    return (t, self.material, normalized(Ro+Rd*t))


class Plane(SceneObject):
  """Point-normal representation of an infinite plane"""

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
  """A triangle represented by its vertices, and optionally, its vertex normals"""

  def __init__(self, a, b, c, material, na=None, nb=None, nc=None):
    self.a, self.b, self.c = a, b, c
    if all((na != None, nb != None, nc != None)):
      self.na, self.nb, self.nc = normalized(na), normalized(nb), normalized(nc)
    else:
      self.na = self.nb = self.nc = normalized(cross(b-a, c-a))
    self.material = material

  def intersect(self, ray, tmin):
    try:
      beta, gamma, t = np.linalg.solve(np.array([self.a-self.b, self.a-self.c, ray.direction]).T, (self.a-ray.origin)[np.newaxis].T)
    except np.linalg.LinAlgError:
      return None
    alpha = 1 - beta - gamma
    if t < tmin or alpha < 0 or beta < 0 or gamma < 0:
      return None
    return (t, self.material, alpha*self.na + beta*self.nb + gamma*self.nc)

class Group(SceneObject):
  """Represent a collection of SceneObjects -- makes SceneObject into a tree"""

  def __init__(self, objects):
    self.objects = objects

  def intersect(self, ray, tmin):
    hits = (obj.intersect(ray, tmin) for obj in self.objects)
    hits = (hit for hit in hits if hit != None)
    try:
      return min(hits, key=lambda h: h[0])
    except ValueError: # no hits
      return None

class Transformation(SceneObject): # TODO: transformation intersection code
  """Represent an affine transformation of scene objects"""

  def __init__(self, matrix, obj):
    self.object = obj
    self.M = matrix
