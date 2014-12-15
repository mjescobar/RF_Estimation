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
#  Calculate the mimimum distance
#  
def delta(distances, densities, length, i,clustersCenters):
	minDistance = ridiculouslyHighNumber    # ridiculously high number
	
	density = densities[i]
		
	for j in range(length):
		if densities[j] > density:
			if distances[i][j] < minDistance:
				minDistance = distances[i][j]
	
	# A Super dense point has been found
	if minDistance == ridiculouslyHighNumber:
		maxDistance = 0
		for j in range(length):
			if distances[i][j] > maxDistance:
				maxDistance = distances[i][j]
		minDistance = maxDistance
		clustersCenters.append(i)
	
	return minDistance

#  
#  Perform the prediction
#  
def predict(data, dc):
	length = data.shape[0]
	
	distances = calculateDistance(data, length)	
	
	densities = np.zeros((length))
	for i in range(length-1):
		for j in range(i+1,length):
			densities[i] = densities[i] + math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
			densities[j] = densities[j] + math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
	
	deltas = np.zeros((length))
	maxDistance = np.amax(distances)
	for i in range(length):
		deltas[i] = maxDistance
		for j in range(length):
			if densities[j] > densities[i]:
				if distances[i][j] < deltas[i]:
					deltas[i] = distances[i][j]

	# Al punto de mayor densidad le asigno la mayor distancia calculada para un punto
	ordDeltas = sorted(deltas)
	deltas[np.where(deltas==ordDeltas[-1])[0]] = ordDeltas[-2]
	
	previousDistance = ordDeltas[-2]
	clustersCenters = []
	for i in range(1,length):
		print i
		print 'previousDistance',previousDistance
		print 'ordDeltas[-i] - ordDeltas[-i-1]',ordDeltas[-i-1] - ordDeltas[-i-2]
		print 'ordDeltas[-i]',ordDeltas[-i-1]
		print 'ordDeltas[-i-1]',ordDeltas[-i-2]
		iDistance = ordDeltas[-i-1] - ordDeltas[-i-2]
		if (3. * iDistance) <= previousDistance:
			break
		else:
			print np.where(deltas==ordDeltas[-i-1])
			print np.where(deltas==ordDeltas[-i-1])[0]
			for cluster in np.where(deltas==ordDeltas[-i-1])[0]:
				clustersCenters.append(cluster)
			previousDistance = iDistance
	
	print clustersCenters
	
	labels = np.zeros((length))
	for i in range(length):
		currentDistance = maxDistance
		for j in clustersCenters:
			if distances[i][j] <= currentDistance:
				currentDistance = distances[i][j]
				labels[i] = clustersCenters.index(j)
	
	import matplotlib.pyplot as plt
	from operator import itemgetter
	list1, list2 = (list(x) for x in zip(*sorted(zip(densities, deltas), key=lambda pair: pair[0])))
	plt.plot(list1,list2,'ro')
	plt.savefig('/tmp/densitiesvsdeltas.png', bbox_inches='tight')
	plt.close()
	
	plt.plot(densities,deltas,'ro')
	plt.savefig('/tmp/densitiesvsdeltas_unsorted.png', bbox_inches='tight')
	plt.close()
	
	return (len(clustersCenters), labels)
