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
from scipy.spatial import distance
import math
import heapq
import sys

#  
#  For each data point calculate the distances
#  
def calculateDistance(data, length):
	#  Calculate the distance between all the data points
	
	#  ToDo Optimise calculation as it's symetrical
		
	distances = np.zeros((length,length))
	for x in range(length):
		for y in range(length):
			distances[x][y] = distance.cdist(data[x][np.newaxis,:], data[y][np.newaxis,:], 'euclidean')
	return distances

#  
#  Perform the prediction
#  
def predict(data, percentage):
	length = data.shape[0]
	
	distances = calculateDistance(data, length)	
	
	sortedDistances = sorted(set(distances.ravel()))[1:]
	
	position=int(math.ceil(len(sortedDistances)*percentage/100.))
	dcs = heapq.nsmallest(position, sortedDistances)[position-1]
	dc = dcs

	densities = np.zeros((length))
	for i in range(length-1):
		for j in range(i):
			densities[i] += math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
			densities[j] += math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
	
	ordDensities = (-np.array(densities)).argsort()
	
	deltas = np.zeros((length))
	deltas[ordDensities[0]] = -1

	maxDistance = np.amax(distances)

	for x in range(1,length):
		deltas[ordDensities[x]] = maxDistance
		for y in range(x-1):
			if distances[ordDensities[x],ordDensities[y]] < deltas[ordDensities[x]]:
				deltas[ordDensities[x]] = distances[ordDensities[x],ordDensities[y]]

	# Al punto de mayor densidad le asigno la mayor distancia calculada para un punto
	deltas[ordDensities[0]] = np.amax(deltas)

	ordDeltas = sorted(deltas)

	previousDistance = ordDeltas[-1]
	clustersCenters = []
	for cluster in np.where(deltas==ordDeltas[-1])[0]:
				clustersCenters.append(cluster)

	for i in range(len(clustersCenters),length):
		iDistance = ordDeltas[-i] - ordDeltas[-i-1]
		if iDistance >= (previousDistance*45/100):
			break
		else:
			for cluster in np.where(deltas==ordDeltas[-i-1])[0]:
				clustersCenters.append(cluster)
			previousDistance = iDistance
	
	labels = np.zeros((length))
	for i in range(length):
		currentDistance = 2 * maxDistance
		for j in clustersCenters:
			if distances[i][j] < currentDistance:
				currentDistance = distances[i][j]
				labels[i] = clustersCenters.index(j)

	import matplotlib.pyplot as plt
	plt.plot(densities,deltas,'ro')
	plt.savefig('/tmp/densitiesvsdeltas.png', bbox_inches='tight')
	plt.close()
	
	return (len(clustersCenters), labels)
