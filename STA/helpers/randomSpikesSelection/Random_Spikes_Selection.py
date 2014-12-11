#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Random_Spikes_Selection.py
#  
#  Copyright 2014 Mónica <monicaot2001@gmail.com>
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
import random


def main():
	parser = argparse.ArgumentParser(prog='Random_Spikes_Selection.py',
	 description='Selecciona aleatoriamente un numero x de spikes dentro del fichero timestamps',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFile',
	 help='Source file',
	 type=str, required=True)
	parser.add_argument('--percentOfSpikes',
	 help='Number of spikes to be extracted',
	 type=int, default= '1000' , required=False)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	parser.add_argument('--repetitions', default=10,
	 help='Number of repetitions',
	 type=int, required=False)
	args = parser.parse_args()

	sourceFile = args.sourceFile
	percentOfSpikes = args.percentOfSpikes
	outputFolder= args.outputFolder
	repetitions=args.repetitions

	
	#Output folder of the files with the timestamps selected
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
	
	for i in range (repetitions):
		f= open (sourceFile,'r')
		listOfSpikes= f.readlines()
		numberOfSpikes=(percentOfSpikes*len(listOfSpikes))/100
		randomNumbers= random.sample (xrange (len(listOfSpikes)), numberOfSpikes)
		randomNumbers.sort()
		fileOutName = outputFolder+'/'+str(numberOfSpikes)+'/'+ 'resultFile'+str(i)+'.txt'
		file= open (fileOutName, 'w')
		for number in randomNumbers:
		 file.write(listOfSpikes[number])
	f.close()
	file.close()
		

if __name__ == '__main__':
	main()
