import unittest
import main as main

class VirtualCbctTest(unittest.TestCase):
  def test_hello(self):
    self.assertTrue(main.hello())

if __name__ == '__main__':
  unittest.main()
