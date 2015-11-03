#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  graficaGratings.py
#  
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

from numpy import loadtxt,array,pi,amax
import argparse 							#argument parsing
from platform import system				# Windows or Linux?
import sys, os
from matplotlib.pyplot import figure,subplot,polar,legend,show,rc \
	,savefig,suptitle,close

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
	angle = [0, 45, 90, 135, 180, 225, 270, 315, 0]
	angle = array(angle)*pi/180 

	parser = argparse.ArgumentParser(prog='calculaMeans.py',
	 description='Calcula los means de cada unidad',
	 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--sourceFolder125',
	 help='Source folder 125',
	 type=str, required=True)
	parser.add_argument('--sourceFolder250',
	 help='Source folder 250',
	 type=str, required=True)
	parser.add_argument('--outputFolder',
	 help='Output folder',
	 type=str, required=True)
	 	 	 
	args = parser.parse_args()
	
	sourceFolder125 = fixPath(args.sourceFolder125)
	if not os.path.exists(sourceFolder125):
		print ''
		print 'Source folder does not exists ' + sourceFolder125
		print ''
		sys.exit()

	sourceFolder250 = fixPath(args.sourceFolder250)
	if not os.path.exists(sourceFolder250):
		print ''
		print 'Source folder does not exists ' + sourceFolder250
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
		
	cols=[1,2,3,4,5,6,7,8,9]
	v2_125 = loadtxt(sourceFolder125+'v2.csv', delimiter=',',skiprows=1,usecols=cols)
	v4_125 = loadtxt(sourceFolder125+'v4.csv', delimiter=',',skiprows=1,usecols=cols)
	v8_125 = loadtxt(sourceFolder125+'v8.csv', delimiter=',',skiprows=1,usecols=cols)
	v2_250 = loadtxt(sourceFolder250+'v2.csv', delimiter=',',skiprows=1,usecols=cols)
	v4_250 = loadtxt(sourceFolder250+'v4.csv', delimiter=',',skiprows=1,usecols=cols)
	v8_250 = loadtxt(sourceFolder250+'v8.csv', delimiter=',',skiprows=1,usecols=cols)
	
	units = loadtxt(sourceFolder125+'v2.csv', delimiter=',',skiprows=1,usecols=[0],dtype='str')
	
	rc('xtick', labelsize=10)
	rc('ytick', labelsize=8)
	for unit in range(len(units)):
		unitName=units[unit].replace('\"', '')
		mv2_125=amax(v2_125[unit,:])
		mv4_125=amax(v4_125[unit,:])
		mv8_125=amax(v8_125[unit,:])
		mv2_250=amax(v2_250[unit,:])
		mv4_250=amax(v4_250[unit,:])
		mv8_250=amax(v8_250[unit,:])
		maximoValor=max(mv2_125,mv4_125,mv8_125,mv2_250,mv4_250,mv8_250)		
		figure('Unit 125 v2 '+unitName)
		suptitle('Unit 125 v2 '+unitName,fontsize=15)
		ax = subplot(111, polar=True)		
		ax.plot(angle, v2_125[unit,:], 'b', linewidth=3, label='v2')
		ax.set_rmax(maximoValor)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		savefig(outputFolder+unitName+'_v2_125.pdf',format='pdf')
		close()
		figure('Unit 125 v4 '+unitName)
		suptitle('Unit 125 v4 '+unitName, fontsize=15)
		ax = subplot(111, polar=True)		
		ax.plot(angle, v4_125[unit,:], 'b', linewidth=3, label='v4')
		ax.set_rmax(maximoValor)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		savefig(outputFolder+unitName+'_v4_125.pdf',format='pdf')
		close()
		figure('Unit 125 v8 '+unitName)
		suptitle('Unit 125 v8 '+unitName, fontsize=15)
		ax = subplot(111, polar=True)		
		ax.plot(angle, v8_125[unit,:], 'b', linewidth=3, label='v8')
		ax.set_rmax(maximoValor)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		savefig(outputFolder+unitName+'_v8_125.pdf',format='pdf')
		close()
		
		figure('Unit 250 v2 '+unitName)
		suptitle('Unit 250 v2 '+unitName, fontsize=15)
		ax = subplot(111, polar=True)		
		ax.plot(angle, v2_250[unit,:], 'r', linewidth=3, label='v2')
		ax.set_rmax(maximoValor)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		savefig(outputFolder+unitName+'_v2_250.pdf',format='pdf')
		close()
		figure('Unit 250 v4 '+unitName)
		suptitle('Unit 250 v4 '+unitName, fontsize=15)
		ax = subplot(111, polar=True)		
		ax.plot(angle, v4_250[unit,:], 'r', linewidth=3, label='v4')
		ax.set_rmax(maximoValor)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		savefig(outputFolder+unitName+'_v4_250.pdf',format='pdf')
		close()
		figure('Unit 250 v8 '+unitName)
		suptitle('Unit 250 v8 '+unitName, fontsize=15)
		ax = subplot(111, polar=True)		
		ax.plot(angle, v8_250[unit,:], 'r', linewidth=3, label='v8')
		ax.set_rmax(maximoValor)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		savefig(outputFolder+unitName+'_v8_250.pdf',format='pdf')
		close()
		
	return 0

if __name__ == '__main__':
	main()

