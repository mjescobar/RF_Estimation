#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pca.py
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

import sys    # system lib
import os     # operative system lib
import matplotlib.pyplot as plt
import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)

parser = argparse.ArgumentParser(prog='pca.py',
 description='Performs PCA',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
 help='Source folder',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output folder',
 type=str, required=False)
args = parser.parse_args()

#Source folder of the files with the timestamps
sourceFolder = args.sourceFolder
# Check for trailing / on the folder
if sourceFolder[-1] != '/':
	sourceFolder+='/'

#Source folder of the files with the timestamps
outputFolder = args.outputFolder
# Check for trailing / on the folder
if sourceFolder[-1] != '/':
	sourceFolder+='/'
	
def loadMatrix(sourceFolder,unitFile):
	unit=unitFile.rsplit('_', 1)[0]
	print sourceFolder+unitFile+'/sta_array_'+unit+'.mat'
	staMatrixFile = scipy.io.loadmat(sourceFolder+unitFile+'/sta_array_'+unit+'.mat')
	staMatrix = staMatrixFile['STA_array']
	
	print staMatrix.shape
	
	
for unitFile in os.listdir(sourceFolder):
	if os.path.isdir(sourceFolder+unitFile):
		loadMatrix(sourceFolder,unitFile)
