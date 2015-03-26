#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spaceClustering.py
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

# Performs basic clustering based on the size of the RF

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../..','LIB'))
import rfestimationLib as rfe
import argparse 					# argument parsing
import numpy as np					# Numpy
import densityPeaks as dp
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

clustersColours = ['blue', 'red', 'green', 'orange', 'black','yellow', \
				'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
				'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
				'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
				'#5b6756','#0c8248','k','#820cff','#932c11', \
				'#002c11','#829ca7']

def main():
	
	parser = argparse.ArgumentParser(prog='spaceClustering.py',
	 description='Performs basic clustering based on the size of th RF',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='Source folder',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	parser.add_argument('--percentage',
	 help='Percentage used to calculate the distance',
	 type=float, default='2', required=False)
	parser.add_argument('--xSize',
	 help='X size of the stimuli',
	 type=int, default='31', required=False)
	parser.add_argument('--ySize',
	 help='Y size of the stimuli',
	 type=int, default='31', required=False)
	 
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
	
	units = []
	dataCluster = np.zeros((1,7))
	for unitFile in sorted(os.listdir(sourceFolder)):
		if os.path.isdir(sourceFolder+unitFile):
			unitName = unitFile.rsplit('_', 1)[0]
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			dataCluster = np.vstack((dataCluster,[fitResult[0][2],fitResult[0][3],fitResult[0][1],fitResult[0][4],fitResult[0][5],fitResult[0][2]*fitResult[0][3]*3,(fitResult[0][2]+fitResult[0][3])/2]))
			units.append(unitName)
	# remove the first row of zeroes
	dataCluster = dataCluster[1:,:]	

	percentage = args.percentage    #exploratory, '...for large data sets, the results of the analysis are robust with respect to the choice of d_c'
	# Area instead o Radius
	#clustersNumber, labels = dp.predict(dataCluster[:,0:2], percentage)
	clustersNumber, labels = dp.predict(dataCluster[:,5:7], percentage)
	
	
	for clusterId in range(clustersNumber):
		clusterFile = open(outputFolder+'cluster_'+str(clusterId)+'.csv', "w")
		for unit in range(labels.size):
			if labels[unit] == clusterId:
				clusterFile.write(units[unit]+'\n')
		clusterFile.close
	
	xSize = args.xSize
	ySize = args.ySize
	# generate graphics of all ellipses
	for clusterId in range(clustersNumber):
		dataGrilla = np.zeros((1,7))
		for unitId in range(dataCluster.shape[0]):
			if labels[unitId] == clusterId:
				datos=np.zeros((1,7))
				datos[0]=dataCluster[unitId,:]
				dataGrilla = np.append(dataGrilla,datos, axis=0)
		## remove the first row of zeroes
		dataGrilla = dataGrilla[1:,:]

		rfe.graficaGrilla(dataGrilla, outputFolder+'Grilla_'+str(clusterId)+'.png', 0, clustersColours[clusterId], xSize, ySize)

	return 0

if __name__ == '__main__':
	main()
