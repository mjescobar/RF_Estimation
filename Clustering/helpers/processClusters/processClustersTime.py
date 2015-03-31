#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  processClustersTime.py
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
from numpy import loadtxt
from numpy import shape
from numpy import histogram
from numpy import amax
from numpy import amin
from numpy import append
from numpy import zeros
from numpy import empty
from numpy import linspace
from scipy.interpolate import UnivariateSpline
from math import ceil
from math import floor
from scipy.ndimage import gaussian_filter

clustersColours = ['blue', 'red', 'green', 'orange', 'black','yellow', \
				'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
				'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
				'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
				'#5b6756','#0c8248','k','#820cff','#932c11', \
				'#002c11','#829ca7']

clustersMarkers = ['o', '^', 'v', '*', 's','p', \
				'<','>','1', '2', '3', \
				'4', '8','h','H','+', \
				'x','D','d','|','_']

framesNumber = 20
xSize = 31
ySize = 31

def loadClusterFile(sourceFile):
	data = loadtxt(sourceFile, delimiter=',')
	
	return data

#Input file format

# 0-19 Timestamps
# aRadius
# bRadius
# angle
# xCoordinate
# yCoordinate
# area
# clusterId
# peakTime

def main():
	parser = argparse.ArgumentParser(prog='processClustersTime.py',
	 description='Plot units (time) from clustering',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFile',
	 help='Source file containing the units and its data',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	 
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
	
	Units = loadClusterFile(sourceFile)
	numeroClusters = int(max(Units[:,26]))
	
	# Calculates the next 5-step for the y-coordinate
	maxData =  ceil(amax(Units[:,0:framesNumber])/5)*5
	minData = floor(amin(Units[:,0:framesNumber])/5)*5
	
	figClusterCompletoSpline = plt.figure()
	axClusterCompletoSpline = figClusterCompletoSpline.add_subplot(111)
	figClusterCompletoGaussiano = plt.figure()
	axClusterCompletoGaussiano = figClusterCompletoGaussiano.add_subplot(111)
	figClusterCompletoCrudo = plt.figure()
	axClusterCompletoCrudo = figClusterCompletoCrudo.add_subplot(111)

	# Por cada cluster recorro las units
	for clusterId in range(numeroClusters + 1):
		clusterUnits = empty([1, 28])
		for unitId in range(len(Units)):
			if Units[unitId,26] == clusterId:
				clusterUnits = append(clusterUnits,Units[unitId].reshape(1, 28), axis=0)
				x = linspace(1, framesNumber, framesNumber)
				s = UnivariateSpline(x, Units[unitId,0:framesNumber], s=0)
				xs = linspace(1, framesNumber, framesNumber*1000)
				ys = s(xs)
				axClusterCompletoSpline.plot(ys,clustersColours[clusterId],\
				 alpha=0.2)
				axClusterCompletoGaussiano.plot(gaussian_filter(Units[unitId,0:framesNumber-1],1),\
				 clustersColours[clusterId],alpha=0.2)
				axClusterCompletoCrudo.plot(Units[unitId,0:framesNumber-1],\
				 clustersColours[clusterId],alpha=0.2)

		## remove the first row of zeroes
		clusterUnits = clusterUnits[1:,:]
		
		figCluster = plt.figure()
		axCluster = figCluster.add_subplot(111)
		meanData = clusterUnits[:,0:framesNumber].mean(axis=0)

		for curve in range(clusterUnits.shape[0]):
			x = linspace(1, framesNumber, framesNumber)
			s = UnivariateSpline(x, clusterUnits[curve,0:framesNumber], s=0)
			xs = linspace(1, framesNumber, framesNumber*1000)
			ys = s(xs)
			axCluster.plot(ys,clustersColours[clusterId],alpha=0.2)
		x = linspace(1, framesNumber, framesNumber)
		s = UnivariateSpline(x, meanData, s=0)
		xs = linspace(1, framesNumber, framesNumber*1000)
		ys = s(xs)
		axCluster.plot(ys,clustersColours[clusterId],linewidth=4)
		axClusterCompletoSpline.plot(ys,clustersColours[clusterId],linewidth=4)
		axClusterCompletoGaussiano.plot(gaussian_filter(meanData,1),clustersColours[clusterId],linewidth=4)
		axClusterCompletoCrudo.plot(meanData,clustersColours[clusterId],linewidth=4)
		
		axCluster.set_xlim(0, 1000*framesNumber-1)
		axCluster.set_ylim(minData,maxData)
		figCluster.savefig(outputFolder+'cluster_'+str(clusterId)+'.png', bbox_inches='tight')

	axClusterCompletoSpline.set_xlim(0, 1000*framesNumber-1)
	axClusterCompletoSpline.set_ylim(minData,maxData)
	figClusterCompletoSpline.savefig(outputFolder+'clusters_Spline.png', bbox_inches='tight')

	axClusterCompletoGaussiano.set_xlim(0, framesNumber-2)
	axClusterCompletoGaussiano.set_ylim(minData,maxData)
	figClusterCompletoGaussiano.savefig(outputFolder+'clusters_Gaussiano.png', bbox_inches='tight')

	axClusterCompletoCrudo.set_xlim(0, framesNumber-2)
	axClusterCompletoCrudo.set_ylim(minData,maxData)
	figClusterCompletoCrudo.savefig(outputFolder+'clusters_Crudo.png', bbox_inches='tight')
	
	return 0

if __name__ == '__main__':
	main()

