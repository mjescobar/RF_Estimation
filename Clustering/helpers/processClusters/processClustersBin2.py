#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  processClustersBin2.py
#  
#  Copyright 2015 Monica Otero <monicaot2011@gmail.com>
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

import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe				#Some custom functions
import argparse 							#argument parsing
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from numpy import loadtxt
from numpy import shape
from numpy import histogram
from numpy import amax
from numpy import amin
from numpy import append
from numpy import zeros
from numpy import empty
from numpy import arange

#Input file format

# 0-19 Timestamps
# aRadius
# bRadius
# angle
# xCoordinate
# yCoordinate
# area
# clusterId
# peakTime
# On/Off 

clustersColours = ['green', 'red', 'blue', 'yellow', 'black','indigo', \
'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
'#5b6756','#0c8248','k','#820cff','#932c11', \
'#002c11','#829ca7']
				
def loadClusterFile(sourceFile):
	data = loadtxt(sourceFile, delimiter=',')
	
	return data

def graficaHistograma(areaTotal,areaInteres,outputFolder,titulo,clusterId,binsCalculados):
	plt.hist(areaTotal, bins=binsCalculados,\
	 histtype='stepfilled', normed=0, color='grey', alpha=0.2, label='Total')
	plt.hist(areaInteres, bins=binsCalculados,\
	 histtype='stepfilled', normed=0, color=clustersColours[clusterId], alpha=0.4, label=titulo)
	plt.title('Total/'+titulo)
	plt.xlabel('Area')
	plt.ylabel('Units')
	plt.legend()
	plt.savefig(outputFolder+titulo+'_cluster_'+str(clusterId)+'.png', bbox_inches='tight')
	plt.close()
	
	return 0
	
def main():
	
	parser = argparse.ArgumentParser(prog='processClustersBin2.py',
	 description='Plot units from clustering',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFile',
	 help='Source file containing the units and its data',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	 
	args = parser.parse_args()

	#Source file of the units
	sourceFile = args.sourceFile
	if not os.path.exists(sourceFile):
		print ''
		print 'Source file does not exists ' + sourceFile
		print ''
		sys.exit()

	#Output folder for the graphics
	outputFolder = rfe.fixPath(args.outputFolder)
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except:
			print ''
			print 'Unable to create folder ' + outputFolder
			print ''
			sys.exit()
	
	Units = loadClusterFile(sourceFile)
	# Slow, Fast ?
	# Separación en base a 2 bins segun peak time
	peaks = Units[:,27]
	hist,edges = histogram(peaks,bins=2)
	slowMaximum = edges[1]
	fastMaximum = edges[2]
	
	#print 'slowMaximum',slowMaximum
	#print 'fastMaximum',fastMaximum
		
	# Por cada cluster recorro las units
	numClusters = int(max(Units[:,26]))
	for clusterId in range(numClusters + 1):
		slowUnits = empty([1, 29])
		fastUnits = empty([1, 29])
		# Por cada unit las separo en lentas y rapidas dependiendo del Hist anerior
		for unitId in range(len(Units)):
			if Units[unitId,26] == clusterId:
				#print 'clusterId',clusterId
				#print 'peak',Units[unitId,27]
				if Units[unitId,27] <= slowMaximum:
					slowUnits = append(slowUnits,Units[unitId].reshape(1, 29), axis=0)
				else:
					fastUnits = append(fastUnits,Units[unitId].reshape(1, 29), axis=0)
	
		# Elimino la primera fila
		slowUnits = slowUnits[1:,:]	
		fastUnits = fastUnits[1:,:]	
		
		areaTotal = Units[:,25]
		
		binwidth = 30
		binsCalculados = arange(min(areaTotal), max(areaTotal) + binwidth, binwidth)
		# Podria quedar un bin vacio (creo)?
		if shape(slowUnits)[0] > 0 :
			# Extraigo caracteristica de interes
			areaSlows = slowUnits[:,25]
			# Graficas
			graficaHistograma(areaTotal,areaSlows,outputFolder,'Slows',clusterId,binsCalculados)

		# Podria quedar un bin vacio (creo)?
		if shape(fastUnits)[0] > 0 :
			# Extraigo caracteristica de interes
			areaFasts = fastUnits[:,25]
			# Graficas
			graficaHistograma(areaTotal,areaFasts,outputFolder,'Fasts',clusterId,binsCalculados)
			
	return 0

if __name__ == '__main__':
	main()

