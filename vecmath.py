"""A wrapper for NumPy functions"""
import numpy as np
import math

epsilon = 1e-7 # An arbitrary small distance -- use for floating comparison
pi = math.pi

def vector(*components):
  return np.array(components)

norm = np.linalg.norm
dot = np.dot
cross = np.cross
abs = np.vectorize(math.fabs)

# wrap index lookups in case arrays aren't used down the road
getX = lambda self: self[0]
getY = lambda self: self[1]
getZ = lambda self: self[2]

# surprisingly, numpy doesn't implement this
def normalized(vec):
  return vec/norm(vec)

def quantize(x):
  """convert a float in [0,1] to an int in [0,255]"""
  y = math.floor(x*255)
  return y if y<256 else 255
quantize = np.vectorize(quantize)

#####
# experimental: will be used for transform code

def transformPoint(matrix, point):
  return (matrix*np.matrix(np.append(point, 1)).T).A.flatten()[:2]

def transformVector(matrix, vector):
  return (matrix*np.matrix(np.append(point, 0)).T).A.flatten()[:2]


def identityM():
  return np.matrix([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [0,0,0,1]])

def translateM(a,b,c):
  return np.matrix([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [a,b,c,1]])
