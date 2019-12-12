import numpy as np
import cv2
import matplotlib.pyplot as plt

class PhantomGenerator():
	def __init__(self):
		self.thickness = 10
		self.height = 110
		self.width = 40
		self.shellAttenuation = 1
		self.cavityAttenuation = 0.5

	def create_phantom(self):
		# Create phantom with default size of 200
		rows = 200 if max(self.height, self.width) <= 200 else max(self.height, self.width) + 20
		columns = rows

		phantom = np.zeros((rows, columns, columns))
		cavityHeight = self.height - (self.thickness * 2) 
		cavityWidth = self.width - (self.thickness * 2) 

		phantom[
				rows // 2 - self.height // 2 : rows // 2 + self.height // 2,
				columns // 2 - self.width // 2 : columns // 2 + self.width // 2,
				columns // 2 - self.width // 2 : columns // 2 + self.width // 2
			] = self.shellAttenuation

		phantom[
				rows // 2 - cavityHeight // 2 : rows // 2 + cavityHeight // 2,
				columns // 2 - cavityWidth // 2 : columns // 2 + cavityWidth // 2,
				columns // 2 - cavityWidth // 2 : columns // 2 + cavityWidth // 2
			] = self.cavityAttenuation

		phantom[
				rows // 2 - 5 : rows // 2 + 5,
				columns // 2 + cavityWidth // 2 : columns // 2 + self.width // 2,
				columns // 2 - 5 : columns // 2 + 5
			] = 0
		return phantom

	def phantom_on_detector(self, phantom, detectorRows, detectorColumns):
		# reshape phantom based on detector size
		newPhantom = np.zeros((detectorRows, detectorColumns, detectorColumns))
		phantomSize = len(phantom)

		if detectorRows < phantomSize:
			phantomRowStart = phantomSize // 2 - detectorRows // 2
			phantomRowEnd = phantomRowStart + detectorRows
			rowStart = 0
			rowEnd = detectorRows
			
		elif detectorRows > phantomSize:
			phantomRowStart = 0
			phantomRowEnd = phantomSize
			rowStart = detectorRows // 2 - phantomSize // 2
			rowEnd = rowStart + phantomSize

		elif detectorRows == phantomSize:
			rowStart = phantomRowStart = 0
			rowEnd = phantomRowEnd = phantomSize

		if detectorColumns < phantomSize:
			phantomColStart = phantomSize // 2 - detectorColumns // 2
			phantomColEnd = phantomColStart + detectorColumns
			colStart = 0
			colEnd = detectorColumns

		elif detectorColumns > phantomSize:
			phantomColStart = 0
			phantomColEnd = phantomSize
			colStart = detectorColumns // 2 - phantomSize // 2
			colEnd = colStart + phantomSize

		elif detectorColumns == phantomSize:
			colStart = phantomColStart = 0
			colEnd = phantomColEnd = phantomSize

		print (rowStart, rowEnd, colStart, colEnd, phantomRowStart, phantomRowEnd, phantomColStart, phantomColEnd)
		newPhantom[rowStart: rowEnd, colStart: colEnd, colStart: colEnd] = \
			phantom[
				phantomRowStart: phantomRowEnd, 
				phantomColStart: phantomColEnd, 
				phantomColStart: phantomColEnd]

		return newPhantom

def get_phantom_jpg(phantom):
	dimensions = phantom.shape
	cv2.imwrite("phantom_xy.jpg", normalize_image(phantom[dimensions[0]//2, :, :]))
	cv2.imwrite("phantom_yz.jpg", normalize_image(phantom[:, dimensions[1]//2, :]))
	cv2.imwrite("phantom_xz.jpg", normalize_image(phantom[:, :, dimensions[1]//2]))

def normalize_image(phantom):
	min_val = np.min(phantom)
	max_val = np.max(phantom)
	return (phantom - min_val)*(255/(max_val-min_val))