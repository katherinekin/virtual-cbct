import unittest
import phantom as pm
import cbct as cbct
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

	# def test_get_x_ray_graph(self):
	# 	sensor_resolution = 64
	# 	i_0 = 40	# keV
	# 	U = pm.get_attenuations()
	# 	cbct.show_graphs(cbct.get_x_ray(sensor_resolution, i_0, U))


if __name__ == '__main__':
	unittest.main()
