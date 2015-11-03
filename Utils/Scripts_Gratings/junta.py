#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  junta.py
#  
#  Copyright 2015 Carlos "casep" Sepulveda <carlos.sepulveda@gmail.com>
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


def main():

	parser = argparse.ArgumentParser(prog='junta.py',
	 description='Genera agrupacion de archivos desde archivos PostionsPerCategoryPositionsPerCategoryXXXX.csv',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder',
	 help='Source folder',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	parser.add_argument('--files_number',
	 help='Number of files',
	 type=int, required=True)
	
	
	args = parser.parse_args()
	files_number = args.files_number 
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

	archivoSalida='0001.csv'
	salida=1
	categoria=1
	output=open(outputFolder+archivoSalida,'w')
	for i in range(1,files_number):
		if salida==31:
			categoria+=1
			output.close()
			archivoSalida=str(categoria).zfill(4)+'.csv'
			output=open(outputFolder+archivoSalida,'w')
			salida=1
				
		f = open(sourceFolder+'PostionsPerCategoryPositionsPerCategory'+str(i).zfill(4)+'.csv', 'r')
		f.readline()
		contenido=f.readline()
		linea=''
		if len(contenido)>0:
			
			linea=contenido.split(' ', 1 )[0]+','+contenido.split(' ', 1 )[1].translate(None, '\r\n')+','+str(float(contenido.split(' ', 1 )[0])/20000)+'\r\n'
		output.write(linea)
		f.close()
		salida+=1
	return 0

if __name__ == '__main__':
	main()

