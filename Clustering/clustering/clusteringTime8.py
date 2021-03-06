#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SpectralClustering.py
#  
#  Copyright 2014 Carlos "casep" Sepulveda <carlos.sepulveda@gmail.com>
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

# Performs clustering using different libraries

import sys, os 
#Relative path for RFE LIB
sys.path.append(os.path.join(os.path.dirname(__file__), '../..','LIB'))
import rfestimationLib as rfe				#Some custom functions
import argparse 							#argument parsing
from sklearn import metrics
from sklearn import preprocessing
from math import ceil
from math import floor
from scipy.interpolate import UnivariateSpline
from numpy import zeros
from numpy import linspace
from numpy import concatenate
from numpy import append
from numpy import amax
from numpy import amin
from numpy import chararray
from numpy import shape
from numpy import savetxt
from numpy import where
from numpy import unique
from numpy import mean
from numpy import absolute
from math import pi
from numpy import float64
from numpy import empty
from numpy import reshape

#Output file format

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
	
	parser = argparse.ArgumentParser(prog='clusteringTime8.py',
	 description='Performs clustering, Gaussian Mixture, KMeans or Spectral',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='Source folder',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	parser.add_argument('--clustersNumber',
	 help='Number of clusters',
	 type=int, default='3', choices=[2,3,4,5,6,7,8,9,10,11,12,13,14,15], required=False)
	parser.add_argument('--framesNumber',
	 help='Number of frames used in STA analysis',
	 type=int, default='20', required=False)
	parser.add_argument('--blockSize',
	 help='Size of each block in micrometres',
	 type=int, default='50', required=False)
	parser.add_argument('--clusteringAlgorithm',
	 help='Clustering algorithm to use: K-Means, Spectral Clustering, GMM',
	 type=str, default='kmeans', choices=['kmeans','spectral','gmm','densityPeaks'], required=False)
	parser.add_argument('--percentageDensityDistance',
	 help='Percentage used to calculate the distance',
	 type=float, default='2', required=False)
	 
	args = parser.parse_args()

	#Source folder of the files with the timestamps
	sourceFolder = rfe.fixPath(args.sourceFolder)
	if not os.path.exists(sourceFolder):
		print ''
		print 'Source folder does not exists ' + sourceFolder
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
	
	#Clusters number for the kmeans algorithm
	clustersNumber = args.clustersNumber

	#Frames used in STA analysis
	framesNumber = args.framesNumber
	
	#Size of each block in micrometres
	blockSize = args.blockSize
	
	#Clustering Algorithm
	clusteringAlgorithm = args.clusteringAlgorithm
	
	#dataCluster stores the data to be used for the clustering process
	#the size is equal to the number of frames, aka, the time component
	#plus 5 as we are incorporating the 2 dimensions of the ellipse, 
	#x position, y position and angle
	dataCluster = zeros((1,framesNumber+7))
	units = []
	dato = empty((1,1))
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):	
			dato = empty((1,1))		
			unitName = unitFile.rsplit('_', 1)[0]
			#print unitName
			dataUnit, coordinates = rfe.loadSTACurve(sourceFolder,unitFile,unitName)
			xSize = dataUnit.shape[0]
			ySize = dataUnit.shape[1]
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			dataUnitTemporal = dataUnit[coordinates[0][0],[coordinates[1][0]],:]
			#Time data from FITResult
			#dataUnitTemporal = rfe.loadVectorAmp(sourceFolder,unitFile).T
			#A radius of the RF ellipse
			aRadius = fitResult[0][2]
			dato[0] = aRadius
			dataUnitCompleta = concatenate((dataUnitTemporal,dato),1)
			#B radius of the RF ellipse
			bRadius = fitResult[0][3]
			dato[0] = bRadius
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#angle of the RF ellipse
			angle = fitResult[0][1]
			dato[0] = angle
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#X coordinate of the RF ellipse
			xCoordinate = fitResult[0][4]
			#print 'xCoordinate',xCoordinate
			dato[0] = xCoordinate
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#Y coordinate of the RF ellipse
			yCoordinate = fitResult[0][5]
			#print 'yCoordinate',yCoordinate
			dato[0] = yCoordinate
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#Area of the RF ellipse
			area = aRadius*bRadius*pi
			dato[0] = area
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#UnitName
			dato=empty(1, dtype='|S16')
			dato[0]=unitName
			dataUnitCompleta = concatenate((dataUnitCompleta,dato.reshape(1, 1)),1)
			
			dataCluster = append(dataCluster,dataUnitCompleta, axis=0)
			
			units.append(unitName)
	# remove the first row of zeroes
	dataCluster = dataCluster[1:,:]	
		
	#Solo temporal dataCluster[:,0:framesNumber]
	# framesNumber
	data = dataCluster[:,framesNumber*.45:framesNumber*.9]
	data = data.astype(float64, copy=False)
	
	# Calculates the next 5-step for the y-coordinate
	maxData =  ceil(amax(data)/5)*5
	minData = floor(amin(data)/5)*5

	if clusteringAlgorithm == 'spectral':
		from sklearn.cluster import SpectralClustering
		sc = SpectralClustering(n_clusters=clustersNumber, eigen_solver=None, \
				random_state=None,  n_init=10, gamma=1.0, affinity='nearest_neighbors', \
				n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, \
				coef0=1, kernel_params=None)
		sc.fit(data)
		labels = sc.labels_
	elif clusteringAlgorithm == 'gmm':
		from sklearn import mixture
		gmix = mixture.GMM(n_components=clustersNumber, covariance_type='spherical')
		gmix.fit(data)
		labels = gmix.predict(data)
	elif clusteringAlgorithm == 'densityPeaks':
		import densityPeaks as dp
		percentageDensityDistance = args.percentageDensityDistance
		clustersNumber, labels = dp.predict(data, percentageDensityDistance)
	else:
		from sklearn.cluster import KMeans
		km = KMeans(init='k-means++', n_clusters=clustersNumber, n_init=10,n_jobs=-1)
		km.fit(data)
		labels = km.labels_
	
	dataFile = empty((1,framesNumber+9),dtype='|S16')
	datos = empty((1,framesNumber+7),dtype='|S16')
	dato = empty((1,1),dtype='|S16')
	for clusterId in range(clustersNumber):
		for unitId in range(dataCluster.shape[0]):
			if labels[unitId] == clusterId:			
				dato[0] = clusterId
				dataFileTmp = concatenate(([dataCluster[unitId,:]],dato),1)
				x = linspace(1, framesNumber, framesNumber)
				s = UnivariateSpline(x, dataCluster[unitId,0:framesNumber], s=0)
				xs = linspace(1, framesNumber, framesNumber*1000)
				ys = s(xs)
				
				media = mean(ys)
				maximo = amax(ys)
				minimo = amin(ys)
				maximaDistancia = absolute(maximo-media)
				minimaDistancia = absolute(minimo-media) 
				peakTempCurve = minimo
				if maximaDistancia > minimaDistancia:
					peakTempCurve = maximo
				dato[0] = unique(where(peakTempCurve==ys)[0])[0]
				dataFileTmp = concatenate((dataFileTmp,dato),1)
				dataFile = append(dataFile, dataFileTmp, axis=0)
		
	# remove the first row of zeroes
	dataFile = dataFile[1:,:]
	savetxt(outputFolder+'outputFile.csv',dataFile, fmt='%s', delimiter=',', newline='\n')
		
	return 0

if __name__ == '__main__':
	main()
