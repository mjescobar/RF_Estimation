#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  recuperaSNR.py
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

import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)
import os     # operative system lib

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
		
def loadSNRMatrix(sourceFolder):
	SNRFile = scipy.io.loadmat(sourceFolder+'/snr_inspector.mat')
	SNRResult = SNRFile['snr_inspector']
	
	return SNRResult
	
def loadUnitsMatrix(sourceFolder):
	unitsFile = scipy.io.loadmat(sourceFolder+'/unit_name_inspector.mat')
	unitsResult = unitsFile['unit_name_inspector']
	
	return unitsResult
def main():

	file = open(outputFolder+'snr.csv', "w")
	header = 'Unidad\t'+'SNR'+'\n'
	snr = loadSNRMatrix(sourceFolder)
	units = loadUnitsMatrix(sourceFolder)
	for unit in range(len(snr)):
		linea = '"'+units[unit][0][0]+'"\t"'+str(snr[unit][0])+'"\n'
		file.write(linea)
	file.close
	return 0

if __name__ == '__main__':
	main()

