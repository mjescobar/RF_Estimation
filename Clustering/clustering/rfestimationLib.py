#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rfestimationLib.py
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

# Set of functions used on different codes of the project
# 

import numpy
import scipy.io 	      # input output lib (for save matlab matrix)
import platform				# Windows or Linux?

def fixPath(folderName):
	pathCharacter = returnPathCharacter()
	# Check for trailing / on the folder
	if folderName[-1] != pathCharacter:
		folderName+=pathCharacter
	
	return folderName
	
# 
# loadFitMatrix will recover the result of the gauss2dfitSTA script
# will return the matrix ready to use
def loadFitMatrix(sourceFolder,unitFile):
	pathCharacter = returnPathCharacter()
	
	firResultFileName = sourceFolder+unitFile+pathCharacter+'fit_var.mat'
	firResultFile = scipy.io.loadmat(firResultFileName)
	firResult = firResultFile['fitresult']
	
	return firResult
	
#
# loadSTACurve will load the curve, adjusted with a Gaussian filter.
# for the a unit previously processed with the STA code
def loadSTACurve(sourceFolder,unitFile,unitName):
	pathCharacter = returnPathCharacter()
	
	# The STA matrix is named as M8a_lineal/sta_array_M8a.mat
	staMatrixFile = scipy.io.loadmat(sourceFolder+unitFile+pathCharacter+'sta_array_'+unitName+'.mat')
	staMatrix = staMatrixFile['STA_array']

	# STA matrix shaped (xPixels, yPixels, nFrames) 
	# x,y,z; x=pixel width, y=pixel heigth, z=number of images
	xLength = staMatrix.shape[0]
	yLength = staMatrix.shape[1]
	result = numpy.zeros((xLength,yLength))
	maxDataSTAValue = 0
	for xAxis in range(xLength):
		for yAxis in range(yLength):
			dataSTA = staMatrix[xAxis,yAxis,:]
			maxDataSTAtmp = numpy.amax(numpy.abs(staMatrix[xAxis,yAxis,:]))
			if maxDataSTAtmp > maxDataSTAValue:
				maxDataSTAValue = maxDataSTAtmp
				maxDataSTAId = numpy.where(maxDataSTAValue==dataSTA)
			result[xAxis][yAxis] = numpy.var(dataSTA)
	coordinates = numpy.where(result==numpy.amax(result))

	return staMatrix, coordinates

#
# Determine which character use to path contatenation
# 
def returnPathCharacter():
	pathCharacter = '/'
	if platform.system() == 'Windows':
		pathCharacter = '\\'
	
	return pathCharacter
	
