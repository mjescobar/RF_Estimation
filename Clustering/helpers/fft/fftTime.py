#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fftTime.py
#  
#  Copyright 2015 Carlos "casep" Sepulveda <carlos.sepulveda@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe				#Some custom functions
import argparse 							#argument parsing
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from numpy import append, empty, fft, sqrt, linspace, shape
from math import ceil, floor
#from scipy.interpolate import UnivariateSpline
#from scipy.ndimage import gaussian_filter

xSize = 31
ySize = 31

def main():
	parser = argparse.ArgumentParser(prog='fftTime.py',
	 description='fft Time dimension',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFile',
	 help='Source file containing the units and its data',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	parser.add_argument('--framesNumber',
	 help='Number of frames',
	 type=int, default=18, required=False) 
	args = parser.parse_args()

	#Source file of the units
	sourceFile = args.sourceFile
	if not os.path.exists(sourceFile):
		print ''
		print 'Source file does not exists ' + sourceFile
		print ''
		sys.exit()

	#Output folder for the graphics
	outputFolder = rfe.fixPath(args.outputFolder)
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except:
			print ''
			print 'Unable to create folder ' + outputFolder
			print ''
			sys.exit()
	
	framesNumber = args.framesNumber
	Units = rfe.loadClusterFile(sourceFile,framesNumber)
	numeroClusters = int(max(Units[:,framesNumber+6]))
		
	# Por cada cluster recorro las units
	for clusterId in range(numeroClusters + 1):
		clusterUnits = empty([1, framesNumber+9])
		for unitId in range(len(Units)):
			if Units[unitId,framesNumber+6] == clusterId:
				clusterUnits = append(clusterUnits,Units[unitId].reshape(1, framesNumber+9), axis=0)

		## remove the first row of zeroes
		clusterUnits = clusterUnits[1:,:]
		
		figCluster = plt.figure()
		axCluster = figCluster.add_subplot(111)
		meanData = clusterUnits[:,0:framesNumber].mean(axis=0)

		fftData = fft.fft(meanData)
		freq = fft.fftfreq(meanData.shape[-1])
		freq = linspace(1,300,framesNumber)
		isqr = fftData.imag*fftData.imag
		rsqr = fftData.real*fftData.real
		axCluster.plot(freq, fftData.real, label='Real')
		axCluster.plot(freq, fftData.imag, label='Imaginario')
		axCluster.plot(freq, sqrt(rsqr + isqr), label='Modulo')
		plt.legend(loc="upper right", bbox_to_anchor=[0, 1], ncol=1, shadow=True, title="Legenda", fancybox=True)
		figCluster.savefig(outputFolder+'cluster_'+str(clusterId)+'.png', bbox_inches='tight')	
		plt.close()
		
	return 0

if __name__ == '__main__':
	main()
