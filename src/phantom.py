# Generates a hollow phantom to represent the skull
# 512 x 512 default size for now
# Outside represents air
# Thickness represents thickness of the skull
# Rest of inside represents brain
import numpy as np
import cv2
import matplotlib.pyplot as plt

def generate_phantom():
	widthPixels = heightPixels = 512
	heightPixels = 512
	cmPerPixel = 10

	phantom = np.zeros((heightPixels, widthPixels), np.uint8) # phantom image
	U = np.zeros((heightPixels, widthPixels), np.float32) # attenuation matrix
	L = np.ones((heightPixels, widthPixels), np.float32) # length matrix

	# TODO: may just use this as a conversion factor, no need for matrix
	L = L * cmPerPixel / widthPixels # how many cm per pixel

	struct_1 = np.zeros((heightPixels, widthPixels), np.float32)
	struct_1[int(heightPixels*0.1): int(heightPixels * 0.1) * 2, 
			int(widthPixels * 0.3): int(widthPixels * 0.3) + int(widthPixels * 0.1)] = 1
	attenuation_1 = 0.2

	phantom += struct_1.astype(np.uint8)        
	U += struct_1 * attenuation_1
	phantom *= 255

	return phantom, U, L

def get_phantom_jpg(phantom):
	cv2.imwrite("phantom.jpg", phantom)