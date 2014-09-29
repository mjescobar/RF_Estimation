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
import matplotlib.pyplot as plt 	  # plot lib (for figures)

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
	
# 
# Genera la salida grafica para los clusters encontrados
# 
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
			plt.plot(data[curve,:],'#6d19df')
		if labels[curve] == 8:
			plt.plot(data[curve,:],'#95e618')
		if labels[curve] == 9:
			plt.plot(data[curve,:],'#195ddf')
		if labels[curve] == 10:
			plt.plot(data[curve,:],'#e67f18')
		if labels[curve] == 11:
			plt.plot(data[curve,:],'#e64c18')
		if labels[curve] == 12:
			plt.plot(data[curve,:],'#e61864')
		if labels[curve] == 13:
			plt.plot(data[curve,:],'#e6189d')
		if labels[curve] == 14:
			plt.plot(data[curve,:],'#b718e6')
	
	plt.savefig(name)
	plt.close()
	
	return 0
