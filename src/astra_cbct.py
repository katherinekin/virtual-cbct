from __future__ import division
import os
import numpy as np
from os.path import join
from imageio import get_writer, imread, imwrite
 
import astra

PROJECTION_RESULTS = 'output/dataset'
RECONSTRUCTION_RESULTS = 'output/reconstruction'

class Virtual_Cbct():
	def __init__(self):
		# Configuration.
		self.distance_source_origin = 300  # [mm]
		self.distance_origin_detector = 100  # [mm]
		self.detector_pixel_size = 1.05  # [mm]
		self.detector_rows = 200  # Vertical size of detector [pixels].
		self.detector_cols = 200  # Horizontal size of detector [pixels].
		self.num_of_projections = 180
		
	def start_run(self, phantom):
		self.phantom = phantom
		self.angles = np.linspace(
			0, 2 * np.pi, num = self.num_of_projections, endpoint=False)
		self.proj_geom = astra.create_proj_geom('cone', 1, 1, 
			self.detector_rows, self.detector_cols, self.angles,
		  (self.distance_source_origin + self.distance_origin_detector) /
		  self.detector_pixel_size, 0)

		self.vol_geom = astra.creators.create_vol_geom(
			self.detector_cols, self.detector_cols, self.detector_rows)
		self.create_projections()
		self.create_reconstructions()
	
	def create_projections(self):
		# Create projections. With increasing angles, the projection are such that the
		# object is rotated clockwise. Slice zero is at the top of the object. The
		# projection from angle zero looks upwards from the bottom of the slice.
		phantom_id = astra.data3d.create('-vol', self.vol_geom, data = self.phantom)
		
		projections_id, projections = astra.creators.create_sino3d_gpu(
			phantom_id, self.proj_geom, self.vol_geom)

		projections /= np.max(projections)
		 
		# Apply Poisson noise.
		projections = np.random.poisson(projections * 10000) / 10000
		projections[projections > 1.1] = 1.1
		projections /= 1.1
		 
		# Save projections.
		projections = np.round(projections * 65535).astype(np.uint16)

		output_dir = PROJECTION_RESULTS	
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)

		for i in range(self.num_of_projections):
			projection = projections[:, i, :]
			with get_writer(join(output_dir, 'proj%04d.tif' %i)) as writer:
				writer.append_data(projection, {'compress': 9})
		 
		# Cleanup.
		astra.data3d.delete(projections_id)
		astra.data3d.delete(phantom_id)
	
	def create_reconstructions(self):
		# Set result directories
		input_dir = PROJECTION_RESULTS
		output_dir = RECONSTRUCTION_RESULTS
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		# Load projections from saved directory.
		projections = np.zeros((self.detector_rows, self.num_of_projections, self.detector_cols))
		for i in range(self.num_of_projections):
			im = imread(join(input_dir, 'proj%04d.tif' % i)).astype(float)
			im /= 65535
			projections[:, i, :] = im
		 
		# Copy projection images into ASTRA Toolbox.
		projections_id = astra.data3d.create('-sino', self.proj_geom, projections)
		 
		# Create reconstruction.
		reconstruction_id = astra.data3d.create('-vol', self.vol_geom, data=0)
		alg_cfg = astra.astra_dict('FDK_CUDA')
		alg_cfg['ProjectionDataId'] = projections_id
		alg_cfg['ReconstructionDataId'] = reconstruction_id
		algorithm_id = astra.algorithm.create(alg_cfg)
		astra.algorithm.run(algorithm_id)
		reconstruction = astra.data3d.get(reconstruction_id)
		 
		# Limit and scale reconstruction.
		reconstruction[reconstruction < 0] = 0
		reconstruction /= np.max(reconstruction)
		reconstruction = np.round(reconstruction * 255).astype(np.uint8)
		 
		# Save reconstruction.
		for i in range(self.detector_rows):
			im = reconstruction[i, :, :]
			im = np.flipud(im)
			imwrite(join(output_dir, 'reco%04d.tif' % i), im)
		 
		# Cleanup.
		astra.algorithm.delete(algorithm_id)
		astra.data3d.delete(reconstruction_id)
		astra.data3d.delete(projections_id)

# cbct = Virtual_Cbct()
# cbct.start_run()