#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pca.py
#  
#  Copyright 2014 Carlos "casep" Sepulveda <casep@fedoraproject.org>
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

import sys    # system lib
import os     # operative system lib
import matplotlib.pyplot as plt
import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)
import numpy
import matplotlib.pyplot as plt 	  # plot lib (for figures)

parser = argparse.ArgumentParser(prog='pca.py',
 description='Performs PCA',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
 help='Source folder',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output folder',
 type=str, required=True)
args = parser.parse_args()

#Source folder of the files with the timestamps
sourceFolder = args.sourceFolder
# Check for trailing / on the folder
if sourceFolder[-1] != '/':
	sourceFolder+='/'

if not os.path.exists(sourceFolder):
	print ''
	print 'Source folder does not exists ' + sourceFolder
	sys.exit()

#Source folder of the files with the timestamps
outputFolder = args.outputFolder
# Check for trailing / on the folder
if outputFolder[-1] != '/':
	outputFolder+='/'

if not os.path.exists(outputFolder):
	try:
		os.makedirs(outputFolder)
	except:
		print ''
		print 'Unable to create folder ' + outputFolder
		sys.exit()
		
def loadVarMatrix(sourceFolder,unitFile,unitName):
	# The STA matrix is named as M8a_lineal/sta_array_M8a.mat
	staMatrixFile = scipy.io.loadmat(sourceFolder+unitFile+'/sta_array_'+unitName+'.mat')
	staMatrix = staMatrixFile['STA_array']
	# STA matrix shaped (31, 31, 20) 
	# x,y,z; x=pixel width, y=pixel heigth, z=number of images
	xLength = staMatrix.shape[0]
	yLength = staMatrix.shape[1]
	result = numpy.zeros((xLength,yLength))
	for xAxis in range(xLength):
		for yAxis in range(yLength):
			result[xAxis][yAxis] = numpy.var(staMatrix[xAxis,yAxis,:])
	coordinates = numpy.where(result==numpy.amax(result))
#	print numpy.amax(result)
#	print numpy.std(result)
	print numpy.var(numpy.histogram(result)[0])
	
	return staMatrix[coordinates[0][0],[coordinates[1][0]],:]

def plotImages(data, unitName):
	lenData = len(data[0])	
	plt.figure()
	plt.plot(numpy.linspace(1,lenData,lenData),data[0],linestyle="dashed", marker="o", color="green")
	plt.savefig(outputFolder+unitName+".png",format='png', bbox_inches='tight')
	plt.close()

	return 0

def main():
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			unitName = unitFile.rsplit('_', 1)[0]
			print unitName
			loadVarMatrix(sourceFolder,unitFile,unitName)
			#plotImages(loadVarMatrix(sourceFolder,unitFile,unitName), unitName)
			
	return 0

if __name__ == '__main__':
	main()
