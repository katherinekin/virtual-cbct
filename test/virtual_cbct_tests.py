import unittest
import phantom as pm
import main as main

class VirtualCbctTest(unittest.TestCase):
  def test_hello(self):
    self.assertTrue(main.hello())

  def test_generate_phantom(self):
  	phantom, U, L = pm.generate_phantom()
  	self.assertTrue(len(U) == 512)
  	self.assertTrue(len(L) == 512)
  	
if __name__ == '__main__':
  unittest.main()
