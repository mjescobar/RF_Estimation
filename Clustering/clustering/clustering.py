#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SpectralClustering.py
#  
#  Copyright 2014 Carlos "casep" Sepulveda <casep@alumnos.inf.utfsm.cl>
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

# Performs SpectralClustering using scikit-learn

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../..','LIB'))
import rfestimationLib as rfe
import argparse #argument parsing
import numpy as np
import scipy.ndimage
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn import preprocessing
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import mlab as mlab

clustersColours = ['#fcfa00', '#ff0000', '#820c2c', '#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff','#0c820e','#28ea04','#ea8404','#c8628f','#6283ff','#5b6756','#0c8248','k','#820cff','#932c11','#002c11','#829ca7']
clustersColours = ['blue', 'red', 'green', 'yellow', 'black','orange','#ff006f','#00e8ff']

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
	 type=str, default='kmeans', choices=['kmeans','spectral','gmm'], required=False)
	 
	args = parser.parse_args()

	#Source folder of the files with the timestamps
	sourceFolder = rfe.fixPath(args.sourceFolder)
	if not os.path.exists(sourceFolder):
		print ''
		print 'Source folder does not exists ' + sourceFolder
		sys.exit()

	#Output folder for the graphics
	outputFolder = rfe.fixPath(args.outputFolder)
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except:
			print ''
			print 'Unable to create folder ' + outputFolder
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
	#plus 7 as we are incorporating the 2 dimensions of the ellipse, 
	#2 dimensions of the ellipse on micrometres,
	#x position, y position and angle
	dataCluster = np.zeros((1,framesNumber+7))
	units = []
	dato = np.zeros((1,1))
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			unitName = unitFile.rsplit('_', 1)[0]
			dataUnit, coordinates = rfe.loadSTACurve(sourceFolder,unitFile,unitName)
			xSize = dataUnit.shape[0]
			ySize = dataUnit.shape[1]
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			#should we use the not-gaussian-fitted data for clustering?
			dataUnitGauss = scipy.ndimage.gaussian_filter(dataUnit[coordinates[0][0],[coordinates[1][0]],:],2)

			# Standarisation
			dataMedia = dataUnitGauss[0].mean(axis=0)
			dataStd = dataUnitGauss[0].std(axis=0)
			featureRange = [dataMedia-dataStd, dataMedia+dataStd]
			minMaxScaler = preprocessing.MinMaxScaler(featureRange)
			dimensionsToScale = np.array([fitResult[0][2], fitResult[0][3]])
			dimensionsScaled = minMaxScaler.fit_transform(dimensionsToScale)
			#A radius of the RF ellipse, adjusted to micrometres and scaled
			dato[0] = dimensionsScaled[0]
			dataUnitCompleta = np.concatenate((dataUnitGauss,dato),1)
			#B radius of the RF ellipse, adjusted to micrometres
			dato[0] = dimensionsScaled[1]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#A radius of the RF ellipse
			dato[0] = fitResult[0][2]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#B radius of the RF ellipse
			dato[0] = fitResult[0][3]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#angle of the RF ellipse
			dato[0] = fitResult[0][1]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#X coordinate of the RF ellipse
			dato[0] = fitResult[0][4]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#Y coordinate of the RF ellipse
			dato[0] = fitResult[0][5]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			dataCluster = np.append(dataCluster,dataUnitCompleta, axis=0)
			units.append(unitName)
	# remove the first row of zeroes
	dataCluster = dataCluster[1:,:]	
		
	#Solo temporal dataCluster[:,0:framesNumber]
	#Temporal y espacial dataCluster[:,0:framesNumber+2]
	data = dataCluster[:,0:framesNumber+2]
	
	if clusteringAlgorithm == 'spectral':
		from sklearn.cluster import SpectralClustering
		sc = SpectralClustering(n_clusters=clustersNumber, eigen_solver=None, random_state=None,  n_init=10, gamma=1.0, affinity='nearest_neighbors', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
		sc.fit(data)
		labels = sc.labels_
	elif clusteringAlgorithm == 'gmm':
		from sklearn import mixture
		gmix = mixture.GMM(n_components=clustersNumber, covariance_type='spherical')
		gmix.fit(data)
		labels = gmix.predict(data)
	else:
		from sklearn.cluster import KMeans
		km = KMeans(init='k-means++', n_clusters=clustersNumber, n_init=10,n_jobs=-1)
		km.fit(data)
		labels = km.labels_

	#fit = metrics.silhouette_score(data, labels, metric='euclidean')
	#rfe.graficaCluster(labels, dataCluster[:,0:framesNumber-1], outputFolder+clusteringAlgorithm+'.png', clustersColours, fit)
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# generate graphics of all ellipses
	for clusterId in range(clustersNumber):
		dataGrilla = np.zeros((1,framesNumber+7))
		for unitId in range(dataCluster.shape[0]):
			if labels[unitId] == clusterId:
				
				datos=np.zeros((1,framesNumber+7))
				datos[0]=dataCluster[unitId,:]
				dataGrilla = np.append(dataGrilla,datos, axis=0)
				ax.plot(dataCluster[unitId,0:framesNumber-1],clustersColours[clusterId],alpha=0.2)
		## remove the first row of zeroes
		dataGrilla = dataGrilla[1:,:]
		meanData = dataGrilla.mean(axis=0)			
		ax.plot(meanData[0:framesNumber-1],clustersColours[clusterId],linewidth=4)
		rfe.graficaGrilla(dataGrilla, outputFolder+'Grilla_'+str(clusterId)+'.png', clustersColours[clusterId], framesNumber, xSize, ySize)
		figCluster = plt.figure()
		axCluster = figCluster.add_subplot(111)
		#rfe.graficaCluster(labels, dataGrilla[:,0:framesNumber-1], outputFolder+'cluster_'+str(clusterId)+'.png', clustersColours[clusterId])
		for curve in range(dataGrilla.shape[0]):
			axCluster.plot(dataGrilla[curve,0:framesNumber-1],clustersColours[clusterId],alpha=0.2)
			axCluster.plot(meanData[0:framesNumber-1],clustersColours[clusterId],linewidth=4)
		
		figCluster.savefig(outputFolder+'cluster_'+str(clusterId)+'.png')
	#Estimate fit for the clusterings
	fit = metrics.silhouette_score(data, labels, metric='euclidean')
	ax.text(0.01, 0.01, 'Silhouette score: '+str(round(fit,4)),
		verticalalignment='bottom', horizontalalignment='left',
		transform=ax.transAxes,
		color='green', fontsize=15)
	fig.savefig(outputFolder+clusteringAlgorithm+'_new.png')
	#plt.close()	
		
		
	rfe.guardaClustersIDs(outputFolder, units, labels, outputFolder+'clusterings.csv')

	return 0

if __name__ == '__main__':
	main()
