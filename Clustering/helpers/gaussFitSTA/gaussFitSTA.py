#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gaussFitSTA.py
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

import argparse 			# argument parsing
import gaussFit				# our Gaussian Fit library
import os					# os manipulation 
import sys					# system lib
import scipy				# numerical methods lib (like Matlab functions)
import scipy.io				# input output lib (for save matlab matrix)

def loadSTAVisual(sourceFolder,unit):
	staVisualFileName = sourceFolder+unit+'_lineal/stavisual_lin_array_'+unit+'.mat'
	staVisualFile = scipy.io.loadmat(staVisualFileName)
	staVisual = staVisualFile['STAarray_lin']
	
	return staVisual


def main():	
	parser = argparse.ArgumentParser(prog='gaussFitSTA.py',
	 description='2D Gaussian fit to estimated receptive fields STA',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder', default=".",
	 help='Folder containing the STA',
	 type=str, required=True)
	parser.add_argument('--unit',
	 help='Unit to be processed',
	 type=str, required=True)
	 
	args = parser.parse_args()

	#Source folder of the files with the timestamps
	sourceFolder = args.sourceFolder
	# Check for trailing / on the folder
	if sourceFolder[-1] != '/':
		sourceFolder+='/'
	
	if not os.path.exists(sourceFolder):
		print ''
		print 'Source folder does not exists ' + sourceFolder
		sys.exit()
	
	unit = args.unit
	
	staVisual = loadSTAVisual(sourceFolder,unit)
	Xpixels, Ypixels, valores, Xpixel2D, Ypixel2D = gaussFit.prepareSurfaceData(staVisual[:,:,14])
	print valores
	
	return 0

if __name__ == '__main__':
	main()

