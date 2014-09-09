#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  readWriteTimestamps.py
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
#  


import sys, argparse, csv, os
	
def main():

	# command arguments
	parser = argparse.ArgumentParser(prog='readWriteTimestamps.py',
	 description='Splits the units file generated on NeuroExplorer',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFile',
	 help='File containing the time stamps',
	 type=str, default='datos0001_timestamps2_02_03.txt', required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, default='.', required=False)
	args = parser.parse_args()
	csv_file = args.sourceFile

	outputFolder = args.outputFolder
	# Check for trailing / on the folder
	if outputFolder[-1] != '/':
		outputFolder+='/'
	
	try:
		os.mkdir( outputFolder ) # if folder "STA" don't exist, create the folder
	except OSError:
		pass
		
	# open csv file
	with open(csv_file, 'rb') as csvfile:
		primeraFila = csvfile.readline().strip().split('\t')
		largoPrimeraFila = len(primeraFila)
		ultimoString = primeraFila[largoPrimeraFila-1]
		largoUltimoString = len(ultimoString)
		units = {'a','b','c','d'}
		if (largoUltimoString == 3 or largoUltimoString == 4) and ultimoString[-1] in units:
			num_columns = largoPrimeraFila - 1
		else:
			num_columns = largoPrimeraFila - 2
		
		csvfile.seek(0)
		
		reader = csv.reader(csvfile, delimiter='\t')
		
		print 'Numero Unidades =',num_columns
		num_lineas = sum(1 for line in csvfile)
		
		datos = [[[] for i in range(num_columns)] for i in range(num_lineas)]
		
		rowId = 0
		csvfile.seek(0)
		
		for row in reader:
			for column in range(num_columns):
				datos[rowId][column] = row[column]		      
			rowId += 1
		
		for i in range(num_columns):
			fileOutName = outputFolder+datos[0][i]+'.txt'
			f2 = open(fileOutName,'w')
			for j in range(num_lineas-1):
				if datos[j+1][i]:
					f2.writelines(datos[j+1][i]+'\n')
			f2.close()
		
	return 0

if __name__ == '__main__':
	main()

