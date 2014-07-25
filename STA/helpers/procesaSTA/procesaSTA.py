#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  procesaSTA.py
#  
#  Copyright 2014 
#  Monica Otero <monicaot2001@gmail.com>
#  Carlos "casep" Sepulveda <casep@fedoraproject.org>
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

# Procesa resultado de Ajuste Gaussiano y genera salida resumen 

import sys    # system lib
import os     # operative system lib
import matplotlib.pyplot as plt
import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)
import numpy
import matplotlib.pyplot as plt 	  # plot lib (for figures)
import scipy.ndimage
from scipy.cluster.vq import kmeans,vq
from pylab import plot,show

parser = argparse.ArgumentParser(prog='pca.py',
 description='Performs PCA',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
 help='Source folder',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output folder',
 type=str, required=True)
args = parser.parse_args()

#Source folder of the files with the timestamps
sourceFolder = args.sourceFolder
# Check for trailing / on the folder
if sourceFolder[-1] != '/':
	sourceFolder+='/'

if not os.path.exists(sourceFolder):
	print ''
	print 'Source folder does not exists ' + sourceFolder
	sys.exit()

#Source folder of the files with the timestamps
outputFolder = args.outputFolder
# Check for trailing / on the folder
if outputFolder[-1] != '/':
	outputFolder+='/'
	
if not os.path.exists(outputFolder):
	try:
		os.makedirs(outputFolder)
	except:
		print ''
		print 'Unable to create folder ' + outputFolder
		sys.exit()

def loadFitMatrix(sourceFolder,unitFile):
	# The STA matrix is named as M8a_lineal/sta_array_M8a.mat
	firResultFile = scipy.io.loadmat(sourceFolder+unitFile+'/fit_var.mat')
	firResult = firResultFile['fitresult']
	
	return firResult

def main():
	
	file = open(outputFolder+'myfile.csv', "w")
	header = "Unidad,"+"Radio A,"+"Radio B,"+"Area,"+"Angulo,"+"X,"+"Y"+'\n'
	file.write(header)
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			fitResult = loadFitMatrix(sourceFolder,unitFile)
			salidaValor=unitFile.rsplit('_', 1)[0]+","+str(fitResult[0][2])+","+str(fitResult[0][3])+","+str(3.14*fitResult[0][2]*fitResult[0][3])+","+str(fitResult[0][1])+","+str(fitResult[0][4])+","+str(fitResult[0][5])+'\n'
			file.write(salidaValor)
	file.close
	return 0

if __name__ == '__main__':
	main()

