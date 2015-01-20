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
	print 'position',position

	dcs = heapq.nsmallest(position, sortedDistances)[position-1]
	print 'dc_s',dcs

	dcl = heapq.nlargest(position, sortedDistances)[position-1]
	print 'dc_l',dcl

	dcss = sortedDistances[position]
	print 'dc_sorted',dcss

	dc = dcs

	densities = np.zeros((length))
	print 'length',length
	for i in range(length-1):
		for j in range(i):
			densities[i] += math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
			densities[j] += math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
	
	print 'densities',densities[:-1]
	ordDensities = (-np.array(densities)).argsort()
	
	deltas = np.zeros((length))
	deltas[ordDensities[0]] = -1

	maxDistance = np.amax(distances)

	for x in range(1,length):
		deltas[ordDensities[x]] = maxDistance
		for y in range(x-1):
			print 'x',x,'y',y
			print 'ordDensities[x]',ordDensities[x]
			print 'ordDensities[y]',ordDensities[y]
			print 'distances', distances[ordDensities[x],ordDensities[y]]
			print 'deltas',deltas[ordDensities[x]]
			if distances[ordDensities[x],ordDensities[y]] < deltas[ordDensities[x]]:
				deltas[ordDensities[x]] = distances[ordDensities[x],ordDensities[y]]

	#maxDistance = np.amax(distances)
	#for i in range(length):
	#	deltas[i] = maxDistance
	#	for j in range(i):
	#		if densities[j] > densities[i]:
	#			if distances[i][j] < deltas[i]:
	#				deltas[i] = distances[i][j]

	# Al punto de mayor densidad le asigno la mayor distancia calculada para un punto
	ordDeltas = sorted(deltas)
	deltas[np.where(deltas==ordDeltas[-1])[0]] = ordDeltas[-2]
	ordDeltas = sorted(deltas)

	previousDistance = ordDeltas[-1]
	#print 'densities',densities
	print 'deltas',deltas
	print 'ordDeltas',ordDeltas
	clustersCenters = []
	for cluster in np.where(deltas==ordDeltas[-1])[0]:
				clustersCenters.append(cluster)

	for i in range(len(clustersCenters),length):
		iDistance = ordDeltas[-i] - ordDeltas[-i-1]
		if iDistance >= (previousDistance*30/100):
			break
		else:
			for cluster in np.where(deltas==ordDeltas[-i-1])[0]:
				clustersCenters.append(cluster)
			previousDistance = iDistance
	
	#clustersCenters = np.unique(clustersCenters)

	print 'clustersCenters',clustersCenters

	labels = np.zeros((length))
	for i in range(length):
		currentDistance = 2 * maxDistance
		for j in clustersCenters:
			#print 'i',i,'j',j,distances[i][j]
			if distances[i][j] < currentDistance:
				currentDistance = distances[i][j]
				#print 'labels ',i,' cluster ',j
				labels[i] = clustersCenters.index(j)
		#print ''
	print 'labels',labels

	import matplotlib.pyplot as plt
	plt.plot(densities,deltas,'ro')
	plt.savefig('/tmp/densitiesvsdeltas_unsorted.png', bbox_inches='tight')
	plt.close()
	
	return (len(clustersCenters), labels)
