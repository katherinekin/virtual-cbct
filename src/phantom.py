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

	def create_phantom(self, detectorRows, detectorColumns):
		# Create phantom	
		phantom = np.zeros((detectorRows, detectorColumns, detectorColumns))
		cavityHeight = self.height - (self.thickness * 2)  # Height of cavity in beam [pixels].
		cavityWidth = self.width - (self.thickness * 2)   # Width of cavity in beam [pixels].
		phantom[
				detectorRows // 2 - self.height // 2 : detectorRows // 2 + self.height // 2,
				detectorColumns // 2 - self.width // 2 : detectorColumns // 2 + self.width // 2,
				detectorColumns // 2 - self.width // 2 : detectorColumns // 2 + self.width // 2
			] = self.shellAttenuation

		phantom[
				detectorRows // 2 - cavityHeight // 2 : detectorRows // 2 + cavityHeight // 2,
				detectorColumns // 2 - cavityWidth // 2 : detectorColumns // 2 + cavityWidth // 2,
				detectorColumns // 2 - cavityWidth // 2 : detectorColumns // 2 + cavityWidth // 2
			] = self.cavityAttenuation

		phantom[
				detectorRows // 2 - 5 : detectorRows // 2 + 5,
				detectorColumns // 2 + cavityWidth // 2 : detectorColumns // 2 + self.width // 2,
				detectorColumns // 2 - 5 : detectorColumns // 2 + 5
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