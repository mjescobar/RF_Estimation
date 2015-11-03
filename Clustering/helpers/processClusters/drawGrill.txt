#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  drawClustersGrill.py
#  Mónica Otero
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

#  Code use to draw all ellipses from different clusters

import sys
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../..','LIB'))
import argparse
import numpy as np
import scipy.ndimage
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn import preprocessing
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
import math
from matplotlib.patches import Ellipse
from pylab import figure, show, savefig

parser = argparse.ArgumentParser(prog='drawClustersGrill.py',
 description='Draw the ellipses for all the clusters',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFile',
 help='Source File',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output File',
 type=str, required=True)
parser.add_argument('--xPixels',
 help='Number of xblocks',
 type=int, default=31, required=False)
parser.add_argument('--yPixels',
 help='Number of yblocks',
 type=int, default=31, required=False)
parser.add_argument('--blockSize',
 help='Block Size',
 type=int, default=50, required=False)



args = parser.parse_args()

#Source file of the clusters and all the information
sourceFile = args.sourceFile
#Output file where the graphics are going to be placed
outputFolder = args.outputFolder

xPixels = args.xPixels
yPixels = args.yPixels
blockSize= args.blockSize

clustersColours = ['green', 'red', 'blue', 'orange','yellow','indigo',\
'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
'#5b6756','#0c8248','k','#820cff','#932c11', \
'#002c11','#829ca7']


## Loading and reading data

indata = np.loadtxt(sourceFile, delimiter=',', usecols=[20,21,22,23,24,25,27,28,29])
#indataLabels = np.loadtxt(sourceFile,usecols=[12],dtype=str)

print "> Reading input data: ", np.shape(indata)

#  Random_Spikes_Selection.py
	#0-19 Timestamps
	#  20 aRadius
	#  21 bRadius
	#  22 angle
	#  23 xCoordinate
	#  24 yCoordinate
	#  25 area
	#  26 clusterId
	#  27 peakTime
	#  28 ON_OFF

spk_OFF = []
spk_ON = []

for i in range(len(indata[:,0])):
	if( int(indata[i,8]) == 1):
		spk_OFF.append(indata[i,:])
	if( int(indata[i,8]) == 0):
		spk_ON.append(indata[i,:])

spk_OFF = np.array(spk_OFF)
spk_ON = np.array(spk_ON)
 
nOFF = np.size(spk_OFF[:,1])
nON = np.size(spk_ON[:,1])
print "> Number of ON cells: ", nON, "(", 1.0*nON/(nON+nOFF), "%)" 
print "> Number of OFF cells: ", nOFF, "(", 1.0*nOFF/(nON+nOFF), "%)" 

# Separating data by grouped clusters
nclusters = np.max(indata[:,6])
print "> Number of clusters: ", nclusters + 1

resFig= figure()
bx = resFig.add_subplot(111, aspect='equal')

for cluster in range(int(nclusters)+1):
	print cluster
	fig = figure()
	ax = fig.add_subplot(111, aspect='equal')
	for unit in range(nOFF):
		eWidth = float(spk_OFF[unit,0])
		eHeight = float(spk_OFF[unit,1])
		eAngle = float(spk_OFF[unit,2])
		eXY = [float(spk_OFF[unit,3]),  float(spk_OFF[unit,4])]
		resE = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle)
		bx.add_artist(resE)
		resE.set_alpha(0.2)
		resE.set_facecolor(clustersColours[int(spk_OFF[unit,6])])
		bx.set_xlabel('Retina piece Xsize ('+r'$\mu$'+'m)')
		bx.set_ylabel('Retina piece Ysize ('+r'$\mu$'+'m)')
		if(int(spk_OFF[unit,6])==cluster):
			e = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle, fill=False)
			ax.add_artist(e)
			e.set_alpha(0.6)
			e.set_edgecolor(clustersColours[int(spk_OFF[unit,6])])
			
		else:
			e = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle, fill=False)
			ax.add_artist(e)
			e.set_edgecolor('gray')
			e.set_alpha(0.2)
			
	'''Xaxis = ax.xaxis
	Yaxis = ax.yaxis
	lengthX=len(Xaxis.get_ticklocs())
	lengthY=len(Yaxis.get_ticklocs())
	coefX=Xaxis.get_ticklocs()
	coefY=Yaxis.get_ticklocs()
	xlabels=coefX
	ylabels=coefY
	for value in range(lengthX):
		xlabels[value]=int((xPixels/lengthX)*coefX[value]*(xPixels/lengthX)*blockSize)	
	for value in range(lengthY):
		ylabels[value]=int((yPixels/lengthY)*coefY[value]*(yPixels/lengthY)*blockSize)'''		
	ax.set_xlim(0, xPixels)
	ax.set_ylim(0, yPixels)
	xlabels= ['0','250', '500', '750', '1000','1250', '1500']
	ylabels= ['0','250', '500', '750', '1000','1250', '1500']
	ax.set_xticklabels(xlabels)
	ax.set_yticklabels(ylabels)
	ax.set_xlabel('Retina piece Xsize ('+r'$\mu$'+'m)')
	ax.set_ylabel('Retina piece Ysize ('+r'$\mu$'+'m)')
	fig.savefig(outputFolder + '/OFF_Grill_' + str(cluster)+ '.pdf', dpi=None, bbox_inches='tight', format='pdf')
xlabels= ['0','250', '500', '750', '1000','1250', '1500']
ylabels= ['0','250', '500', '750', '1000','1250', '1500']
bx.set_xlim(0, xPixels)
bx.set_ylim(0, yPixels)
bx.set_xticklabels(xlabels)
bx.set_yticklabels(ylabels)
bx.set_xlabel('Retina piece Xsize ('+r'$\mu$'+'m)')
bx.set_ylabel('Retina piece Ysize ('+r'$\mu$'+'m)')
resFig.savefig(outputFolder + '/GeneralGrill_OFF.pdf', dpi=None, bbox_inches='tight',format='pdf')
plt.close(resFig)
plt.close(fig)
resFig= figure()
bx = resFig.add_subplot(111, aspect='equal')


for cluster in range(int(nclusters)+1):
	print cluster
	fig = figure()
	ax = fig.add_subplot(111, aspect='equal')
	for unit in range(nON):
		eWidth = float(spk_ON[unit,0])
		eHeight = float(spk_ON[unit,1])
		eAngle = float(spk_ON[unit,2])
		eXY = [float(spk_ON[unit,3]),  float(spk_ON[unit,4])]
		resE = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle)
		bx.add_artist(resE)
		resE.set_alpha(0.2)
		resE.set_facecolor(clustersColours[int(spk_ON[unit,6])])
		if(spk_ON[unit,6]==cluster):
			e = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle, fill=False)
			ax.add_artist(e)
			e.set_edgecolor(clustersColours[int(spk_ON[unit,6])])
			e.set_alpha(0.6)
		else:
			e = Ellipse(xy=eXY, width=eWidth, height=eHeight, angle=eAngle, fill=False)
			ax.add_artist(e)
			e.set_edgecolor('gray')
			e.set_alpha(0.2)
	'''Xaxis = ax.xaxis
	Yaxis = ax.yaxis
	lengthX=len(Xaxis.get_ticklocs())
	print lengthX
	lengthY=len(Yaxis.get_ticklocs())
	coefX=Xaxis.get_ticklocs()
	coefY=Yaxis.get_ticklocs()
	for value in range(lengthX):
		xlabels[value]=int((xPixels/lengthX)*coefX[value]*(xPixels/lengthX)*blockSize)	
	for value in range(lengthY):
		ylabels[value]=int((yPixels/lengthY)*coefY[value]*(yPixels/lengthY)*blockSize)'''		
	ax.set_xlim(0, xPixels)
	ax.set_ylim(0, yPixels)
	xlabels= ['0','250', '500', '750', '1000','1250', '1500']
	ylabels= ['0','250', '500', '750', '1000','1250', '1500']
	ax.set_xticklabels(xlabels)
	ax.set_yticklabels(ylabels)
	ax.set_xlabel('Retina piece Xsize ('+r'$\mu$'+'m)')
	ax.set_ylabel('Retina piece Ysize ('+r'$\mu$'+'m)')
	fig.savefig(outputFolder + '/ON_Grill_' + str(cluster)+ '.pdf', dpi=None, bbox_inches='tight',format='pdf')
xlabels= ['0','250', '500', '750', '1000','1250', '1500']
ylabels= ['0','250', '500', '750', '1000','1250', '1500']
bx.set_xlim(0, xPixels)
bx.set_ylim(0, yPixels)
bx.set_xticklabels(xlabels)
bx.set_yticklabels(ylabels)
bx.set_xlabel('Retina piece Xsize ('+r'$\mu$'+'m)')
bx.set_ylabel('Retina piece Ysize ('+r'$\mu$'+'m)')
resFig.savefig(outputFolder + '/GeneralGrill_ON.pdf', dpi=None, bbox_inches='tight', format='pdf')
