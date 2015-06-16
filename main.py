from sceneobject import *
from material import *
from light import *
from camera import *
from ray import *
from vecmath import *
from sceneparser import *
import Image

def main():
  config = parseFile('bluesphere.scene')
  array = np.zeros((200, 200, 3))
  for i,x in enumerate(np.linspace(-1, 1, 200)):
    for j,y in enumerate(np.linspace(1, -1, 200)):
      ray = config.camera.generateRay(vector(x,y))
      hit = config.scene.intersect(ray, 0)
      if hit == None:
        array[j][i] = vector(0,0,0)
      else:
        t, material, normal = hit
        array[j][i] = material.shade(t, ray, normal, config.lights[0])
  write_image(array)

def write_image(array, outfile=None):
  """Use PIL to output NumPy array as image."""
  if outfile == None:
    Image.fromarray(quantize(array).astype(np.uint8)).show() # use show() for debugging
                                                             # may not work on all platforms
  else:
    Image.fromarray(quantize(array).astype(np.uint8)).save(outfile)

if __name__ == '__main__':
  main()
