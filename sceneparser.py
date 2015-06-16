"""A rough and simple parser to read scene description files"""
__all__ = ['Configuration', 'parseFile']
from vecmath import *
from sceneobject import *
from camera import *
from light import *
from material import *

class Configuration:
  def __init__(self):
    self.background_color = vector(0,0,0)
    self.ambient_light = vector(0.1,0.1,0.1)
  def isValid(self):
    try:
      return all([self.camera != None,
                  self.lights != None,
                  self.scene != None,
                  self.background_color != None,
                  self.ambient_light != None])
    except NameError:
      return False

def parseFile(infile):
  config = Configuration()
  tokens = getTokens(infile)
  for token in tokens:
    if token == 'PerspectiveCamera':
      config.camera = parsePerspectiveCamera(getBlock(tokens))
    elif token == 'Lights':
      config.lights = parseLights(getBlock(tokens))
    elif token == 'Materials':
      config.materials = parseMaterials(getBlock(tokens))
    elif token == 'Scene':
      config.scene = parseScene(config.materials, getBlock(tokens))
    elif token == 'Settings':
      parseSettings(config, getBlock(tokens))
    else:
      raise ValueError('Top-level command '+token+' not recognized')
  return config

def getTokens(infile):
  with open(infile, 'r') as file:
    for line in file:
      for token in line.split():
        yield token

def getBlock(tokens):
  try:
    if next(tokens) == '{':
      i = 1
      while i > 0:
        token = next(tokens)
        if token == '{':
          i += 1
          yield token
        elif token == '}' and i == 1:
          i -= 1
        elif token == '}':
          i -= 1
          yield token
        else:
          yield token
    else:
      raise ValueError('Expected block, no opening bracket found')
  except StopIteration:
    raise ValueError('Ran out of tokens before completing block')

def parseVector(tokens):
  x = parseFloat(tokens)
  y = parseFloat(tokens)
  z = parseFloat(tokens)
  return vector(x,y,z)

def parseFloat(tokens):
  try:
    return float(next(tokens))
  except ValueError:
    raise ValueError('Expected float, could not parse')

def parseInt(tokens):
  try:
    return int(next(tokens))
  except ValueError:
    raise ValueError('Expected int, could not parse')

def parsePerspectiveCamera(tokens):
  angle = 90.0
  aspect = 1.0
  for token in tokens:
    if token == 'location':
      location = parseVector(tokens)
    elif token == 'forward':
      forward = parseVector(tokens)
    elif token == 'up':
      up = parseVector(tokens)
    elif token == 'angle':
      angle = parseFloat(tokens)
    elif token == 'aspect':
      aspect = parseFloat(tokens)
  try:
    return PerspectiveCamera(location, forward, up, angle, aspect)
  except NameError:
    raise ValueError('Failed to parse PerspectiveCamera')

def parseLights(tokens):
  lights = []
  try:
    for token in tokens:
      if token == 'PointLight':
        color = vector(1,1,1)
        toks = getBlock(tokens)
        for tok in toks:
          if tok == 'location':
            location = parseVector(toks)
          elif tok == 'color':
            color = parseVector(toks)
        lights.append(PointLight(location, color))
  except NameError:
    raise ValueError('Failed to parse light')
  return lights

def parseMaterials(tokens):
  materials = []
  try:
    for token in tokens:
      if token == 'ConstantShader':
        toks = getBlock(tokens)
        for tok in toks:
          if tok == 'color':
            color = parseVector(toks)
        materials.append(ConstantShader(color))
      elif token == 'PhongDiffuse':
        toks = getBlock(tokens)
        for tok in toks:
          if tok == 'diffuse_color':
            color = parseVector(toks)
        materials.append(PhongDiffuse(color))
  except NameError:
    raise ValueError('Failed to parse material')
  return materials
    
def parseScene(materials, tokens):
  objects = []
  for token in tokens:
    if token == 'Sphere':
      toks = getBlock(tokens)
      for tok in toks:
        if tok == 'center':
          center = parseVector(toks)
        elif tok == 'radius':
          radius = parseFloat(toks)
        elif tok == 'material_idx':
          material = materials[parseInt(toks)]
      objects.append(Sphere(radius, center, material))
    elif token == 'Plane':
      toks = getBlock(tokens)
      for tok in toks:
        if tok == 'origin':
          origin = parseVector(toks)
        elif tok == 'normal':
          normal = parseVector(toks)
        elif tok == 'material_idx':
          material = materials[parseInt(toks)]
      objects.append(Plane(normal, origin, material))
    elif token == 'Triangle':
      toks = getBlock(tokens)
    elif token == 'Group':
      objects.append(parseScene(getBlock(tokens)))
    elif token == 'Transform':
      toks = getBlock(tokens)
  return Group(objects)

def parseSettings(config, tokens):
  backgroud_color = vector(0,0,0)
  ambient_light = vector(0.1,0.1,0.1)
  for token in tokens:
    if token == 'background_color':
      config.background_color = parseVector(tokens)
    elif token == 'ambient_light':
      config.ambient_light = parseVector(tokens)

