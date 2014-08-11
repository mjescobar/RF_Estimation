#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  creaInicioFin.py
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
#  Crea archivo de inicio fin 

import argparse #argument parsing
import os     # operative system lib

parser = argparse.ArgumentParser(prog='creaInicioFin.py',
 description='Crea archivo de inicio fin desde uno que solo tiene inicio',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFile',
 help='Source file',
 type=str, required=True)
parser.add_argument('--outputFile',
 help='Output file',
 type=str, required=True)
parser.add_argument('--adjustment',
 help='Adjustment',
 type=float, required=True)
args = parser.parse_args()

sourceFile = args.sourceFile
outputFile = args.outputFile
adjustment = args.adjustment

def main():

	fileI = open(sourceFile, 'r')
	fileO = open(outputFile, 'w')
	for line in fileI:
		fileO.write(str('%e' % float(line))+'\t'+str('%e' % (float(line)+adjustment))+'\n')
	fileI.close()
	fileO.close()
	return 0

if __name__ == '__main__':
	main()

