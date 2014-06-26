#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  readwrite_timestamps_txt.py
#  
#  Copyright 2014 Aland Astudillo
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

#============================================================
# READ WRITE TIME STAMPS OF SPIKES
# AASTUDILLO 2013
#============================================================

import numpy as np 	      # numerical methods lib
import sys    # system lib
import os     # operative system lib
import glob # package for get filenames from files in a folder
import argparse #argument parsing

# getimagenames = int(sys.argv[1]) #0
print '---------------------BEGIN---------------------------'

parser = argparse.ArgumentParser(prog='readwrite_timestamps_txt.py',
 description='Splits the units file generated on NeuroExplorer',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--filetimestamps',
 help='File containing the time stamps',
 type=str, default='datos0001_timestamps2_02_03.txt', required=True)
parser.add_argument('--outputFolder',
 help='Output folder',
 type=str, default='.', required=False)
args = parser.parse_args()

tsfolder = args.outputFolder

# Check for trailing / on the folder
if tsfolder[-1] != '/':
	tsfolder+='/'
	
try:
  os.mkdir( tsfolder ) # if folder "STA" don't exist, create the folder
except OSError:
  pass

filetimestamps = args.filetimestamps 

if not os.path.isfile(filetimestamps):
	print 'File [' + filetimestamps + '] not found'
	sys.exit()

f = open( filetimestamps ,'r')
per_row = []
for line in f:
    per_row.append(line.split('\t'))
per_column = zip(*per_row)
lenFile=len(per_row[0])
print 'len(per_row) ', len(per_row) ,'x', lenFile

for k in range(lenFile-1):
	columna1 = per_column[k]
	unit1 = columna1[0]
	if unit1 != 'AllFile':
		print unit1 ,' spikes ', len(columna1)-1
		p = 0
		for elemento in columna1:
			try:
				float(elemento)
				g= True
			except ValueError:
				g= False
			if g:
				p += 1
		print unit1 ,' spikes ', p
		col = columna1[1:p] #columna1[1:len(columna1)]
		fileoutname = tsfolder+''+unit1+'.txt'
		f2 = open( fileoutname ,'w')
		for linea in col:
			fila = linea + '\n'
			f2.writelines(fila)
		f2.close()
f.close()

print '-----------------------END---------------------------'
