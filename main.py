from shape import *
from material import *
from camera import *
from ray import *
from vecmath import *
import Image

scene = Sphere(5.0, vector(0,0,0), ConstantShader(vector(0,0,1)))
camera = PerspectiveCamera(vector(0,0,10), vector(0,0,-1), vector(0,1,0))

def main():
  array = np.zeros((200, 200, 3))
  for i,x in enumerate(np.linspace(-1, 1, 200)):
    for j,y in enumerate(np.linspace(-1, 1, 200)):
      ray = camera.generateRay(vector(x,y))
      hit = scene.intersect(ray, 0)
      if hit == None:
        array[j][i] = vector(0,0,0)
      else:
        t, material, normal = hit
        array[j][i] = material.shade(t, ray, None)
  write_image(array)

def get_arguments():
    raise NotImplementedError

def write_image(array, outfile=None):
  if outfile == None:
    Image.fromarray(quantize(array).astype(np.uint8)).show()
  else:
    Image.fromarray(quantize(array)).save(outfile)

if __name__ == '__main__':
  main()
