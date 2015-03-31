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
import scipy.ndimage
from sklearn import metrics
from sklearn import preprocessing
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
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
from numpy import reshape
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from mpl_toolkits.mplot3d import Axes3D

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
          
clustersColours = ['blue', 'red', 'green', 'orange', 'black','yellow', \
				'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
				'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
				'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
				'#5b6756','#0c8248','k','#820cff','#932c11', \
				'#002c11','#829ca7']

clustersMarkers = ['o', '^', '*', 'v', 's','p', \
				'<','>','1', '2', '3', \
				'4', '8','h','H','+', \
				'x','D','d','|','_']

def main():
	
	parser = argparse.ArgumentParser(prog='clustering.py',
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
	 type=int, default='5', choices=[2,3,4,5,6,7,8,9,10,11,12,13,14,15], required=False)
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
	dataCluster = zeros((1,framesNumber+6))
	units = []
	dato = zeros((1,1))
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			unitName = unitFile.rsplit('_', 1)[0]
			dataUnit, coordinates = rfe.loadSTACurve(sourceFolder,unitFile,unitName)
			xSize = dataUnit.shape[0]
			ySize = dataUnit.shape[1]
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			#Time data from STA with gauss fit
			#dataUnitTemporal = scipy.ndimage.gaussian_filter(dataUnit[coordinates[0][0],[coordinates[1][0]],:],2)
			#Time data from STA without  gauss fit
			dataUnitTemporal = dataUnit[coordinates[0][0],[coordinates[1][0]],:]
			#Time data from FITResult
			#dataUnitTemporal = rfe.loadVectorAmp(sourceFolder,unitFile).T
			#A radius of the RF ellipse
			aRadius = fitResult[0][2]
			dato[0] = aRadius
			dataUnitCompleta = concatenate((dataUnitTemporal,dato),1)
			#B radius of the RF ellipse
			bRadius = fitResult[0][2]
			dato[0] = bRadius
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#angle of the RF ellipse
			angle = fitResult[0][1]
			dato[0] = angle
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#X coordinate of the RF ellipse
			xCoordinate = fitResult[0][4]
			dato[0] = xCoordinate
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#Y coordinate of the RF ellipse
			yCoordinate = fitResult[0][5]
			dato[0] = yCoordinate
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			#Area of the RF ellipse
			area = aRadius*bRadius*pi
			dato[0] = area
			dataUnitCompleta = concatenate((dataUnitCompleta,dato),1)
			
			dataCluster = append(dataCluster,dataUnitCompleta, axis=0)
			units.append(unitName)
	# remove the first row of zeroes
	dataCluster = dataCluster[1:,:]	
		
	#Solo temporal dataCluster[:,0:framesNumber]
	#Temporal y espacial dataCluster[:,0:framesNumber+2]
	#data = dataCluster[:,0:framesNumber]
	#PCA
	n_components = 2
	pca = PCA(n_components=n_components)
	timePCA = pca.fit_transform(dataCluster[:,0:framesNumber])
	media = (dataCluster[:,framesNumber+1] + dataCluster[:,framesNumber+2])/2
	area = dataCluster[:,framesNumber+1]*dataCluster[:,framesNumber+2]*3
	timePlusMedia = concatenate((timePCA,reshape(media,(len(media),1))),axis=1)
	#data = concatenate((timePlusMedia,reshape(area,(len(area),1))),axis=1)
	data = concatenate((timePCA,reshape(media,(len(media),1))),axis=1)
	data = normalize(data, axis=0)
	
	# Calculates the next 5-step for the y-coordinate
	maxData =  ceil(amax(dataCluster[:,0:framesNumber])/5)*5
	minData = floor(amin(dataCluster[:,0:framesNumber])/5)*5

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
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# generate graphics of all ellipses
	dataFile = zeros((1,framesNumber+8))
	datos = zeros((1,framesNumber+6))
	dato = zeros((1,1))
	fig3D = plt.figure()
	ax3D = fig3D.add_subplot(111, projection='3d')
	for clusterId in range(clustersNumber):
		dataGrilla = zeros((1,framesNumber+6))
		for unitId in range(dataCluster.shape[0]):
			if labels[unitId] == clusterId:			
				datos[0] = dataCluster[unitId,:]
				dataGrilla = append(dataGrilla,datos, axis=0)		
				dato[0] = clusterId
				dataFileTmp = concatenate(([dataCluster[unitId,:]],dato),1)
				x = linspace(1, framesNumber, framesNumber)
				s = UnivariateSpline(x, dataCluster[unitId,0:framesNumber], s=0)
				xs = linspace(1, framesNumber, framesNumber*1000)
				ys = s(xs)
				
				#3d plotting for each cluster
				ax3D.scatter(data[unitId,0], data[unitId,1], data[unitId,2],\
				 c=clustersColours[clusterId], marker=clustersMarkers[clusterId])
				
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

				#ax.plot(dataCluster[unitId,0:framesNumber],clustersColours[clusterId],alpha=0.2)
				ax.plot(ys,clustersColours[clusterId],alpha=0.2)

		## remove the first row of zeroes
		dataGrilla = dataGrilla[1:,:]
		meanData = dataGrilla.mean(axis=0)
		x = linspace(1, framesNumber, framesNumber)
		s = UnivariateSpline(x, meanData[0:framesNumber], s=0)
		xs = linspace(1, framesNumber, framesNumber*1000)
		ys = s(xs)			
		#ax.plot(meanData[0:framesNumber],clustersColours[clusterId],linewidth=4)
		ax.plot(ys,clustersColours[clusterId],linewidth=4)
		ax.set_xlim(0, 1000*framesNumber-1)		
		#ax.set_xlim(0, 20)
		ax.set_ylim(minData,maxData)
		rfe.graficaGrilla(dataGrilla, outputFolder+'Grilla_'+str(clusterId)+'.png', framesNumber, clustersColours[clusterId], xSize, ySize)
		figCluster = plt.figure()
		axCluster = figCluster.add_subplot(111)
		for curve in range(dataGrilla.shape[0]):
			x = linspace(1, framesNumber, framesNumber)
			s = UnivariateSpline(x, dataGrilla[curve,0:framesNumber], s=0)
			xs = linspace(1, framesNumber, framesNumber*1000)
			ys = s(xs)
			#axCluster.plot(dataGrilla[curve,0:framesNumber],clustersColours[clusterId],alpha=0.2)
			#axCluster.plot(meanData[0:framesNumber],clustersColours[clusterId],linewidth=4)
			axCluster.plot(ys,clustersColours[clusterId],alpha=0.2)
			x = linspace(1, framesNumber, framesNumber)
			s = UnivariateSpline(x, meanData[0:framesNumber], s=0)
			xs = linspace(1, framesNumber, framesNumber*1000)
			ys = s(xs)
			axCluster.plot(ys,clustersColours[clusterId],linewidth=4)
		
		axCluster.set_xlim(0, 1000*framesNumber-1)
		#axCluster.set_xlim(0, framesNumber)
		axCluster.set_ylim(minData,maxData)
		figCluster.savefig(outputFolder+'cluster_'+str(clusterId)+'.png', bbox_inches='tight')
	
		ax3D.view_init(elev=10., azim=180)
		fig3D.savefig(outputFolder+'3D_180_cluster_'+str(clusterId)+'.png', bbox_inches='tight')
		ax3D.view_init(elev=10., azim=90)
		fig3D.savefig(outputFolder+'3D_90_cluster_'+str(clusterId)+'.png', bbox_inches='tight')
		ax3D.view_init(elev=10., azim=0)
		fig3D.savefig(outputFolder+'3D_0_cluster_'+str(clusterId)+'.png', bbox_inches='tight')

		
	# remove the first row of zeroes
	dataFile = dataFile[1:,:]
	savetxt(outputFolder+'outputFile.csv',dataFile, fmt='%s', delimiter=',', newline='\n')
	savetxt(outputFolder+'labels.csv',units,fmt='%s',delimiter=',', newline='\n')
	
	#Estimate fit for the clusterings
	fit = metrics.silhouette_score(data, labels, metric='euclidean')
	ax.text(0.01, 0.01, 'Silhouette score: '+str(round(fit,4)),
		verticalalignment='bottom', horizontalalignment='left',
		transform=ax.transAxes,
		color='green', fontsize=15)
	fig.savefig(outputFolder+clusteringAlgorithm+'_media.png', bbox_inches='tight')
		
	rfe.guardaClustersIDs(outputFolder, units, labels, 'clusterings.csv')

	return 0

if __name__ == '__main__':
	main()
