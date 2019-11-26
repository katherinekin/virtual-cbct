from __future__ import division
import os
import numpy as np
from os.path import join
from imageio import get_writer
 
import astra

class Virtual_Cbct():
	def __init__(self):
		# Configuration.
		self.distance_source_origin = 300  # [mm]
		self.distance_origin_detector = 100  # [mm]
		self.detector_pixel_size = 1.05  # [mm]
		self.detector_rows = 200  # Vertical size of detector [pixels].
		self.detector_cols = 200  # Horizontal size of detector [pixels].
		self.num_of_projections = 180
		self.angles = np.linspace(
			0, 2 * np.pi, num = self.num_of_projections, endpoint=False)
		self.output_dir = 'output'
	
		if not os.path.exists(self.output_dir):
			os.makedirs(self.output_dir)

	def create_phantom(self):
		# Create phantom.
		vol_geom = astra.creators.create_vol_geom(
			self.detector_cols, self.detector_cols, self.detector_rows)

		phantom = np.zeros(
			(self.detector_rows, self.detector_cols, self.detector_cols))

		hb = 110  # Height of beam [pixels].
		wb = 40   # Width of beam [pixels].
		hc = 100  # Height of cavity in beam [pixels].
		wc = 30   # Width of cavity in beam [pixels].
		phantom[
				self.detector_rows // 2 - hb // 2 : self.detector_rows // 2 + hb // 2,
				self.detector_cols // 2 - wb // 2 : self.detector_cols // 2 + wb // 2,
				self.detector_cols // 2 - wb // 2 : self.detector_cols // 2 + wb // 2
			] = 1

		phantom[
				self.detector_rows // 2 - hc // 2 : self.detector_rows // 2 + hc // 2,
				self.detector_cols // 2 - wc // 2 : self.detector_cols // 2 + wc // 2,
				self.detector_cols // 2 - wc // 2 : self.detector_cols // 2 + wc // 2
			] = 0

		phantom[
				self.detector_rows // 2 - 5 : self.detector_rows // 2 + 5,
				self.detector_cols // 2 + wc // 2 : self.detector_cols // 2 + wb // 2,
				self.detector_cols // 2 - 5 : self.detector_cols // 2 + 5
			] = 0

		phantom_id = astra.data3d.create('-vol', vol_geom, data=phantom)
		return phantom, phantom_id, vol_geom
	
	def create_projections(self):
		# Create projections. With increasing angles, the projection are such that the
		# object is rotated clockwise. Slice zero is at the top of the object. The
		# projection from angle zero looks upwards from the bottom of the slice.
		phantom, phantom_id, vol_geom = self.create_phantom()

		proj_geom = astra.create_proj_geom('cone', 1, 1, 
			self.detector_rows, self.detector_cols, self.angles,
		  (self.distance_source_origin + self.distance_origin_detector) /
		  self.detector_pixel_size, 0)

		projections_id, projections = astra.creators.create_sino3d_gpu(
			phantom_id, proj_geom, vol_geom)

		projections /= np.max(projections)
		 
		# Apply Poisson noise.
		projections = np.random.poisson(projections * 10000) / 10000
		projections[projections > 1.1] = 1.1
		projections /= 1.1
		 
		# Save projections.
		projections = np.round(projections * 65535).astype(np.uint16)

		for i in range(self.num_of_projections):
			projection = projections[:, i, :]
			with get_writer(join(self.output_dir, 'proj%04d.tif' %i)) as writer:
				writer.append_data(projection, {'compress': 9})
		 
		# Cleanup.
		astra.data3d.delete(projections_id)
		astra.data3d.delete(phantom_id)

cbct = Virtual_Cbct()
cbct.create_projections()