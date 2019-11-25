import numpy as np
import cv2
import matplotlib.pyplot as plt
import phantom as pm

cmPerPixel = 10

# Compute the instensity across all layers (using matrix multiplication)
def get_length_matrix(U):
	xPixels = yPixels = len(U)
	L = np.ones((yPixels, xPixels), np.float32) # length matrix
	L = L * cmPerPixel / xPixels # how many cm per pixel
	return L

def compute_signal_intensity(i_0, U):
	return i_0 * np.prod(np.exp(-1 * np.multiply(U, get_length_matrix(U))), axis=1)

def get_x_ray(sensor_resolution, i_0, U):
	# Get Intensities
	x_ray = compute_signal_intensity(i_0, U)

	# map to sensor resolution
	print(x_ray.shape)
	x_ray = x_ray.reshape(sensor_resolution, U.shape[0]//sensor_resolution)
	print(x_ray.shape)
	x_ray = np.mean(x_ray, axis=1)
	print(x_ray.shape)
	return x_ray

def show_graphs(x_ray):
	plt.figure(3)
	plt.title("Intensity Merged")
	plt.plot(x_ray, 'ro')
	plt.plot(x_ray)
	plt.ylabel('Signal Intensity')
	plt.show()