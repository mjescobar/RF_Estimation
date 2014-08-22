#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  onOffClassification.py
#  
#  Copyright 2014 
#  Monica Otero <monicaot2001@gmail.com>
#  Carlos "casep" Sepulveda <casep@fedoraproject.org>
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

# Genera clasificacion unidades on-off u off-on dependiendo de ocurrencia
# minimo y maximo y además el frame dde se alcanzó este min/max

import sys    # system lib
import os     # operative system lib
import matplotlib.pyplot as plt
import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)
import numpy
import matplotlib.pyplot as plt 	  # plot lib (for figures)
import scipy.ndimage
from scipy.cluster.vq import kmeans,vq
from pylab import plot,show

parser = argparse.ArgumentParser(prog='onOffClassification.py',
 description='Classify On-Off or Off-On units',
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

def loadFitMatrix(sourceFolder,unitFile):
	firResultFile = scipy.io.loadmat(sourceFolder+unitFile+'/fit_var.mat')
	firResult = firResultFile['fitresult']
	
	return firResult

def main():
	
	file = open(outputFolder+'onOff.csv', "w")
	
	header = 'Unidad\t'+'OnOff\t'+'PeekFrame''\n'
	file.write(header)
	maxDataSTAValue = 0
	minDataSTAValue = 0
	for unitFile in os.listdir(sourceFolder):
		unitName = unitFile.rsplit('_', 1)[0]
		if os.path.isdir(sourceFolder+unitFile):
			# The STA matrix is named as M8a_lineal/sta_array_M8a.mat
			staMatrixFile = scipy.io.loadmat(sourceFolder+unitFile+'/sta_array_'+unitName+'.mat')
			staMatrix = staMatrixFile['STA_array']
			xLength = staMatrix.shape[0]
			yLength = staMatrix.shape[1]
			result = numpy.zeros((xLength,yLength))
			maxDataSTAValue = 0
			minDataSTAValue = 0
			for xAxis in range(xLength):
				for yAxis in range(yLength):
					dataSTA = staMatrix[xAxis,yAxis,:]
					maxDataSTAtmp = numpy.amax(staMatrix[xAxis,yAxis,:])
					minDataSTAtmp = numpy.amin(staMatrix[xAxis,yAxis,:])
					if maxDataSTAtmp > maxDataSTAValue:
						maxDataSTAValue = maxDataSTAtmp
						maxDataSTAId = numpy.where(maxDataSTAValue==dataSTA)
					if minDataSTAtmp <  minDataSTAValue:
						minDataSTAValue = minDataSTAtmp
						minDataSTAId = numpy.where(minDataSTAValue==dataSTA)
			if maxDataSTAId[0] > minDataSTAId[0]:
				linea = '"'+unitName+'"\t"On"\t"'+ str(maxDataSTAId[0]+1) + '\n'
			else:
				linea = '"'+unitName+'"\t"Off"\t"'+ str(minDataSTAId[0]+1) + '\n'
			file.write(linea)
	file.close
	return 0

if __name__ == '__main__':
	main()

