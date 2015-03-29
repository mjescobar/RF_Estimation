#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  processClusters.py
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
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
from numpy import loadtxt
from numpy import shape
from numpy import histogram
from numpy import amax
from numpy import amin
from numpy import append
from numpy import zeros
from numpy import empty


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

def loadClusterFile(sourceFile):
	data = loadtxt(sourceFile, delimiter=',')
	
	return data

def main():
	
	parser = argparse.ArgumentParser(prog='processClusters.py',
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
	#Slow, Medium, Fast ?
	peaks = Units[:,27]
	hist,edges = histogram(peaks,bins=3)
	print 'hist',hist
	print 'edges',edges
	slowMinimum = edges[0]
	slowMaximum = edges[1]
	mediumMinimum = edges[1]
	mediumMaximum = edges[2]
	fastMinimum = edges[2]
	fastMaximum = edges[3]

	slowUnits = empty([1, 28])
	mediumUnits = empty([1, 28])
	fastUnits = empty([1, 28])
	
	for unitId in range(len(Units)):
		if Units[unitId,27] < slowMaximum:
			slowUnits = append(slowUnits,Units[unitId].reshape(1, 28), axis=0)
		elif Units[unitId,27] < mediumMaximum:
			mediumUnits = append(mediumUnits,Units[unitId].reshape(1, 28), axis=0)
		else:
			fastUnits = append(fastUnits,Units[unitId].reshape(1, 28), axis=0)
	
	slowUnits = slowUnits[1:,:]	
	mediumUnits = mediumUnits[1:,:]	
	fastUnits = fastUnits[1:,:]	
	
	print 'slows',shape(slowUnits)
	print 'mediums',shape(mediumUnits)
	print 'fasts',shape(fastUnits)
	print 'Units',shape(Units)
	
	areaTotal = Units[:,25]
	areaSlows = slowUnits[:,25]
	areaMediums = mediumUnits[:,25]
	areaFasts = fastUnits[:,25]

	plt.hist(areaTotal, bins=2, histtype='stepfilled', normed=True, color='b', alpha=0.2, label='Total')
	plt.hist(areaSlows, bins=2, histtype='stepfilled', normed=True, color='r', alpha=0.4, label='Slows')
	plt.title("Total/Slows")
	plt.xlabel("Area")
	plt.ylabel("Y Value")
	plt.legend()
	plt.savefig(outputFolder+'slows.png', bbox_inches='tight')
	plt.close()
	
	plt.hist(areaTotal, bins=2, histtype='stepfilled', normed=True, color='b', alpha=0.2, label='Total')
	plt.hist(areaMediums, bins=2, histtype='stepfilled', normed=True, color='r', alpha=0.4, label='Mediums')
	plt.title("Total/Medium")
	plt.xlabel("Area")
	plt.ylabel("Y Value")
	plt.legend()
	plt.savefig(outputFolder+'mediums.png', bbox_inches='tight')
	plt.close()
	
	plt.hist(areaTotal, bins=2, histtype='stepfilled', normed=True, color='b', alpha=0.2, label='Total')
	plt.hist(areaFasts, bins=2, histtype='stepfilled', normed=True, color='r', alpha=0.4, label='Fasts')
	plt.title("Total/Fast")
	plt.xlabel("Area")
	plt.ylabel("Y Value")
	plt.legend()
	plt.savefig(outputFolder+'fasts.png', bbox_inches='tight')
	plt.close()
	
	
	
	
	return 0

if __name__ == '__main__':
	main()

