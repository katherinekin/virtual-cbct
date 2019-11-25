import unittest
import phantom as pm
import main as main
import os.path
from os import path

class VirtualCbctTest(unittest.TestCase):
  def test_hello(self):
    self.assertTrue(main.hello())

  def test_get_attenuations(self):
  	U = pm.get_attenuations()
  	self.assertTrue(len(U) == 512)

  def test_generate_phantom(self):
  	self.assertTrue(len(pm.generate_phantom() == 512))

  def test_get_phantom_jpg(self):
  	pm.get_phantom_jpg(pm.generate_phantom())
  	self.assertTrue(path.exists("./phantom.jpg"))

if __name__ == '__main__':
  unittest.main()
