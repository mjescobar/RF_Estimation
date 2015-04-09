#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  procesaGratings.py
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
#  Procesa gratings obtenidas secuencialmente

import sys    # system lib
import os     # operative system lib
import argparse #argument parsing
import numpy
	  

parser = argparse.ArgumentParser(prog='procesaGratings.py',
 description='Process the inicio_fin Frames taken from Gratings',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFile',
 help='Source File',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output File',
 type=str, required=True)
#parser.add_argument('--expOrder',
 #help='Experiment Order',
 #type=str, required=True)
args = parser.parse_args()

#Source file of the files with the inicio_fin Frames de las gratings
sourceFile = args.sourceFile

#Output file where the positions associated to the categories of the experiments are associated
outputFolder = args.outputFolder

#Categories file
#expOrder = args.expOrder

def main():
	
	f= open (sourceFile,'r')
	results=[]
	differences=[]
	firstTime=0;
	repetitions=0;
	for line in f:
		linea = line.split ()
		ini=linea[0]
		fin=linea[1]
		resta=float(fin)-float(ini)
		if (resta < 333):
			if firstTime ==0:
				firstTime+=1
		elif (resta > 336):
			results.append(ini)
			differences.append(resta)
			firstTime=0
			repetitions+=1
			file = open(outputFolder+'PositionsPerCategory'+str(repetitions)+'.csv', "w")
			header = '\"Punto\"\t\"Categoria\"\n'
			file.write(header)
			for i in xrange(len(results)):
				cadena= str(results[i])+ ' ' +str(differences[i]) + '\n' 		 
				file.write (cadena )
			file.close
			results=[]
			differences=[]
			
		else :
			if firstTime:
				results.append(ini)
				differences.append(resta)	
				firstTime=0
	repetitions+=1
	file = open(outputFolder+'PositionsPerCategory'+str(repetitions)+'.csv', "w")
	header = '\"Punto\"\t\"Categoria\"\n'
	file.write(header)
	for i in xrange(len(results)):
		cadena= str(results[i])+ ' ' +str(differences[i]) + '\n' 		 
		file.write (cadena )
	file.close
	return 0

if __name__ == '__main__':
	main()


	

