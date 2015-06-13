import numpy as np
import math

epsilon = 1e-7
pi = math.pi

vector = np.array
norm = np.linalg.norm
dot = np.dot
cross = np.cross

getX = lambda self: self[0]
getY = lambda self: self[1]
getZ = lambda self: self[2]

def normalized(vec):
  s = vec.sum()
  if s > epsilon:
    return vec / s

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
