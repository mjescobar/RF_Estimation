#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kmeans_scikit.py
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

# Performs K-means using scikit-learn

import rfestimationLib	as rfe
import sys    # system lib
import os     # operative system lib
from sklearn.cluster import KMeans
import argparse #argument parsing
import numpy as np
import scipy.ndimage
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 	  # plot lib (for figures)

def graficaCluster(labels, data, name):
	
	plt.figure()
	for curve in range(data.shape[0]):
		if labels[curve] == 0:
			plt.plot(data[curve,:],'r')
		if labels[curve] == 1:
			plt.plot(data[curve,:],'g')
		if labels[curve] == 2:
			plt.plot(data[curve,:],'b')
		if labels[curve] == 3:
			plt.plot(data[curve,:],'c')
		if labels[curve] == 4:
			plt.plot(data[curve,:],'m')
		if labels[curve] == 5:
			plt.plot(data[curve,:],'k')
		if labels[curve] == 6:
			plt.plot(data[curve,:],'y')
		if labels[curve] == 7:
			plt.plot(data[curve,:],'#d2691e')

	plt.savefig(name)
	plt.close()
	
	return 0

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
	 type=int, default='5', required=False)
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
	
	data = np.zeros((1,framesNumber))
	units=[]
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			unitName = unitFile.rsplit('_', 1)[0]
			dataUnit, coordinates = rfe.loadSTACurve(sourceFolder,unitFile,unitName)
			dataUnitGauss = scipy.ndimage.gaussian_filter(dataUnit[coordinates[0][0],[coordinates[1][0]],:],2)
			data = np.append(data,dataUnitGauss, axis=0)
			units.append(unitName)
	# data es normalizado
	data = data[1:,:]
	
	km = KMeans(init='k-means++', n_clusters=clustersNumber, n_init=10,n_jobs=-1)
	km.fit(data)
	
	# Genero output 
	print 'Labels No PCA '
	indice = 0
	for unit in units:
		print unit,",",km.labels_[indice]
		indice+=1
	
	graficaCluster(km.labels_, data, outputFolder+'no_pca.png')
	if args.doPCA:
		pca = PCA(n_components=args.pcaComponents)
		newData = pca.fit_transform(data)
		km.fit(newData)
		print 'Labels PCA    ',km.labels_
		graficaCluster(km.labels_, data, outputFolder+'pca.png')	
	
	return 0

if __name__ == '__main__':
	main()

