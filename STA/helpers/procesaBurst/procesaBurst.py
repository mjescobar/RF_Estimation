#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  procesaBurst.py
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
import argparse
import matplotlib.pyplot as plt

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe

def main():
	# command arguments
	parser = argparse.ArgumentParser(prog='procesaBurst.py',
	 description='Genera histograma de los burst de spikes',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='File containing the time stamps',
	 type=str, default='.', required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, default='.', required=False)
	args = parser.parse_args()
	
	#Source folder of the files with the timestamps
	sourceFolder = rfe.fixPath(args.sourceFolder)
	
	#Output folder for the graphics
	outputFolder = rfe.fixPath(args.outputFolder)
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except:
			print ''
			print 'Unable to create folder ' + outputFolder
			sys.exit()
	
	for unitFile in os.listdir(sourceFolder):
		primerValor = 0
		segundoValor = 0	
		valores = []

		f = open(sourceFolder+unitFile, 'r')
		for line in f:
			if primerValor == 0:
				primerValor = float(line)
			if segundoValor == 0:
				segundoValor = float(line)
			segundoValor = float(line)
			if segundoValor > primerValor:
				valores.append(segundoValor - primerValor)
			primerValor = segundoValor
		f.close
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.hist(valores)
		fig.savefig(outputFolder+unitFile+'.png')
		plt.close()
		
	return 0

if __name__ == '__main__':
	main()

