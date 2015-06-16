from sceneobject import *
from material import *
from light import *
from camera import *
from ray import *
from vecmath import *
from sceneparser import *
import argparse
import Image

def main():
  cmd_args = getArguments()
  xres, yres = cmd_args.res
  config = parseFile(cmd_args.infile)
  if isinstance(config.camera, PerspectiveCamera):
    config.camera.aspect = yres/float(xres)
  array = np.zeros((yres, xres, 3))
  for i,x in enumerate(np.linspace(-1, 1, xres)):
    for j,y in enumerate(np.linspace(1, -1, yres)):
      ray = config.camera.generateRay(vector(x,y))
      hit = config.scene.intersect(ray, 0)
      if hit == None:
        array[j][i] = config.background_color
      else:
        t, material, normal = hit
        array[j][i] = material.shade(t, ray, normal, config.lights[0])
  write_image(array, cmd_args.o)

def getArguments():
  """Use argparse to get the command-line arguments"""
  parser = argparse.ArgumentParser(description='A simple raytracer')
  parser.add_argument('infile', help='The input file path. The input file describes the scene to be raytraced.')
  parser.add_argument('-o', help='The output image file path.')
  parser.add_argument('-res', nargs=2, help='Output resolution.', metavar=('x','y'), type=int, default=[200,200])
  return parser.parse_args()

def write_image(array, outfile=None):
  """Use PIL to output NumPy array as image."""
  if outfile == None:
    Image.fromarray(quantize(array).astype(np.uint8)).show() # use show() for debugging
                                                             # may not work on all platforms
  else:
    Image.fromarray(quantize(array).astype(np.uint8)).save(outfile)

if __name__ == '__main__':
  main()
