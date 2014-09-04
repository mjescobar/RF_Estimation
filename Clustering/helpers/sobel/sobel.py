#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sobel.py
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

from scipy import ndimage
import sys    # system lib
import os     # operative system lib
import matplotlib.pyplot as plt
import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)
import numpy
import matplotlib.cm as cm      	  # plot lib


parser = argparse.ArgumentParser(prog='pca.py',
 description='Performs PCA',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
 help='Source folder',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output folder',
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

#Source folder of the files with the timestamps
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

def main():
	for unitFile in os.listdir(sourceFolder):
		if os.path.isdir(sourceFolder+unitFile):			
			unitName = unitFile.rsplit('_', 1)[0]
			print unitName
			staMatrixFile = scipy.io.loadmat(sourceFolder+unitFile+'/stavisual_lin_array_'+unitName+'.mat')
			staMatrix = staMatrixFile['STAarray_lin']
			xLength = staMatrix.shape[0]
			yLength = staMatrix.shape[1]
			zLength = staMatrix.shape[2]
			for zAxis in range(zLength):
				print 'desde disco'
				
				fig = plt.figure()
				fig.set_size_inches(1, 1)
				data = staMatrix[:,:,zAxis]
				#plt.pcolormesh( staMatrix[:,:,zAxis],vmin = 0,vmax = 255, cmap=cm.jet )
				ax = plt.Axes(fig, [0., 0., 1., 1.])
				ax.set_axis_off()
				fig.add_axes(ax)
				plt.set_cmap(cm.jet)
				ax.imshow(data, aspect = 'auto')
				plt.savefig(outputFolder+unitName+str(zAxis)+".png",format='png',dpi=31)
				plt.close()
			
	return 0

if __name__ == '__main__':
	main()

