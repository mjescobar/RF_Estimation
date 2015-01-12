#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  onOffClassification.py
#  
#  Copyright 2014 
#  Monica Otero <monicaot2001@gmail.com>
#  Carlos "casep" Sepulveda <casep@fedoraproject.org>
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

# Genera clasificacion unidades on-off u off-on dependiendo de ocurrencia
# minimo y maximo y además el frame dde se alcanzó este min/max

import sys    # system lib
import os     # operative system lib
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe
import gaussfitter as gf
import argparse #argument parsing
import scipy.io 	      # input output lib (for save matlab matrix)
import numpy
import matplotlib.pyplot as plt
  

parser = argparse.ArgumentParser(prog='onOffClassification.py',
 description='Classify On-Off or Off-On units',
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

def loadFitMatrix(sourceFolder,unitFile):
	firResultFile = scipy.io.loadmat(sourceFolder+unitFile+'/fit_var.mat')
	firResult = firResultFile['fitresult']
	
	return firResult

def main():
	
	file = open(outputFolder+'onOff.csv', "w")
	
	header = 'Unidad\t'+'OnOff\t'+'PeakFrame''\n'
	file.write(header)
	maxDataSTAValue = 0
	minDataSTAValue = 0
	for unitFile in os.listdir(sourceFolder):
		unitName = unitFile.rsplit('_', 1)[0]
		if os.path.isdir(sourceFolder+unitFile):
			# The STA matrix is named as M8a_lineal/sta_array_M8a.mat
			staMatrixFile = scipy.io.loadmat(sourceFolder+unitFile+'/sta_array_'+unitName+'.mat')
			staMatrix = staMatrixFile['STA_array']
			staMatrix = staMatrix[:,:,1:18]
			
			dataUnit, coordinates = rfe.loadSTACurve(sourceFolder,unitFile,unitName)
			
			print unitName
			print 'coordinates',coordinates
			
			media = numpy.mean(staMatrix)
			maximo = numpy.amax(staMatrix)
			minimo = numpy.amin(staMatrix)
			maximaDistancia = numpy.absolute(maximo-media)
			minimaDistancia = numpy.absolute(minimo-media) 
			if maximaDistancia > minimaDistancia:
				frame = numpy.where(maximo==staMatrix)[2][0]
				linea = '"'+unitName+'"\t"On"\t"'+ str(frame + 1) + '\"\n'
				data = gf.moments(staMatrix[:,:,frame],circle=0,rotate=1,vheight=1)
				print 'frame',frame
				print 'height',data[0]
				print 'amplitude',data[1]
				print 'x',data[2]
				print 'y',data[3]
				print 'width_x',data[4]
				print 'width_y',data[5]
				print 'rotation',data[6]
							
				dataFit = gf.gaussfit(staMatrix[:,:,frame],autoderiv=1, \
				 return_all=1,circle=0,fixed=numpy.repeat(False,7), \
				 limitedmin=[False,False,False,False,True,True,True], \
				 limitedmax=[False,False,False,False,False,False,True], \
				 usemoment=[1,1,1,1],minpars=numpy.repeat(0,7),maxpars=[0,0,0,0,0,0,360], \
				 rotate=1,vheight=1,quiet=True,returnmp=False, \
				 returnfitimage=True)

				fig = plt.figure(1, figsize=(10,10))
				ax = fig.add_subplot(111)
				plt.imshow(dataFit[1])

				plt.savefig("/tmp/"+unitName+".png")
				plt.close()
			else:
				linea = '"'+unitName+'"\t"Off"\t"'+ str(numpy.where(minimo==staMatrix)[2][0]) + '\"\n'
				frame = numpy.where(minimo==staMatrix)[2][0]
				linea = '"'+unitName+'"\t"On"\t"'+ str(frame + 1) + '\"\n'
				data = gf.moments(staMatrix[:,:,frame],circle=0,rotate=1,vheight=1)
				print 'frame',frame
				print 'height',data[0]
				print 'amplitude',data[1]
				print 'x',data[2]
				print 'y',data[3]
				print 'width_x',data[4]
				print 'width_y',data[5]
				print 'rotation',data[6]
				
				dataFit = gf.gaussfit(staMatrix[:,:,frame],autoderiv=1, \
				 return_all=1,circle=0,fixed=numpy.repeat(False,7), \
				 limitedmin=[False,False,False,False,True,True,True], \
				 limitedmax=[False,False,False,False,False,False,True], \
				 usemoment=[1,1,1,1],minpars=numpy.repeat(0,7),maxpars=[0,0,0,0,0,0,360], \
				 rotate=1,vheight=1,quiet=True,returnmp=False, \
				 returnfitimage=True)

				fig = plt.figure(1, figsize=(10,10))
				ax = fig.add_subplot(111)
				plt.imshow(dataFit[1])

				plt.savefig("/tmp/"+unitName+".png")
				plt.close()
				
			file.write(linea)
	file.close
	return 0

if __name__ == '__main__':
	main()

