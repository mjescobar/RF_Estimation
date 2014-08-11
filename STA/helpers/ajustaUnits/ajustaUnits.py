#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ajustaUnits.py
#  
#  Copyright 2014 Carlos "casep" Sepulveda <casep@alumnos.inf.utfsm.cl>
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
#  Ajusta tiempo en units para calzar con tiempos de experimento

import argparse #argument parsing
import os     # operative system lib

def main():
	parser = argparse.ArgumentParser(prog='ajustaUnits.py',
	 description='Ajusta los timestamps de los spikes',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='Source file',
	 type=str, required=True)
	parser.add_argument('--adjustment',
	 help='Adjustment',
	 type=float, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	args = parser.parse_args()

	sourceFolder = args.sourceFolder
	adjustment = args.adjustment

	#Source folder of the files with the timestamps
	sourceFolder = args.sourceFolder
	# Check for trailing / on the folder
	if sourceFolder[-1] != '/':
		sourceFolder+='/'
	
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

	# asume there are only unit (.txt) files generated on that folder
	for unitFile in os.listdir(sourceFolder):
		if os.path.isfile(sourceFolder+unitFile):
			fileI = open(sourceFolder+unitFile, 'r')
			fileO = open(outputFolder+unitFile, 'w')
			for line in fileI:
				fileO.write(str(float(line)+adjustment)+'\n')
			fileI.close()
			fileO.close()
	return 0

if __name__ == '__main__':
	main()

