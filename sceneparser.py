"""A parser to read scene description files"""
__all__ = ['Configuration', 'parseFile']
import inspect
import sceneobject
import camera
import light
import material
from vecmath import *

class Configuration:
  def __init__(self):
    self.background_color = vector(0,0,0)
    self.ambient_light = vector(0.1,0.1,0.1)

def parseFile(infile):
  config = Configuration()
  tokens = getTokens(infile)
  for token in tokens:
    if token == 'Settings':
      settings = parseClassArgs(zip(*inspect.getmembers(config))[0], getBlock(tokens))
      for k,v in settings.iteritems():
        setattr(config, k, v)
    elif token == 'Camera':
      config.camera = parseModule(camera, concatGenerators([next(tokens)], '{', getBlock(tokens), '}'))[0]
    elif token == 'Lights':
      config.lights = parseModule(light, getBlock(tokens))
    elif token == 'Materials':
      config.materials = parseModule(material, getBlock(tokens), True)
    elif token == 'Scene':
      config.scene = sceneobject.Group(parseModule(sceneobject, getBlock(tokens), False, ['Group']))
      setMaterials(config.scene, config.materials)
    else:
      raise ValueError('Top-level command '+token+' not recognized')
  return config

def setMaterials(scene, materials):
  for obj in scene.objects:
    if hasattr(obj, 'material'):
      obj.material = materials[obj.material]
    elif hasattr(obj, 'objects'):
      setMaterials(obj, materials)

def parseModule(module, tokens, named=False, recursiveTypes=[]):
  instances = {} if named else []
  classes = {name:obj for name,obj in inspect.getmembers(module, inspect.isclass)}
  for token in tokens:
    if token in recursiveTypes:
      classobj = classes[token]
      instances.append(classobj(parseModule(module, getBlock(tokens), False, recursiveTypes)))
    elif token in classes:
      if named:
        instanceName = next(tokens)
      classobj = classes[token]
      argnames = inspect.getargspec(classobj.__init__)[0]
      args = parseClassArgs(argnames, getBlock(tokens))
      if named:
        instances[instanceName] = classobj(**args)
      else:
        instances.append(classobj(**args))
  return instances
      
def parseClassArgs(argnames, tokens):
  d = {}
  for token in tokens:
    if token in argnames:
      arg = token
      d[arg] = []
    else:
      d[arg].append(token)
  return parseArgDict(d)

def parseArgDict(d):
  for key in d:
    values = d[key]
    try:
      if len(values) == 1:
        d[key] = float(values[0])
      elif len(values) >= 3:
        d[key] = vector(*[float(v) for v in values])
    except ValueError:
      d[key] = values[0] # Just leave it as a string
  return d

def concatGenerators(*gens):
  for gen in gens:
    for x in gen:
      yield x

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
