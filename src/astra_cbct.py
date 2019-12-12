from __future__ import division
import os
import shutil
import numpy as np
from os.path import join
from imageio import get_writer, imread, imwrite
 
import astra

PROJECTION_RESULTS = 'output/dataset'
RECONSTRUCTION_RESULTS = 'output/reconstruction'

class Virtual_Cbct():
	def __init__(self):
		# Configuration.
		self.distanceFromSourceToOrigin = 300  # [mm]
		self.distanceFromOriginToDetector = 10  # [mm]
		self.pixelSize = 1.05  # [mm]
		self.detectorRows = 200  # Vertical size of detector [pixels].
		self.detectorColumns = 200  # Horizontal size of detector [pixels].
		self.numberOfProjections = 180
		
	def start_run(self, phantom):
		self.phantom = phantom
		self.angles = np.linspace(
			0, 2 * np.pi, num = self.numberOfProjections, endpoint=False)
		self.projectionGeometry = astra.create_proj_geom(
			'cone', 1, 1, 
			self.detectorRows, 
			self.detectorColumns, 
			self.angles,
			self.distanceFromSourceToOrigin / self.pixelSize, 
		  	self.distanceFromOriginToDetector / self.pixelSize
		)

		self.vol_geom = astra.creators.create_vol_geom(
			self.detectorColumns, self.detectorColumns, self.detectorRows)
		self.create_projections()
		self.create_reconstructions()
	
	def create_projections(self):
		# Projections are created as if phantom is rotated clockwise. 
		phantomId = astra.data3d.create('-vol', self.vol_geom, data = self.phantom)
		
		projectionId, projections = astra.creators.create_sino3d_gpu(
			phantomId, self.projectionGeometry, self.vol_geom)

		projections /= np.max(projections)
		 
		# Apply Poisson noise.
		projections = np.random.poisson(projections * 10000) / 10000
		projections[projections > 1.1] = 1.1
		projections /= 1.1
		 
		# Save projections.
		projections = np.round(projections * 65535).astype(np.uint16)

		# If output path exists (from previous run) delete and create new folder
		output_dir = PROJECTION_RESULTS	
		if os.path.exists(output_dir):
			shutil.rmtree(output_dir)
		os.makedirs(output_dir)

		for i in range(self.numberOfProjections):
			projection = projections[:, i, :]
			with get_writer(join(output_dir, 'proj%04d.tif' %i)) as writer:
				writer.append_data(projection, {'compress': 9})
		 
		# Cleanup.
		astra.data3d.delete(projectionId)
		astra.data3d.delete(phantomId)
	
	def create_reconstructions(self):
		# Set result directories
		input_dir = PROJECTION_RESULTS
		output_dir = RECONSTRUCTION_RESULTS
		if os.path.exists(output_dir):
			shutil.rmtree(output_dir)
		os.makedirs(output_dir)

		projections = np.zeros((self.detectorRows, self.numberOfProjections, self.detectorColumns))
		for i in range(self.numberOfProjections):
			im = imread(join(input_dir, 'proj%04d.tif' % i)).astype(float)
			im /= 65535
			projections[:, i, :] = im
		 
		# Copy projection images into ASTRA Toolbox.
		projectionId = astra.data3d.create('-sino', self.projectionGeometry, projections)
		 
		# Create reconstruction.
		reconstruction_id = astra.data3d.create('-vol', self.vol_geom, data=0)
		alg_cfg = astra.astra_dict('FDK_CUDA')
		alg_cfg['ProjectionDataId'] = projectionId
		alg_cfg['ReconstructionDataId'] = reconstruction_id
		algorithm_id = astra.algorithm.create(alg_cfg)
		astra.algorithm.run(algorithm_id)
		reconstruction = astra.data3d.get(reconstruction_id)
		 
		# Limit and scale reconstruction.
		reconstruction[reconstruction < 0] = 0
		reconstruction /= np.max(reconstruction)
		reconstruction = np.round(reconstruction * 255).astype(np.uint8)
		 
		# Save reconstruction.
		for i in range(self.detectorRows):
			im = reconstruction[i, :, :]
			im = np.flipud(im)
			imwrite(join(output_dir, 'reco%04d.tif' % i), im)
		 
		# Cleanup.
		astra.algorithm.delete(algorithm_id)
		astra.data3d.delete(reconstruction_id)
		astra.data3d.delete(projectionId)