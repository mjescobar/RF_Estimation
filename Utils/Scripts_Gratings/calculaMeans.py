#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  calculaMeans.py
#  
#  Copyright 2015 M
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

from numpy import shape
import argparse 							#argument parsing
from platform import system				# Windows or Linux?
import sys, os 

def returnPathCharacter():
	pathCharacter = '/'
	if system() == 'Windows':
		pathCharacter = '\\'
	
	return pathCharacter

def fixPath(folderName):
	pathCharacter = returnPathCharacter()
	# Check for trailing / on the folder
	if folderName[-1] != pathCharacter:
		folderName+=pathCharacter
	
	return folderName
from numpy import loadtxt,mean
    
def main():
	parser = argparse.ArgumentParser(prog='calculaMeans.py',
	 description='Calcula firing rate de las units procesadas con el neuroexplorer',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='Source folder',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	 
	args = parser.parse_args()
	
	sourceFolder = fixPath(args.sourceFolder)
	if not os.path.exists(sourceFolder):
		print ''
		print 'Source folder does not exists ' + sourceFolder
		print ''
		sys.exit()

	outputFolder = fixPath(args.outputFolder)
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except:
			print ''
			print 'Unable to create folder ' + outputFolder
			print ''
			sys.exit()
	factor=1000
	output=open(outputFolder+'output.csv','w')
	Deg0 = loadtxt(sourceFolder+'0.csv', delimiter=',',skiprows=1)
	Deg45 = loadtxt(sourceFolder+'45.csv', delimiter=',',skiprows=1)
	Deg90 = loadtxt(sourceFolder+'90.csv', delimiter=',',skiprows=1)
	Deg135 = loadtxt(sourceFolder+'135.csv', delimiter=',',skiprows=1)
	Deg180 = loadtxt(sourceFolder+'180.csv', delimiter=',',skiprows=1)
	Deg225 = loadtxt(sourceFolder+'225.csv', delimiter=',',skiprows=1)
	Deg270 = loadtxt(sourceFolder+'270.csv', delimiter=',',skiprows=1)
	Deg315 = loadtxt(sourceFolder+'315.csv', delimiter=',',skiprows=1)
	
	f = open(sourceFolder+'0.csv', 'r')
	unitsStr=f.readline()
	units=unitsStr[0:len(unitsStr)-1].split(",")
	f.close()
	
	fileHeader='\"Unit Name\"'+','\
	+'\"0 Degrees\"'+','\
	+'\"45 Degrees\"'+','\
	+'\"90 Degrees\"'+','\
	+'\"135 Degrees\"'+','\
	+'\"180 Degrees\"'+','\
	+'\"225 Degrees\"'+','\
	+'\"270 Degrees\"'+','\
	+'\"315 Degrees\"'+','\
	+'\"0 Degrees\"'+'\n'
	output.write(fileHeader)
	
	for unit in range(len(units)):
		unitMeans=units[unit]+','\
		+str(factor*mean(Deg0[:,unit]))+','\
		+str(factor*mean(Deg45[:,unit]))+','\
		+str(factor*mean(Deg90[:,unit]))+','\
		+str(factor*mean(Deg135[:,unit]))+','\
		+str(factor*mean(Deg180[:,unit]))+','\
		+str(factor*mean(Deg225[:,unit]))+','\
		+str(factor*mean(Deg270[:,unit]))+','\
		+str(factor*mean(Deg315[:,unit]))+','\
		+str(factor*mean(Deg0[:,unit]))+'\n'
		output.write(unitMeans)
	
	output.close()

	return 0

if __name__ == '__main__':
	main()

