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
	
# 
# Genera la salida grafica para los clusters encontrados
# 
def graficaCluster(labels, data, name, colours, fit=None):
	import matplotlib
	matplotlib.use('Agg')
	from matplotlib import pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111)
	if isinstance(colours, str):
		for curve in range(data.shape[0]):
			ax.plot(data[curve,:],colours)
	else:
		for curve in range(data.shape[0]):
			ax.plot(data[curve,:],colours[labels[curve]])

	if fit:
		ax.text(0.01, 0.01, 'Silhouette score: '+str(round(fit,4)),
			verticalalignment='bottom', horizontalalignment='left',
			transform=ax.transAxes,
			color='green', fontsize=15)
	
	fig.savefig(name)
	plt.close()
	
	return 0

#
# Genera archivo .csv de unidades respecto clusters id
#
def guardaClustersIDs(outputFolder,units,labels, name):
	
	file = open(outputFolder+name, "w")
	header = '\"Unit\" \t \"ClusterID\"'+'\n'
	file.write(header)
	indice = 0
	for unit in units:
		linea = '\"'+unit+'\" \t'+str(labels[indice])+'\n'
		file.write(linea)
		indice+=1
	file.close
	
	return 0

def graficaGrilla(dataGrilla,name,colour,xPixels,yPixels):	
	from matplotlib.patches import Ellipse
	from pylab import figure, show, savefig

	fig = figure()
	ax = fig.add_subplot(111, aspect='equal')
	# Each row of dataGrilla contains 
	# N == "framesNumbers" , signal
	# A radius of the RF ellipse
	# B radius of the RF ellipse
	# Angle of the RF ellipse
	# X coordinate of the RF ellipse
	# Y coordinate of the RF ellipse

	ax = fig.add_subplot(111, aspect='equal')
	for unit in range(dataGrilla.shape[0]):
		eWidth = dataGrilla[unit][framesNumber-1+1]
		eHeight = dataGrilla[unit][framesNumber-1+2]
		eAngle = dataGrilla[unit][framesNumber-1+3]
		eXY = [dataGrilla[unit][framesNumber-1+4],  dataGrilla[unit][framesNumber-1+5]]
		e = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle)
		ax.add_artist(e)
		e.set_alpha(0.2)
		e.set_facecolor(colour)
	
	ax.set_xlim(0, xPixels)
	ax.set_ylim(0, yPixels)
	savefig(name, dpi=None, bbox_inches='tight')
	return 0
