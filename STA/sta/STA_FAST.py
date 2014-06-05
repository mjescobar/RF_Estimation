#!/usr/bin/env python
#============================================================
# STA FAST CHAIN
# SPIKE TRIGGERED AVERAGE (STA) ALGORITHM FAST VERSION
# Do STA for a list of Unit Cells.
# AASTUDILLO ABRIL 2014
# 29 ABRIL2014
#
# This script use as stimuli ensemble a mat file containing
# the stimuli in its true dimensions 20x20 px.
#============================================================

#============================================================
# Package import section:
#============================================================

#============================================================
# Package import section:
#============================================================
import matplotlib     # Graph and plot library
matplotlib.use("Agg") # for save images without show it in windows (for server use)
import pylab as pl
import matplotlib.cm as cm      	  # plot lib
import matplotlib.pyplot as plt 	  # plot lib (for figures)
import mpl_toolkits.mplot3d.axes3d as p3d # 3D Plot lib

from matplotlib.pyplot import *  	    # plot lib python
from matplotlib.ticker import NullFormatter # ticker formatter

#-----------------------------------------------------------
# Methods, Signal processing, etc:
#-----------------------------------------------------------
import scipy 		      # numerical methods lib (like Matlab functions)
import scipy.io 	      # input output lib (for save matlab matrix)
import scipy.signal as signal # signal processing lib
import numpy as np 	      # numerical methods lib
import sys    # system lib
import os     # operative system lib
import random # Random number methods
import time 		# System timer options
import scipy.misc as scim # scientific python package for image basic process
import glob # package for get file names from files in a folder
import matplotlib.pyplot as plt

from pylab import * 	# laboratory and plot methods lib 
from scipy import misc
from PIL import Image, ImageChops
import argparse #argument parsing

# import gc # garbage collector

#=============================================
# Inputs
#=============================================
parser = argparse.ArgumentParser(prog='STA_FAST.py',
 description='Performs STA from a stimuli ensemble',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--getimagenames', default=0,
 help='0,1 load image name list with the stimulus ensemble',
 type=int, choices=[0, 1], required=False)
parser.add_argument('--openimagesandwrite', default=0,
 help='0,1 DO TESTS FOR READ AND WRITE IMAGES',
 type=int, choices=[0, 1], required=False)
parser.add_argument('--calculatemeanrf', default=0,
 help='0,1 LOAD ALL THE IMAGES FROM THE STIMULOS ENSEMBLE '+
 'AND CALCULATE THE MEAN STIMULUS',
 type=int, choices=[0, 1], required=False)
parser.add_argument('--algorithm', default=4,
 help='1,2,4 How to perform STA, '+
 '1 load all spike triggered stimuli,'+ 
 '2 for sequentially load'+
 '4 from text',
 type=int, choices=[1, 2], required=False)
parser.add_argument('--start',
 help='From which units should be processed',
 type=int, default='0', required=False)
parser.add_argument('--end',
 help='Up to which units should be processed',
 type=int, default='2', required=False)
parser.add_argument('--stafolder',
 help='Output folder',
 type=str, default='.', required=False)
parser.add_argument('--path',
 help='Path to files',
 type=str, default='.', required=False)
parser.add_argument('--folder',
 help='Folder with the stimuli files',
 type=str, default='.', required=True)
parser.add_argument('--filter',
 help='Filter for the stimuli images',
 type=str, default='*.txt')
parser.add_argument('--timefolder',
 help='SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS',
 type=str, default='.', required=False)
parser.add_argument('--syncfile',
 help='SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE'+
 'IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME',
 type=str, default='.', required=True)
parser.add_argument('--samplingRate',
 help='ADQUISITION SAMPLING RATE FOR THE RECORDS',
 type=int, default=20000, required=False)
parser.add_argument('--numberframes',
 help='NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALISE',
 type=int, default=18, required=False)
parser.add_argument('--numberframespost',
 help='number of frames posterior to each spike for STA windows',
 type=int, default=2, required=False)
parser.add_argument('--sizex',
 help='SIZE OF EACH FRAME IN PIXELS X',
 type=int, default=19, required=False)
parser.add_argument('--sizey',
 help='SIZE OF EACH FRAME IN PIXELS Y',
 type=int, default=19, required=False)
parser.add_argument('--dolog',
 help='0,1 logarithm analysis for plot',
 type=int, default=0, choices=[0, 1], required=False)
parser.add_argument('--stim_mini',
 help='Stimuli matrix',
 type=str, default='stim_mini.mat', required=True)
parser.add_argument('--characterisation',
 help='Characterisation',
 type=str, required=False)
parser.add_argument('--unit_files',
 help='File with Units to process',
 type=str, default='units_0003.txt', required=True)
args = parser.parse_args()


#=============================================
# GET SPIKE TIME FILE NAMES
#=============================================

archivosruta = args.path

archivosfolder = args.folder

archivofiltro = args.filter

# FOLDER NAME TO SAVE EACH FOLDER RESULTS
stafolder = args.stafolder

# SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
# IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
synchronyfile = args.syncfile

getimagenames = args.getimagenames #must be 0
openimagesandwrite = args.openimagesandwrite #must be 0
calculatemeanrf = args.calculatemeanrf #must be 0
tipoalgoritmo = args.algorithm

# FOLDER NAME TO LOAD STIMULUS ENSEMBLE: IMAGE STIMULUS FOLDER
# imageruta = 'C:/Users/ALIEN3/Desktop/'
# imagefolder = 'checkImages'
# imagefiltro = '*.png'

# SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS
timefolder = archivosfolder

# SET THE ADQUISITION SAMPLING RATE OF THE RECORDS
samplingRate = args.samplingRate # Hz

# SET THE NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALIZE:
# number of frames previous to each spike for STA windows
numberframes = args.numberframes
# number of frames posterior to each spike for STA windows
numberframespost = args.numberframespost

# SET THE SIZE OF EACH FRAME IN PIXELS
sizex = args.sizex #19
sizey = args.sizey #19

# set if do logarithm analysis for plot:
dolog = args.dolog

# load image mat file stim_mini
stimMini = args.stim_mini
if not os.path.isfile(stimMini):
	print 'File [' + stimMini + '] not found'
	sys.exit()
ensemble = scipy.io.loadmat(stimMini)

estimulos = ensemble['stim']
canal = 2 # same as choose channel 3 of RGB images
estim = np.zeros(( sizex , sizey , 100000 ))

# transform each image from rgb to grayscale
for ke in range(100000):
	rgb = estimulos[:,:,:,ke]
	gray = np.dot(rgb[...,:3], [0.299, 0.587, 0.144])
	estim[:,:,ke] = gray

estim = np.array(estim)

meanimagearray = np.add.reduce(estim,axis=2) // (1.0* 100000)

c = 1
inicio = args.start
final  = args.end

if inicio < 0:
	print ''
	print 'start can not be lesser than 0'
	sys.exit()
	
if inicio > final:
	print ''
	print 'start can not be lesser than end'
	sys.exit()
	
#vectores units y caracterizacion provienen de la tabla excel 
#pero como no la tenemos...la primera vez se deben ignorar

unit_files = args.unit_files
if not os.path.isfile(unit_files):
	print ''
	print 'File [' + unit_files + '] not found'
	sys.exit()
f = open( unit_files ,'r')
per_row = []
for line in f:
    per_row.append(line.split('\t'))
f.close()


#If the characterisationFile is not provided an array of length of the 
# units must be provided. 
characterisationFile = args.characterisation
if not characterisationFile:
	characterization = np.ones((len(per_row[0]),), dtype=np.int)
else:
	if not os.path.isfile(characterisationFile):
		print ''
		print 'File [' + characterisationFile + '] not found'
		sys.exit()
	else:
		characterization = np.loadtxt(characterisationFile)

#Final lesser than Start
if final > len(characterization):
	final=len(characterization)-inicio

# SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
# IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
if not os.path.isfile(synchronyfile):
	print ''
	print 'File [' + synchronyfile + '] not found'
	sys.exit()
inicio_fin_frame = np.loadtxt(synchronyfile)

vector_fin_frame = inicio_fin_frame[:,1]

vector_inicio_frame = inicio_fin_frame[:,0]

#--------------------------------------------------------
# load image file names list: (the file should exist before)
#--------------------------------------------------------
# cadena_texto = "image_filenames"
# contenedor = scipy.io.loadmat(stafolder+'/'+cadena_texto+'.mat')
# ifn2 = contenedor['ifn']
# del contenedor

try:
  os.mkdir( stafolder ) 
except OSError:
  pass

def sta_1():
	# LOAD ALL THE FRAMES ACCORDING TO THE TIME STAMPS OF THE CELL
	# NOT FUNCTIONAL ANYMORE
	limite3 = len(stimei)
	kframe = 0
	spk = np.zeros((500,500,numberframes,limite3))
	
	for kiter in range(limite3):
		kframe = stimei[kiter]
		for b in range(numberframes):
			print ' kiter: ',kiter, ' kframe: ',kframe, ' b: ',b
			line = ifn2[kframe-(numberframes-1)+ b ]
			imagen = scim.imread(line, flatten=True)
			spk[:,:,b,kiter] = imagen - meanimagearray

	N = len(stimei)
	STA = ( np.add.reduce(spk,axis=3) / (1.0 * N) ) 
	MEANSTA = ( np.add.reduce(STA,axis=2) / (1.0 * numberframes) )

def sta_2():
	# LOAD EACH FRAME AND CALCULATES THE STA SEQUENTIALLY
	timeAlgorithm2Ini = time.time()
	kframe = 0
	cadena_texto = "mean_image"
	contenedor = scipy.io.loadmat(stafolder+'/'+cadena_texto+'.mat')
	meanimagearray = contenedor['meanimagearray']
	del contenedor
	sizex = 380
	sizey = 380
	acumula = np.zeros((sizex,sizey,numberframes+numberframespost))
	print 'Get the spike triggered stimuli: \n '
	for kiter in range(limite3):
		timeProcessIni = time.time()
		kframe = stimei[kiter]
		for b in range(numberframes+numberframespost):
			line = ifn2[kframe-(numberframes-1)+ b]
			imagen = scim.imread( line, flatten=True )
			acumula[:,:,b] = acumula[:,:,b] + (imagen - meanimagearray)
		if kiter > len(stimei):
			break
		timeProcessFin = time.time() 
		tiempoDiferencia = timeProcessFin - timeProcessIni
		sys.stdout.write("\r%d%%" %((kiter+1)*100.0/limite3, ) ) 
		sys.stdout.flush()
	N = limite3 # len(stimei)
	STA = acumula // N
	print ' \n '
	minimosta = np.min(np.min(np.min(STA)))
	maximosta = np.max(np.max(np.max(STA)))
	print '\nmin sta ', minimosta, ' max sta ', maximosta
	if minimosta < 0:
		STA_desp = STA + np.abs(minimosta) # lineal shift
	if minimosta >= 0:
		STA_desp = STA - np.abs(minimosta) # lineal shift
	minimosta_desp = np.min(np.min(np.min(STA_desp)))
	maximosta_desp = np.max(np.max(np.max(STA_desp)))
	print 'min sta with bias', minimosta_desp
	print 'max sta with bias', maximosta_desp
	stavisual_lin = STA_desp*255 # it is visualized with lineal scale
	stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
	print 'min sta visual lineal', np.min(np.min(np.min(stavisual_lin)))
	print 'max sta visual lineal', np.min(np.max(np.max(stavisual_lin)))
	# FINAL NORMALIZATION FOR THE MEAN STA
	MEANSTA_lin =  np.add.reduce(stavisual_lin,axis=2) 
	timeAlgorithm2End = time.time()
	timeAlgorithm2Total = timeAlgorithm2End - timeAlgorithm2Ini
	print " Time process ", timeAlgorithm2Total, ' seg (', timeAlgorithm2Total/60, ' min)'

def sta_3():
	timeAlgorithm3Ini = time.time()
	print 'Get the spike triggered stimuli: \n '
	sizechunk = 40
	sizesmall = 20
	acumula = np.zeros((sizex,sizey,numberframes+numberframespost))
	if dosmall:
		acumulaSmall = np.zeros((sizesmall,sizesmall,numberframes+numberframespost))
	for kblock in range(np.round(limite3/sizechunk)):
		spk = np.zeros((sizex,sizey,numberframes+numberframespost,sizechunk))
		if dosmall:
			spkSmall = np.zeros((sizesmall,sizesmall,numberframes+numberframespost,sizechunk))
		for kiter in range(sizechunk):
			kframe = stimei[kiter+kblock*sizechunk]
			for b in range(numberframes+numberframespost):
				line = ifn2[kframe-(numberframes-1)+ b ]
				imagen = scim.imread(line, flatten = True )
				if dosmall:
					imagenSmall = scipy.misc.imresize(imagen, [sizesmall,sizesmall] , interp = 'bilinear' , mode = None )
				spk[:,:,b,kiter] = imagen
				if dosmall:
					spkSmall[:,:,b,kiter] = imagenSmall
		del imagen
		del line
		if dosmall:
			del imagenSmall
		acuchunk = ( np.add.reduce(spk,axis=3) ) 
		acumula[:,:,:] = acumula[:,:,:] + acuchunk
		if dosmall:
			acuchunkSmall = ( np.add.reduce(spkSmall,axis=3) )
			acumulaSmall[:,:,:] = acumulaSmall[:,:,:] + acuchunkSmall
		if kblock > np.round(limite3/sizechunk):
			break
		sys.stdout.write("\r%d%%" % ((kblock+1)*100.0 /(np.round(limite3/sizechunk)), ) )
		sys.stdout.flush()
	N = limite3 
	STA = acumula // N
	for b in range(numberframes+numberframespost):
		STA[:,:,b] = STA[:,:,b] - meanimagearray
	if dosmall:
		meansmall = scipy.misc.imresize(meanimagearray,[sizesmall,sizesmall], interp='bilinear', mode=None)
		STASmall = acumulaSmall // N
		for b in range(numberframes+numberframespost):
			STASmall[:,:,b] = STASmall[:,:,b] - meansmall
	print ' \n '
	minimosta = np.min(np.min(np.min(STA)))
	maximosta = np.max(np.max(np.max(STA)))
	if minimosta < 0:
		STA_desp = STA + np.abs(minimosta) # lineal shift
	if minimosta >= 0:
		STA_desp = STA - np.abs(minimosta) # lineal shift
	minimosta_desp = np.min(np.min(np.min(STA_desp)))
	maximosta_desp = np.max(np.max(np.max(STA_desp)))
	stavisual_lin = STA_desp*255 # it is visualized with lineal scale
	stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
	# FINAL NORMALIZATION FOR THE MEAN STA
	MEANSTA_lin = ( np.add.reduce(stavisual_lin,axis=2) / (1.0 * (numberframes+numberframespost) ) )
	if dosmall:
		minstasmall = np.min(np.min(np.min(STASmall)))
		maxstasmall = np.max(np.max(np.max(STASmall)))
		if minstasmall < 0:
			STA_Small_desp = STASmall + np.abs(minstasmall) # lineal shift
		if minstasmall >= 0:
			STA_Small_desp = STASmall - np.abs(minstasmall) # lineal shift
		minstasmall_desp = np.min(np.min(np.min(STA_Small_desp)))
		maxstasmall_desp = np.max(np.max(np.max(STA_Small_desp)))
		sta_small_visual_lin = STA_Small_desp * 255 # it is visualized with lineal scale
		sta_small_visual_lin = sta_small_visual_lin // (maxstasmall_desp *1.0) # it is normalized with lineal scale
		# FINAL NORMALIZATION FOR THE MEAN STA
		MEAN_STA_small_lin = ( np.add.reduce(sta_small_visual_lin,axis=2) / (1.0 * (numberframes+numberframespost) ) )
			
	timeAlgorithm3End = time.time()
	timeAlgorithm3Total = timeAlgorithm3End - timeAlgorithm3Ini
	print " Time process ", timeAlgorithm3Total, ' seg (', timeAlgorithm3Total/60, ' min)'

def sta_4():
	timeAlgorithm4Ini = time.time()
	stac = np.zeros( ( sizex,sizey, numberframes+numberframespost ) ) # complete sta matrix 
	for numeroframe in range(numberframes): #for 18 frames
		bigsta18 = np.zeros( ( sizex,sizey ) )
		for kiter in range(len(stimei)):
			bigsta18[:,:] = bigsta18[:,:] + estim[ :,:,stimei[kiter]-numeroframe ] - meanimagearray
		sta18 = bigsta18 / (1.0 * len(stimei) ) # one part of the sta matrix
		stac[:,:,numberframes-1 - numeroframe] = sta18
	acumula = np.zeros((sizex,sizey,numberframes+numberframespost))
	STA = stac
	print ' \n '
	minimosta = np.min(np.min(np.min(STA)))
	maximosta = np.max(np.max(np.max(STA)))
	STA_desp = STA - minimosta
	minimosta_desp = np.min(np.min(np.min(STA_desp)))
	maximosta_desp = np.max(np.max(np.max(STA_desp)))
	stavisual_lin = STA_desp * 255 # it is visualized with lineal scale
	stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
	# FINAL NORMALIZATION FOR THE MEAN STA
	MEANSTA_lin = ( np.add.reduce(stavisual_lin,axis=2) / (1.0 * (numberframes+numberframespost) ) )
	timeAlgorithm4End = time.time()
	timeAlgorithm4Total = timeAlgorithm4End - timeAlgorithm4Ini
	print " Time process ", timeAlgorithm4Total, ' seg (', timeAlgorithm4Total/60, ' min)'
	print '\nsize STA: ',len(STA),'x',len(STA[0]),'x',len(STA[0][0])
	return (STA , stavisual_lin, MEANSTA_lin, STA_desp, acumula)


for kunit in range(inicio,final):
	timestampName = per_row[0][kunit]
	
	print timestampName,' ',characterization[kunit]
	if characterization[kunit] > 0:
		print 'Analysing Unit ',timestampName, ' loop :', c ,' unit n ', c + inicio
		print '---------------------BEGIN---------------------------'
		#--------------------------------------------------------
		# get spike time stamps from file 
		#--------------------------------------------------------
		neurontag = timestampName # tag or number of cell
		rastercelulatxtfile = timefolder + timestampName +'.txt'
		timestamps = np.loadtxt(rastercelulatxtfile) # text file containing time spikes in datapoints
		neuronresultfolder_lin = str(neurontag)+'_lineal'
		try:
		  os.mkdir( stafolder+'/'+neuronresultfolder_lin ) # create the folder
		except OSError:
		  pass		
		finalfolder_lin = stafolder+'/'+neuronresultfolder_lin
		print 'size time stamps vector: ', len(timestamps) #, 'x',len(timestamps[0])
		#--------------------------------------------------------
		# get time spikes depending of the stimulus start (frame do not start in time=0)
		#--------------------------------------------------------
		#--------------------------------------------------------
		# Conversion of spike times from seconds to POINTS:
		#--------------------------------------------------------
		vector_spikes = timestamps[:]*samplingRate # without first id zero column (1 COLUMMN)
		stimei = []  # initialize time spike index depending of image time
		spikeframe_matrix = np.zeros( (len(vector_spikes), 4) ) # [spike time, frame id, ini time frame, end time frame]
		#--------------------------------------------------------
		# convert stimes (SPIKE TIMES) to frame indexes (image index):
		#--------------------------------------------------------
		primer_frame = 0
		frame_ant = 0
		print 'Get the spike triggered stimuli indices: \n'
		contator = 0
		contator2 = 0
		totalcont = len(vector_spikes) * len(range(primer_frame, len(vector_fin_frame)))
		for punto_spike in vector_spikes:
			condicion = 1			
			for i in range(primer_frame, len(vector_fin_frame)):
				if (vector_inicio_frame[i] < punto_spike) & (punto_spike <= vector_fin_frame[i]):
					# if the spike time is into a frame time points (start and ends)
					spikeframe_matrix[contator,0] = punto_spike
					spikeframe_matrix[contator,1] = vector_fin_frame[i]
					spikeframe_matrix[contator,2] = inicio_fin_frame[i,0]
					spikeframe_matrix[contator,3] = inicio_fin_frame[i,1]
					stimei.append(i)
					frame_ant = i
					break
			sys.stdout.write("\r%d%%" %contator2)
			sys.stdout.flush()			
			contator = contator + 1 #
			contator2 = contator * 100 // ( 1.0 * len(vector_spikes) )		
			primer_frame = frame_ant
		print '\n'	
		limite3 = len(stimei)
		print 'length frames times vector', len(vector_fin_frame)
		print "length time stamps vector: ", len(timestamps)
		print "length spike triggered stimuli time i vector: ", len(stimei)
		#--------------------------------------------------------
		# STA Algorithm
		#--------------------------------------------------------

		#------------------- ALGORITHM TYPE 1----------------------
		if(tipoalgoritmo == 1):
			sta_1()	

		#------------------- ALGORITHM TYPE 2----------------------
		if(tipoalgoritmo == 2): # sequentially algorithm
			sta_2()
		dosmall = 0

		#------------------- ALGORITHM TYPE 3----------------------
		if(tipoalgoritmo == 3): # LOAD CHUNKS OF FRAMES AND CALCULATES THE STA SEQUENTIALLY
			sta_3()
			
		#===============================================================================
		#------------------- ALGORITHM TYPE 4----------------------
		if(tipoalgoritmo == 4): # LOAD entire matrix stimuli AND CALCULATES THE STA SEQUENTIALLY
			STA , stavisual_lin , MEANSTA_lin, STA_desp, acumula = sta_4()
			
		#----------------------------------------------------
		# save spike time stamp and frame index
		#----------------------------------------------------
		spikeframe_matrix_array =  np.array(spikeframe_matrix)
		spikeframe_filename = "spikeframe_matrix"+str(neurontag)
		print "Save spike frame matrix as mat file: ",spikeframe_filename
		scipy.io.savemat(finalfolder_lin+'/'+spikeframe_filename+'.mat',mdict={'spikeframe_matrix':spikeframe_matrix_array},oned_as='column')

		#----------------------------------------------------
		# save true STA matrix (NON SCALED for visual plot)
		#----------------------------------------------------
		STA_array = np.array(STA)
		cadena_texto = "sta_array_"+str(neurontag)
		print "Saving NON rescaled STA as mat file: ",cadena_texto
		scipy.io.savemat(finalfolder_lin+'/'+cadena_texto+'.mat',mdict={'STA_array':STA_array},oned_as='column')
		
		#----------------------------------------------------
		# save visual STA matrix ( RE SCALED for visual plot)
		#----------------------------------------------------
		stavisual_lin_array = np.array(stavisual_lin)
		cadena_texto = "stavisual_lin_array_"+str(neurontag)
		print "Saving visual STA (lineal) as mat file: ",cadena_texto
		scipy.io.savemat(finalfolder_lin+'/'+cadena_texto+'.mat',mdict={'STAarray_lin':stavisual_lin_array},oned_as='column')

		print 'Saving images in lineal scale...'
		
		plt.clf()
		fig = plt.figure(1, figsize=(12,10))
		
		ax = fig.add_subplot(3,6,1)
		component = stavisual_lin[:,:,0]
		ax.pcolormesh( component,vmin = 0,vmax = 255, cmap=cm.jet )
		ax.set_yticklabels([])
		ax.set_xticklabels([])
		ax.set_aspect(1)
		
		kcontador = 2
		for ksubplot in range(17):
			ax = fig.add_subplot(3,6,kcontador)
			component = stavisual_lin[:,:,kcontador-1]
			ax.pcolormesh( component,vmin = 0,vmax = 255, cmap=cm.jet )
			ax.set_aspect(1)
			ax.set_yticklabels([])
			ax.set_xticklabels([])
			kcontador = kcontador + 1
		
		plt.savefig(finalfolder_lin+"/STA-"+str(neurontag)+"_.png",format='png', bbox_inches='tight')
		plt.savefig(stafolder+"/STA-"+str(neurontag)+"_.png",format='png', bbox_inches='tight')
		plt.show()        
		plt.clf()
		#------------------------------------------------------

		print 'Saving mean image in lineal scale...'
		pl.figure()
		im = pl.pcolormesh(MEANSTA_lin,vmin = 0,vmax = 255, cmap=cm.jet)
		pl.jet()
		pl.colorbar(im)
		ax = pl.axes()
		ax.set_yticklabels([])
		ax.set_xticklabels([])
		pl.savefig(finalfolder_lin+"/MEANSTA-g_"+str(neurontag)+".png",format='png', bbox_inches='tight')
		print 'CELL ' + timestampName + ' FINISHED!!!'
		print '-----------------------END---------------------------'
		del STA_desp 
		del STA 
		del stavisual_lin 
		del spikeframe_matrix
		del acumula
	c = c +1

