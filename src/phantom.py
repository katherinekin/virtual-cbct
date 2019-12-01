import numpy as np
import cv2
import matplotlib.pyplot as plt

class PhantomGenerator():
	def __init__(self):
		self.thickness = 10
		self.height = 110
		self.width = 40
		self.shellAttenuation = 1
		self.cavityAttenuation = 0

	def create_phantom(self, detector_rows, detector_cols):
		# Create phantom	
		phantom = np.zeros((detector_rows, detector_cols, detector_cols))
		cavityHeight = self.height - (self.thickness * 2)  # Height of cavity in beam [pixels].
		cavityWidth = self.width - (self.thickness * 2)   # Width of cavity in beam [pixels].
		phantom[
				detector_rows // 2 - self.height // 2 : detector_rows // 2 + self.height // 2,
				detector_cols // 2 - self.width // 2 : detector_cols // 2 + self.width // 2,
				detector_cols // 2 - self.width // 2 : detector_cols // 2 + self.width // 2
			] = 1

		phantom[
				detector_rows // 2 - cavityHeight // 2 : detector_rows // 2 + cavityHeight // 2,
				detector_cols // 2 - cavityWidth // 2 : detector_cols // 2 + cavityWidth // 2,
				detector_cols // 2 - cavityWidth // 2 : detector_cols // 2 + cavityWidth // 2
			] = 0

		phantom[
				detector_rows // 2 - 5 : detector_rows // 2 + 5,
				detector_cols // 2 + cavityWidth // 2 : detector_cols // 2 + self.width // 2,
				detector_cols // 2 - 5 : detector_cols // 2 + 5
			] = 0
		return phantom

# TODO: determine if below is needed
def generate_phantom():
	phantom = np.zeros((yPixels, xPixels), np.uint8) # phantom image
	return get_attenuations() * 255

def get_phantom_jpg(phantom):
	cv2.imwrite("phantom.jpg", normalize_image(phantom))

def normalize_image(phantom):
	min_val = np.min(phantom)
	max_val = np.max(phantom)
	return (phantom - min_val)*(255/(max_val-min_val))