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
from sklearn.cluster import SpectralClustering
import argparse #argument parsing
import numpy as np
import scipy.ndimage
from sklearn.decomposition import PCA
from sklearn import metrics

clustersColours = ['#fcfa00', '#ff0000', '#820c2c', '#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff','#0c820e','#28ea04','#ea8404','#c8628f','#6283ff','#5b6756','#0c8248','k','#820cff','#932c11','#002c11','#829ca7']

def main():
	
	parser = argparse.ArgumentParser(prog='kmeans_scikit.py',
	 description='Performs K-means using scikit-learn',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='Source folder',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	parser.add_argument('--clustersNumber',
	 help='Number of clusters',
	 type=int, default='5', choices=[3,4,5,6,7,8,9,10,11,12,13,14,15], required=False)
	parser.add_argument('--framesNumber',
	 help='Number of frames used in STA analysis',
	 type=int, default='20', required=False)
	parser.add_argument('--pcaComponents',
	 help='Number of components for PCA',
	 type=int, default='4', required=False)
	parser.add_argument('--doPCA',
	 help='Performs clusterings with PCA or not',
	 type=bool, default=False, required=False)

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
	
	#dataCluster stores the data to be used for the clustering process
	#the size is equal to the number of frames, aka, the time component
	#plus 5 as we are incorporating the 2 dimensions of the ellipse,
	#x position, y position and angle
	dataCluster = np.zeros((1,framesNumber+5))
	units=[]
	dato=np.zeros((1,1))
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			unitName = unitFile.rsplit('_', 1)[0]
			dataUnit, coordinates = rfe.loadSTACurve(sourceFolder,unitFile,unitName)
			xSize = dataUnit.shape[0]
			ySize = dataUnit.shape[1]
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			#should we use the not-gaussian-fitted data for clustering?
			dataUnitGauss = scipy.ndimage.gaussian_filter(dataUnit[coordinates[0][0],[coordinates[1][0]],:],2)
			#A radius of the RF ellipse
			dato[0]=fitResult[0][2]
			dataUnitCompleta = np.concatenate((dataUnitGauss,dato),1)
			#B radius of the RF ellipse
			dato[0]=fitResult[0][3]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#angle of the RF ellipse
			dato[0]=fitResult[0][1]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#X coordinate of the RF ellipse
			dato[0]=fitResult[0][4]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			#Y coordinate of the RF ellipse
			dato[0]=fitResult[0][5]
			dataUnitCompleta = np.concatenate((dataUnitCompleta,dato),1)
			dataCluster = np.append(dataCluster,dataUnitCompleta, axis=0)
			units.append(unitName)
	# remove the first row of zeroes
	dataCluster = dataCluster[1:,:]	
	
	data = dataCluster[:,0:framesNumber+2]	
	sc = SpectralClustering(n_clusters=clustersNumber, eigen_solver=None, random_state=None,  n_init=10, gamma=1.0, affinity='nearest_neighbors', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
	sc.fit(data)
	labels = sc.labels_
	fit = metrics.silhouette_score(data, labels, metric='euclidean')
	rfe.graficaCluster(labels, dataCluster[:,0:framesNumber-1], outputFolder+'no_pca.png',clustersColours, fit)
	

	# generate graphics of all ellipses
	for clusterId in range(clustersNumber):
		dataGrilla = np.zeros((1,framesNumber+5))
		for unitId in range(dataCluster.shape[0]):
			if labels[unitId] == clusterId:
				datos=np.zeros((1,framesNumber+5))
				datos[0]=dataCluster[unitId,:]
				dataGrilla = np.append(dataGrilla,datos, axis=0)
		# remove the first row of zeroes
		dataGrilla = dataGrilla[1:,:]
		rfe.graficaGrilla(dataGrilla,outputFolder+'Grilla_'+str(clusterId)+'.png',clustersColours[clusterId],framesNumber,xSize,ySize)
		rfe.graficaCluster(labels, dataGrilla[:,0:framesNumber-1], outputFolder+'cluster_'+str(clusterId)+'.png',clustersColours[clusterId])
	
	rfe.guardaClustersIDs(outputFolder,units,labels,outputFolder+'clustering_no_pca.csv')
	
	if args.doPCA:
		pca = PCA(n_components=args.pcaComponents)
		newData = pca.fit_transform(data)
		sc.fit(newData)
		fit = metrics.silhouette_score(newData, labels, metric='euclidean')
		rfe.graficaCluster(labels, dataCluster[:,0:framesNumber-1], outputFolder+'pca.png',clustersColours,fit)	
		rfe.guardaClustersIDs(outputFolder,units,labels,outputFolder+'clustering_pca.csv')
	
	return 0

if __name__ == '__main__':
	main()
