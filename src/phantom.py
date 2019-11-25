# Generates a hollow phantom to represent the skull
# 512 x 512 default size for now
# Outside represents air
# Thickness represents thickness of the skull
# Rest of inside represents brain
import numpy as np
import cv2
import matplotlib.pyplot as plt

xPixels = yPixels = 512
zPixels = 512
cmPerPixel = 10

def get_attenuations():
	# phantom = np.zeros((yPixels, xPixels), np.uint8) # phantom image
	U = np.zeros((yPixels, xPixels), np.float32) # attenuation matrix
	L = np.ones((yPixels, xPixels), np.float32) # length matrix

	# TODO: may just use this as a conversion factor, no need for matrix
	L = L * cmPerPixel / xPixels # how many cm per pixel

	struct_1 = np.zeros((yPixels, xPixels), np.float32)
	struct_1[int(yPixels * 0.25): int(yPixels * 0.25) + 256, 
			int(xPixels * 0.25): int(xPixels * 0.25) + 256] = 1
	attenuation_1 = 0.6

	# TODO: thickness can be passed as an argument
	thickness = 20

	struct_2 = np.zeros((yPixels, xPixels), np.float32)
	struct_2[int(yPixels * 0.25) + thickness: int(yPixels * 0.25) + 256 - thickness, 
			int(xPixels * 0.25) + thickness: int(xPixels * 0.25) + 256 - thickness] = 1
	attenuation_2 = 0.2

	# phantom += struct_1.astype(np.uint8)        
	U = U + struct_1 * attenuation_1 + struct_2 * attenuation_2 - struct_2 * attenuation_1

	return U

def generate_phantom():
	phantom = np.zeros((yPixels, xPixels), np.uint8) # phantom image
	return get_attenuations() * 255

def get_phantom_jpg(phantom):
	cv2.imwrite("phantom.jpg", normalize_image(phantom))

def normalize_image(phantom):
	min_val = np.min(phantom)
	max_val = np.max(phantom)
	return (phantom - min_val)*(255/(max_val-min_val))