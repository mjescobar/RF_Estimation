#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  drawDSIvsArea.py
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

#  Code use to draw ellipses

import sys
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '../..','LIB'))
import argparse
import numpy as np
import scipy.ndimage
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
import math
from matplotlib.patches import Ellipse
from pylab import figure, show, savefig

parser = argparse.ArgumentParser(prog='drawDSIvsArea.py',
 description='Draw DSI vs Area for all the units',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--DSI',
 help='Source File',
 type=str, required=True)
parser.add_argument('--Area',
 help='Source File',
 type=str, required=True)
parser.add_argument('--DSI_otro',
 help='Source File',
 type=str, required=True)
parser.add_argument('--Area_otra',
 help='Source File',
 type=str, required=True)
parser.add_argument('--outputFolder',
 help='Output File',
 type=str, required=True)

args = parser.parse_args()

#Source file of the clusters and all the information
DSI = args.DSI
DSI_otro=args.DSI_otro
#Output file where the graphics are going to be placed
outputFolder = args.outputFolder
Area = args.Area
Area_otra=args.Area_otra

## Loading and reading data

DSI_data = np.loadtxt(DSI)
Area_data= np.loadtxt(Area)
DSI_data_otro=np.loadtxt(DSI_otro)
Area_data_otra=np.loadtxt(Area_otra)
plt.figure()
plt.scatter(DSI_data_otro,Area_data_otra/1000,color='blue',s=100,alpha=0.5)
plt.scatter(DSI_data,Area_data/1000,color='red',s=100,alpha=0.5)
plt.xlabel('DSI')
plt.ylabel('Area')
plt.ylim((-5,180))
plt.xlim((0,1.05))
plt.savefig(outputFolder+'dsi_VS_area.pdf', format='pdf', bbox_inches='tight')
plt.show()


