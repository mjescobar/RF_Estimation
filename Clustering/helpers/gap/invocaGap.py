#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  invocaGap.py
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

import sys, os 
#Relative path for RFE LIB
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe				#Some custom functions
import argparse 							#argument parsing
import gap as gap
from numpy import zeros
from numpy import empty
from numpy import concatenate
from math import pi
from numpy import append
from numpy import float64
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

def main():
	parser = argparse.ArgumentParser(prog='invocaGap.py',
	 description='Testing gap staticstics',
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
		print ''
		sys.exit()

	#Output folder for the graphics and files
	outputFolder = rfe.fixPath(args.outputFolder)
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except:
			print ''
			print 'Unable to create folder ' + outputFolder
			print ''
			sys.exit()
		
	#dataCluster stores the data to be used for the clustering process
	#the size is equal to the number of frames, aka, the time component
	#plus 5 as we are incorporating the 2 dimensions of the ellipse, 
	#x position, y position and angle
	dataCluster = zeros((1,27))
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
	
	data = dataCluster[:,0:19]
	data = data.astype(float64, copy=False)
	
	gaps = gap.gap(data, refs=None, nrefs=len(data), ks=range(1,10))

	dgap = zeros(len(gaps))
	for i in range(len(gaps)-1):
		dgap[i] = gaps[i]-gaps[i+1]
	
	plt.plot(gaps)
	plt.show()
	
	plt.plot(dgap)
	plt.show()
	
	return 0

if __name__ == '__main__':
	main()

