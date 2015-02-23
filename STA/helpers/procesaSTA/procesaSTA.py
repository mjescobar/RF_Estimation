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

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe
import argparse #argument parsing

parser = argparse.ArgumentParser(prog='procesaSTA.py',
 description='Recovers the results from GaussFit',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
 help='Source folder',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output folder',
 type=str, required=True)
parser.add_argument('--blockSize',
 help='Size of each block in micrometres',
 type=int, default='50', required=False)
args = parser.parse_args()

def main():
	
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
	
	#Size of each block in micrometres
	blockSize = args.blockSize
			
	file = open(outputFolder+'data_rf.csv', "w")
	header = 'Unidad\tRadio A\tRadio B\tArea\tAngulo\tX\tY\n'
	file.write(header)
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			fitResult = rfe.loadFitMatrix(sourceFolder,unitFile)
			salidaValor='"'+unitFile.rsplit('_', 1)[0]+'"\t"' \
			+str(blockSize*fitResult[0][2])+'"\t"' \
			+str(blockSize*fitResult[0][3])+'"\t"' \
			+str(3.14*blockSize*fitResult[0][2]*blockSize*fitResult[0][3])+'"\t"' \
			+str(fitResult[0][1])+'"\t"' \
			+str(fitResult[0][4])+'"\t"' \
			+str(fitResult[0][5])+'"\n'
			file.write(salidaValor)
	file.close
	return 0

if __name__ == '__main__':
	main()

