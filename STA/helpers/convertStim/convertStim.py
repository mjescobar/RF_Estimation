#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  convertStim.py
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

# Convert and save the stimuli matriz from Matlab v7.3 format to 
# ndarray in the Matlab v7 geometry. The stimuli is saved on grayscale

import h5py         # Matlab v7.3 handling
import argparse     # argument parsing
import os           # operating system lib
import numpy as np 	# numerical methods lib

parser = argparse.ArgumentParser(prog='converStim.py',
 description='Transforms stim_min v7.3 to gray ndarray',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--stimMini',
 help='Stimuli matrix',
 type=str, default='stim_mini.mat', required=True)
parser.add_argument('--outputFile',
 help='Output file',
 type=str, default='ndaarray.out', required=False)
args = parser.parse_args()

# load image mat file stimMini
stimMini = args.stimMini
if not os.path.isfile(stimMini):
	print 'File [' + stimMini + '] not found'
	sys.exit()

h5pyFile = h5py.File(stimMini,'r')
stimuli = h5pyFile['stim']

# Shape is in the was <LEN, 3, 31, 31>
lenStimuli = stimuli.shape[0]
rgbLen=stimuli.shape[1]
xLen=stimuli.shape[2]
yLen=stimuli.shape[3]

grayStimuli = np.zeros(( xLen , yLen , lenStimuli ))

# transform each image from rgb to grayscale
for kIter in range(lenStimuli):
	rgb = stimuli[kIter,:,:,:]
	myArray=[]
	myOtherArray=[]
	myYetAnotherArray=[]
	for rIter in range(xLen):
		myOtherArray=[]
		for gIter in range(yLen):
			myArray=[]
			for bIter in range(rgbLen):
				myArray.append(rgb[bIter,gIter,rIter])
			myOtherArray.append(myArray)
		myYetAnotherArray.append(myOtherArray)
	grayStimuli[:,:,kIter]=np.dot(myYetAnotherArray, [0.299, 0.587, 0.144])

np.save(args.outputFile, grayStimuli)
