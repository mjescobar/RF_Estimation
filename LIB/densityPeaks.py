#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  densityPeaks.py
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
#  Implements (as library)
#  Clustering by fast search and find of density peaks
#  Alex Rodriguez, Alessandro Laio
#  http://www.sciencemag.org/content/344/6191/1492.short

import numpy as np
ridiculouslyHighNumber = 1000000

#  
#  Calculate the distance
#  
def X(dij, dc):
	if dij - dc < 0:
		return 1
	else:
		return 0
#  
#  For each data point calculate the distances
#  
def calculateDistance(data, length):
	#  Calculate the distance between all the data points
	
	#  ToDo Optimise calculation as it's symetrical
		
	distances = np.zeros((length,length))
	for x in range(length):
		for y in range(length):
			distances[x][y] = np.linalg.norm(data[x]-data[y])
	
	return distances

#  
#  Calculate the mimimum distance
#  
def delta(distances, densities, length, i):
	minDistance = ridiculouslyHighNumber    # ridiculously high number
	
	density = densities[i]
		
	for j in range(length):
		if densities[j] > density:
			if distances[i][j] < minDistance:
				minDistance = distances[i][j]
		
	return minDistance

#  
#  Perform the prediction
#  
def predict(data, dc):
	length = data.shape[0]
	
	distances = calculateDistance(data, length)
	
	print distances
	
	densities = np.zeros((length))
	for i in range(length):
		for j in range(length):
			densities[i] = densities[i] + X(distances[i][j],dc)

	deltas = np.zeros((length))
	for i in range(length):
		deltas[i] = delta(distances, densities, length, i)
	
	# Spot the clusters centers
	clustersCenters = []
	for i in range(length):
		if deltas[i] == ridiculouslyHighNumber:
			clustersCenters.append(i)
		
	labels = np.zeros((length))
	for i in range(length):
		currentDistance = ridiculouslyHighNumber
		for j in clustersCenters:
			if distances[i][j] < currentDistance:
				currentDistance = distances[i][j]
				labels[i] = clustersCenters.index(j)

	return (len(clustersCenters), labels)
