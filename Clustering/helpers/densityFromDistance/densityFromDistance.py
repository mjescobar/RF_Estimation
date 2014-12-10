#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  densityFromDistance.py
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

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../..','LIB'))
import argparse #argument parsing
import numpy as np
import math

clustersColours = ['blue', 'red', 'green', 'orange', 'black','yellow', \
				'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
				'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
				'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
				'#5b6756','#0c8248','k','#820cff','#932c11', \
				'#002c11','#829ca7']
	
ridiculouslyHighNumber = 1000000

def X(dij, dc):
	x=0
	if (dij - dc) < 0:
		x=1
	
	return x
						
def calculateDistance(distancesFile,length):
	distances = np.zeros((length,length))
	f = open(distancesFile, 'r')
	for line in f:
		i,j,distancia = line.split()
		distances[int(i)-1][int(j)-1]=float(distancia)
		distances[int(j)-1][int(i)-1]=float(distancia)
	f.close()
	
	return distances

def delta(distances, densities, length, i,clustersCenters):
	maxDistance = np.amax(distances)
	
	minDistance = maxDistance
	
	density = densities[i]
	
	for j in range(i-1):
		if densities[j] > density:
			if distances[i][j] < minDistance:
				minDistance = distances[i][j]
	
	# A Super dense point has been found
	if minDistance == maxDistance:
		maxDistance = 0
		for j in range(length):
			if distances[i][j] > maxDistance:
				maxDistance = distances[i][j]
		minDistance = maxDistance
		clustersCenters.append(i)
	
	return minDistance
	
def predict(distancesFile, dc):
	length = 2000
	
	distances = calculateDistance(distancesFile,length)	
	
	densities = np.zeros((length))
	for i in range(length-1):
		for j in range(i+1,length):
			densities[i] = densities[i] + math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
			densities[j] = densities[j] + math.exp(-(distances[i][j]/dc)*(distances[i][j]/dc))
		
	print 'Max distances  (1.232) ',np.amax(distances)
	
	print 'Max densities (118.6576) ',np.amax(densities)
	
	deltas = np.zeros((length))
	clustersCenters = []
	maxDistance = np.amax(distances)
	for i in range(length):
		deltas[i] = maxDistance
		for j in range(length):
			if densities[j] > densities[i]:
				if distances[i][j] < deltas[i]:
					deltas[i] = distances[i][j]

	# Al punto de mayor densidad le asigno la mayor distancia calculada para un punto
	deltas[np.where(deltas==np.sort(deltas)[-1])[0]]=np.sort(deltas)[-2]

	print 'Max deltas (0.2970) ',np.amax(deltas)

	
	ordDeltas = sorted(deltas, reverse=True)
	varDeltas = np.var(deltas)
	varDeltas = 0.1
	
	for i in range(length-1):
		if (ordDeltas[i]-ordDeltas[i+1]) > varDeltas:
			cut = i
	
	for i in range(cut+1):
		for center in np.where(deltas==ordDeltas[i]):
			for j in range(len(center)):
				clustersCenters.append(center[j])
	
	clustersCenters = np.unique(clustersCenters)
	
	labels = np.zeros((length))
	for i in range(length):
		currentDistance = maxDistance
		for j in clustersCenters:
			if distances[i][j] < currentDistance:
				currentDistance = distances[i][j]
				labels[i] = np.where(clustersCenters==j)[0]
	
	import matplotlib.pyplot as plt
	from operator import itemgetter
	plt.plot(densities,deltas,'ro')
	plt.savefig('/tmp/densitiesvsdeltas.png', bbox_inches='tight')
	plt.close()

	return (len(clustersCenters), labels)
	
def main():
	parser = argparse.ArgumentParser(prog='clustering.py',
	 description='Performs clustering for a given distance matrix',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFile',
	 help='Source file',
	 type=str, required=True)
	parser.add_argument('--dc',
	 help='distance',
	 type=float, required=True)
	 
	args = parser.parse_args()
	
	clusters, labels = predict(args.sourceFile, args.dc)

	print clusters
	print labels
	
	return 0

if __name__ == '__main__':
	main()

