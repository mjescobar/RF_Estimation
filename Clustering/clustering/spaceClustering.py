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
import argparse #argument parsing
import numpy as np
from sklearn.cluster import KMeans

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
	
	units = []
	data = []
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):
			unitName = unitFile.rsplit('_', 1)[0]
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			radiusA = fitResult[0][2]
			radiusB = fitResult[0][3]
			data.append([radiusA,radiusB])
			units.append(unitName)

	km = KMeans(init='k-means++', n_clusters=2, n_init=10,n_jobs=-1)
	km.fit(data)
	labels = km.labels_
	
	smallUnits = []
	largeUnits = []
	fileSmall = open(outputFolder+'clusterSmall.csv', "w")
	fileLarge = open(outputFolder+'clusterLarge.csv', "w")
	for unit in range(labels.size):
		if labels[unit] == 0:
			fileSmall.write(units[unit]+'\n')
		else:
			fileLarge.write(units[unit]+'\n')

	fileSmall.close
	fileLarge.close
		
	return 0

if __name__ == '__main__':
	main()
