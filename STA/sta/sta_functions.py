#============================================================
# AASTUDILLO 2014
#============================================================
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

def sta_each( getimagenames,openimagesandwrite,calculatemeanrf,tipoalgoritmo,timestampName ,stafolder ,imageruta ,imagefolder ,imagefiltro ,timefolder ,samplingRate ,numberframes ,numberframespost , synchronyfile ,sizex ,sizey, dolog):
	#=============================================
	# GET INPUTS: initial options
	#=============================================

	# # LOAD DE IMAGE NAME LIST WITH THE STIMULUS ENSEMBLE
	# getimagenames = int(sys.argv[1]) #0 

	# # DO TESTS FOR READ AND WRITE IMAGES
	# openimagesandwrite = int(sys.argv[2]) #0 

	# # LOAD ALL THE IMAGES FROM THE STIMULOS ENSEMBLE AND CALCULATE THE MEAN STIMULUS
	# calculatemeanrf = int(sys.argv[3]) #0 

	# # defines how to do the STA process: 
	# # 1 for load all spike triggered stimuli, 2 for sequentially load
	# tipoalgoritmo = int(sys.argv[4]) #2

	# # DEFINE THE NAME OF THE TXT FILE WITH TIME STAMPS FOR LOAD:
	# timestampName = (sys.argv[5]) #C1a 

	# =============================================
	# SET OTHERS OPTIONS
	# =============================================

	# FOLDER NAME TO SAVE EACH FOLDER RESULTS
	# stafolder = 'STA_datos0005'

	# # FOLDER NAME TO LOAD STIMULUS ENSEMBLE: IMAGE STIMULUS FOLDER
	# imageruta = 'D:/'
	# imagefolder = 'checkImages'
	# imagefiltro = '*.png'

	# # SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS
	# timefolder = 'TS_datos0005/'

	# # SET THE ADQUISITION SAMPLING RATE OF THE RECORDS
	# samplingRate = 20000 # Hz

	# # SET THE NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALIZE:
	# # number of frames previous to each spike for STA windows
	# numberframes = 13 
	# # number of frames posterior to each spike for STA windows
	# numberframespost = 5 

	# # SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
	# # IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
	# synchronyfile = 'inicio_fin_frame_datos0005.txt'
	inicio_fin_frame = np.loadtxt(synchronyfile)

	# # SET THE SIZE OF EACH FRAME IN PIXELS
	# sizex = 380 #500 #750
	# sizey = 380 #500 #700

	# # set if do logarithm analysis for plot:
	# dolog = 0

	print '---------------------BEGIN---------------------------'

	#--------------------------------------------------------
	# creates STA result folder
	# if folder "STA" don't exist, create the folder
	#--------------------------------------------------------
	try:
	  os.mkdir( stafolder ) 
	except OSError:
	  pass

	#============================================================
	# Get the image names (optional)
	# This stage is performed the first time of analysis only.
	# For each different stimuli ensemble files, this list has 
	# been created the first time of analysis once.
	#============================================================
	#getimagenames = 0
	if(getimagenames == 1):
		#--------------------------------------------------------
		# get image file names from folder
		#--------------------------------------------------------
		
		#imageruta = '../../VIRTUALWIN/cinv_datos_05-06-2013/'
		#imageruta = '../cinv_datos23-4-2013/'
		#imageruta = '/media/Datos/STA_RVM/Datos 13-11-2013/' #Se aplica el mismo estimulo de la semana anterior
		#imageruta = 'D:\Users\ALIEN3\Desktop/'
		# imageruta = 'D:/'

		# #imagefolder = 'random blanco y negro, cuadrados de 40x40 pixeles'
		# imagefolder = 'checkImages'
		
		# imagefiltro = '*.png'

		globstring     =  imageruta + imagefolder +'/'+ imagefiltro
		
		imagefilenames = glob.glob(globstring) # get file names from folder

		imagefilenames.sort()

		print "\t length imagefilenames: ", len(imagefilenames)
		print "\t last imagefilenames : ",imagefilenames[len(imagefilenames)-1]

		#--------------------------------------------------------
		# save image name list to matlab file
		#--------------------------------------------------------
		ifn = np.array(imagefilenames)
		cadena_texto = "image_filenames"
		print "\t Saving image names as mat file: ",cadena_texto
		scipy.io.savemat(stafolder+'/'+cadena_texto+'.mat',mdict={'ifn':ifn},oned_as='column')
		
		#--------------------------------------------------------
		# save image name list to txt file
		#--------------------------------------------------------
		try:
			print "\t Saving image names as mat txt: ",cadena_texto
			configFile = open(stafolder+'/'+cadena_texto+'.txt', 'w')
			
			for parameter in ifn:
				configFile.write( ''+str(parameter)+' \n' ) 
				
			configFile.close
	  
		except OSError:
			pass	


	#--------------------------------------------------------
	# load image file names list:
	# (the file should exist before)
	#--------------------------------------------------------
	cadena_texto = "image_filenames"
	#print "\t Loading image names from mat file: ",cadena_texto
	contenedor = scipy.io.loadmat(stafolder+'/'+cadena_texto+'.mat')
	ifn2 = contenedor['ifn']
	del contenedor

	# print "\t length imagefilenames: ", len(ifn2 )
	# print "\t last imagefilenames : ",ifn2 [len(ifn2 )-1]
	# print "\n"

	#============================================================
	# Load images and write each image as a vector:
	# This stage is only a test for load and save images from 
	# original stimuli images.
	# The important issue is to load correctly images for the 
	# use of all information of each frame, using grey scale or 
	# RGB or others channels.
	#============================================================
	#openimagesandwrite = 0
	if(openimagesandwrite == 1):

	   stimuli =[]  # initialize stimuli matrix to keep images as vectors
	   
	   contador = 0 # to get a defined number of images (abac)
	   
	   limite = 5   # define the number of images to load using the image file name list
	   
	   imagefilenames = ifn2

	   for line in imagefilenames:
		print '\t Loading stimuli: '+ line # show inline image name
		#--------------------------------------------------------
		# load as gray scale image:
		#--------------------------------------------------------
		imagen = scim.imread(line, flatten = True) # read one image as gray scale

		tamanox = len(imagen)
		tamanoy = len(imagen[0])
		tamanomin = np.min([tamanox,tamanoy])
		
		print '\t size imagen : ', tamanox, 'x',tamanoy
		
		imagenvector = np.zeros( ( 1,tamanomin*tamanomin ) ) # initialize vector for keep image
			
		k = 0
		for i in range(tamanomin): # over image x,y coordinates, for keep image matrix as row vector
		   for j in range(tamanomin):
			  imagenvector[0,k] = imagen[i,j] # keep one image pixel as one vector element
			  k = k+1 	# for next element
			  
		stimuli.append( imagenvector ) # add image row vector and a group in a big matrix [MxN]

		saveplot = 1
		
		if saveplot:
			
			pl.figure()
			im = pl.imshow(imagen,interpolation = 'none')
			pl.gray() #pl.hot()
			#pl.clim(mini,maxi)
			pl.contour(imagen)
			pl.colorbar(im)
			ax = pl.axes()
			ax.set_yticklabels([])
			ax.set_xticklabels([])
			#ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
			pl.savefig(stafolder+"/gray_frame-"+str(contador)+"-g.png",format='png', bbox_inches='tight')

			contador = contador + 1 # counting images of the ensemble
			
		if contador==limite: 
				break


	#============================================================
	# Calculate the mean frame image for the entire stimuli 
	# ensemble. This calculation can be performed in one big load
	# or sequentially.
	#============================================================
	#calculatemeanrf = 0
	if(calculatemeanrf==1):
		#---------------------------------------------------
		# get all images and calculate the mean frame image
		#---------------------------------------------------
		
		limite2 = len(ifn)-1 #100000
		
		contador = 0
		
		#tamanomin = 700
		
		imagenvector = np.zeros( ( 1 ,tamanomin*tamanomin ) )

		vectoracumula = imagenvector
		
		#tamanox = 700
		#tamanoy = 750
		
		imagenacumula = np.zeros( ( tamanox , tamanoy ) )

		for line in imagefilenames:
			print 'load id: ', contador #,' Loading stimuli: '+line # show inline image name
			#--------------------------------------------------------
			# load as gray scale image:
			#--------------------------------------------------------
			imagen = scim.imread(line, flatten=True) # read one image as grayscale

			imagenacumula = imagenacumula + imagen
			
			#stimuli.append( imagenvector ) # add image row vector and add to bigmatrix [MxN]

			contador = contador + 1 # counting images of the ensemble
			if contador==limite2: 
					break

		meanimage = imagenacumula // (limite2*1.0)

		meanimagearray = np.array(meanimage)
		
		cadena_texto = "mean_image"
		print "\t Saving mean image as mat file: ",cadena_texto
		scipy.io.savemat(stafolder+'/'+cadena_texto+'.mat',mdict ={'meanimagearray':meanimagearray},oned_as='column')

		#--------------------------------------------------------
		# save mean frame as image:
		#--------------------------------------------------------
		pl.figure()
		#im = pl.imshow(component,interpolation='bicubic')
		im = pl.imshow(meanimage,interpolation = 'none')
		pl.gray() #pl.hot()
		#pl.clim(mini,maxi)
		pl.contour(meanimage)
		pl.colorbar(im)
		ax = pl.axes()
		ax.set_yticklabels([])
		ax.set_xticklabels([])
		#ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
		pl.savefig(stafolder+"/mean_gray_frame-g.png",format='png', bbox_inches='tight')


	#============================================================
	# DO STA
	#============================================================

	#--------------------------------------------------------
	# get spike time stamps from file 
	#--------------------------------------------------------

	#timefolder = 'ss_dMCD_fs20_nb1218_f2_CINV-25-06-2013-RANDOM-1/'
	# timefolder = 'TS_datos0001/'

	# nb = 1218 # number of blocks
	# e  = 15 # 10 #9 #8 # number of electrode
	# nc = 0 # 2 #0 # number of cluster

	#timestampName = 'M10a'

	#neurontag = 'e_'+timestampName # tag or number of cell
	neurontag = timestampName # tag or number of cell

	rastercelulatxtfile = timefolder + timestampName +'.txt'
	#rastercelulatxtfile = timestampName
	
	timestamps = np.loadtxt(rastercelulatxtfile) # text file containing time spikes in datapoints

	#limite3 = 820 #37928 #218 #800 # limit number of spikes to analize

	# neuronresultfolder_lin = 'cell_'+str(neurontag)+'_lineal'
	# neuronresultfolder_log = 'cell_'+str(neurontag)+'_log'
	neuronresultfolder_lin = str(neurontag)+'_lineal'
	neuronresultfolder_log = str(neurontag)+'_log'

	# CREATE SUBFOLDERS
	try:
	  os.mkdir( stafolder+'/'+neuronresultfolder_lin ) # create the folder
	except OSError:
	  pass
	  
	if dolog ==1:
		try:
		  os.mkdir( stafolder+'/'+neuronresultfolder_log ) # create the folder
		except OSError:
		  pass
	  
	finalfolder_lin = stafolder+'/'+neuronresultfolder_lin
	finalfolder_log = stafolder+'/'+neuronresultfolder_log

	#rastercelulatxtfile = timefolder+'isi_spktimes_nb'+str(nb)+'_e'+str(e)+'_nc'+str(nc)+'.txt'
	#rastercelulatxtfile = timefolder+'isi_spktimes_nb90_e17_nc0.txt'
	#rastercelulatxtfile = timefolder+'F1a.txt'
	#timestamps = np.loadtxt(rastercelulatxtfile) # text file containing time spikes in datapoints

	print 'size time stamps vector: ', len(timestamps) #, 'x',len(timestamps[0])

	#--------------------------------------------------------
	# set useful parameters
	#--------------------------------------------------------
	# samplingRate = 20000 #20000 Hz

	# #frameinicio = 31199 #31855-671+2 #1.00385e6 # points, inicio de la presentacion de frames 
	# #frameinicioms = 5.01925e4 # ms

	# #frameduracion = 334*2 #671 #668 #350 # points = (1.00455-1.0042)*10^6
	# #frameduracionms = 17.5 # ms 

	# numberframes = 13 # number of frames previous to each spike for STA windows
	# numberframespost = 5 # number of frames posterior to each spike for STA windows

	# inicio_fin_frame = np.loadtxt('inicio_fin_frame_datos0001.txt')
	#print (inicio_fin_frame)

	#--------------------------------------------------------
	# get time spikes depending of the stimulus start (frame do not start in time=0)
	#--------------------------------------------------------
	#timestamps2 = timestamps[timestamps[:,1]>frameinicio*2,1]
	#print 'size timestamps2: ', len(timestamps2)
	#stimes = (timestamps[:,1]-timeoffset)**(samplingRate/(1000*1.0)) # time spikes (second column of data) as vector

	#--------------------------------------------------------
	# Conversion from microseconds to seconds
	#--------------------------------------------------------
	#timestamps2 = timestamps[:,1]/1000000
	#print timestamps2[100,1]

	#--------------------------------------------------------
	# Conversion of spike times from seconds to POINTS:
	#--------------------------------------------------------
	#vector_spikes = timestamps[:,1]*samplingRate
	vector_spikes = timestamps[:]*samplingRate # without first id zero column (1 COLUMMN)
	#vector_spikes = timestamps[:,1]

	#print vector_spikes

	#punto_spike = timestamps[:,1]

	#print inicio_fin_frame[:,0]

	vector_fin_frame = inicio_fin_frame[:,1]
	vector_inicio_frame = inicio_fin_frame[:,0]

	# initialize time spike index depending of image time
	stimei = [] 

	spikeframe_matrix = np.zeros( (len(vector_spikes), 4) ) # [spike time, frame id, ini time frame, end time frame]

	#--------------------------------------------------------
	# convert stimes (SPIKE TIMES) to frame indexes (image index):
	#--------------------------------------------------------

	primer_frame = 0
	frame_ant = 0

	print 'first spike pos: ',vector_spikes[0],' last spike pos: ',vector_spikes[-1]
	print 'first frame begin at: ',inicio_fin_frame[0,0],' last frame ends at: ',inicio_fin_frame[-1,1]
	#print 'final: ',len(vector_spikes),' x ',len(vector_fin_frame),' = ',len(vector_spikes) * len(vector_fin_frame) 

	print 'Get the spike triggered stimuli indices: \n'

	contator = 0
	contator2 = 0
	totalcont = len(vector_spikes) * len(range(primer_frame, len(vector_fin_frame)))
	for punto_spike in vector_spikes:
		for i in range(primer_frame, len(vector_fin_frame)):
			if (vector_inicio_frame[i] < punto_spike) & (punto_spike <= vector_fin_frame[i]):
				# if the spike time is into a frame time points (start and ends)
				
				#print '\npunto de inicio de frame:\t',inicio_fin_frame[i,0]
				#print 'punto de spike:\t\t\t',punto_spike
				#print 'punto de final de frame:\t',inicio_fin_frame[i,1]
				spikeframe_matrix[contator,0] = punto_spike
				spikeframe_matrix[contator,1] = vector_fin_frame[i]
				spikeframe_matrix[contator,2] = inicio_fin_frame[i,0]
				spikeframe_matrix[contator,3] = inicio_fin_frame[i,1]
				
				#print '\r punto_spike: ',punto_spike, ' i: ',i
				stimei.append(i)
				frame_ant = i

				#contator2 = contator * 100 // (1.0 * len(vector_spikes) * len(vector_fin_frame) )
				#time.sleep(1)
				#sys.stdout.write("\r%d%%" %contator2, "%d%%" %contator)    # or print >> sys.stdout, "\r%d%%" %i,
				sys.stdout.write("\r%d%%" %contator2)
				sys.stdout.flush()
				
		contator = contator + 1 #
		#contator2 = contator * 100 // (1.0 * len(vector_spikes) * len(vector_fin_frame) )/47*100
		contator2 = contator * 100 // ( 1.0 * len(vector_spikes) )
			
				
		primer_frame = frame_ant
		#print primer_frame

	print '\n'	
	limite3 = len(stimei)
	print 'length frames times vector', len(vector_fin_frame)
	print "length time stamps vector: ", len(timestamps)
	print "length spike triggered stimuli time i vector: ", len(stimei)

	#puntos = 10
	#print " timestamps: ", (timestamps[0:puntos,1])
	#print " stimei: ", (stimei[0:puntos])

	#--------------------------------------------------------
	# load mean frame from mat file:
	#--------------------------------------------------------
	cadena_texto = "mean_image"
	#print "\t Loading mean frame from mat file: ",cadena_texto
	contenedor = scipy.io.loadmat(stafolder+'/'+cadena_texto+'.mat')
	meanimagearray = contenedor['meanimagearray']
	del contenedor

	#--------------------------------------------------------
	# STA Algorithm
	#--------------------------------------------------------
	#tipoalgoritmo = 2

	#------------------- ALGORITHM TYPE 1----------------------
	# LOAD ALL THE FRAMES ACCORDING TO THE TIME STAMPS OF THE CELL
	# NOT FUNCTIONAL ANYMORE
	if(tipoalgoritmo == 1):
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
		#sta = sum(spk, axis=1 (over column) ) / (1*Number_Spikes)
		MEANSTA = ( np.add.reduce(STA,axis=2) / (1.0 * numberframes) )

	#------------------- ALGORITHM TYPE 2----------------------
	# LOAD EACH FRAME AND CALCULATES THE STA SEQUENTIALLY
	if(tipoalgoritmo == 2): # sequentially algorithm

		kframe = 0
		
		# sizex = 380 #500 #750
		# sizey = 380 #500 #700
		
		acumula = np.zeros((sizex,sizey,numberframes+numberframespost))

		#timeProcessIni = time.time()

		print 'Get the spike triggered stimuli: \n '
		for kiter in range(limite3):
			timeProcessIni = time.time()
			
			kframe = stimei[kiter]
			
			for b in range(numberframes+numberframespost):
				#print 'b ',b
				line = ifn2[kframe-(numberframes-1)+ b]
				imagen = scim.imread( line, flatten=True )
				#spk[:,:,b,kiter] = imagen
				acumula[:,:,b] = acumula[:,:,b] + (imagen - meanimagearray)
				
			if kiter > len(stimei):
				break
				
			timeProcessFin = time.time() 
			tiempoDiferencia = timeProcessFin - timeProcessIni
			#print '\r kiter: ',kiter, ' kframe: ',kframe, '  ',"%.2f" % ((kiter+1)*100.0/limite3, ), ' % ' , (limite3 -(kiter+0)) * tiempoDiferencia/60, 'min'

			#sys.stdout.write("\r%d%%" %contator2)   
			#sys.stdout.write("\r%d%% %d%%" %((kiter+1)*100.0/limite3) %(limite3 -(kiter+0)) * tiempoDiferencia/60)    
			sys.stdout.write("\r%d%%" %((kiter+1)*100.0/limite3, ) ) 
			#sys.stdout.write("\r%d%%" %((limite3 -(kiter+0)) * tiempoDiferencia/60 ) ) 
			sys.stdout.flush()
			
			
		N = limite3 # len(stimei)

		STA = acumula // N
		
		print ' \n '

		minimosta = np.min(np.min(np.min(STA)))	
		maximosta = np.max(np.max(np.max(STA)))
		#print '\nmin sta ', minimosta, ' max sta ', maximosta
		if minimosta < 0:
			STA_desp = STA + np.abs(minimosta) # lineal shift
		if minimosta >= 0:
			STA_desp = STA - np.abs(minimosta) # lineal shift
		minimosta_desp = np.min(np.min(np.min(STA_desp)))
		maximosta_desp = np.max(np.max(np.max(STA_desp)))
		#print 'min sta with bias', minimosta_desp
		#print 'max sta with bias', maximosta_desp
		
		if dolog ==1:
			STA_log = log10(STA_desp + 1) # logarithmic normalization
			minimosta_log = np.min(np.min(np.min(STA_log)))
			maximosta_log = np.max(np.max(np.max(STA_log)))
			print 'min sta log ', minimosta_log
			print 'max sta log ', maximosta_log
			
		stavisual_lin = STA_desp*255 # it is visualized with lineal scale
		stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
		#print 'min sta visual lineal', np.min(np.min(np.min(stavisual_lin)))
		#print 'max sta visual lineal', np.min(np.max(np.max(stavisual_lin)))

		if dolog ==1:
			stavisual_log = STA_log*255 # it is visualized with logarithmic scale
			stavisual_log = stavisual_log // (maximosta_log *1.0) # it is normalized with logarithmic scale
			print 'min sta visual log', np.min(np.min(np.min(stavisual_log)))
			print 'max sta visual log', np.min(np.max(np.max(stavisual_log)))
		   
		# FINAL NORMALIZATION FOR THE MEAN STA
		MEANSTA_lin = ( np.add.reduce(stavisual_lin,axis=2) / (1.0 * (numberframes+numberframespost) ) )
		if dolog ==1:
			MEANSTA_log = ( np.add.reduce(stavisual_log,axis=2) / (1.0 * (numberframes+numberframespost) ) )
		
	#============================================================
	#============================================================

	print '\nsize STA: ',len(STA),'x',len(STA[0]),'x',len(STA[0][0])

	#----------------------------------------------------
	# save results
	#----------------------------------------------------

	spikeframe_matrix_array =  np.array(spikeframe_matrix)
	spikeframe_filename = "spikeframe_matrix"+str(neurontag)
	print "\t spikeframe_matrix as mat file: ",spikeframe_filename
	scipy.io.savemat(finalfolder_lin+'/'+spikeframe_filename+'.mat',mdict={'spikeframe_matrix':spikeframe_matrix_array},oned_as='column')


	stavisual_lin_array = np.array(stavisual_lin)
	cadena_texto = "stavisual_lin_array_"+str(neurontag)
	print "\t Saving visual STA (lineal) as mat file: ",cadena_texto
	scipy.io.savemat(finalfolder_lin+'/'+cadena_texto+'.mat',mdict={'STAarray_lin':stavisual_lin_array},oned_as='column')

	if dolog ==1:
		stavisual_log_array = np.array(stavisual_log)
		cadena_texto = "stavisual_log_array_"+str(neurontag)
		print "\t Saving visual STA (logarithmic) as mat file: ",cadena_texto
		scipy.io.savemat(finalfolder_log+'/'+cadena_texto+'.mat',mdict={'STAarray_log':stavisual_log_array},oned_as='column')

	# MEANSTAarray_lin = np.array(MEANSTA_lin)
	# cadena_texto = "MEANSTA_lin"+str(neurontag)
	# print "\t Saving STA as mat file: ",cadena_texto
	# scipy.io.savemat(finalfolder_lin+'/'+cadena_texto+'.mat',mdict={'MEANSTAarray_lin':MEANSTAarray_lin},oned_as='column')

	# MEANSTAarray_log = np.array(MEANSTA_log)
	# cadena_texto = "MEANSTA_log"+str(neurontag)
	# print "\t Saving STA as mat file: ",cadena_texto
	# scipy.io.savemat(finalfolder_log+'/'+cadena_texto+'.mat',mdict={'MEANSTAarray_log':MEANSTAarray_log},oned_as='column')

	print '\nSaving images in lineal scale...'
	for b in range(numberframes+numberframespost):
		#print 'Image ', b
		sys.stdout.write("\r Image %d" %(b ) ) 
		sys.stdout.flush()
		component = stavisual_lin[:,:,b] #STA[:,:,b]
		pl.figure()
		#im = pl.imshow(component,interpolation = 'none')
		#im = pl.pcolor( component,vmin = 0,vmax = 255, cmap=cm.jet )
		im = pl.pcolormesh( component,vmin = 0,vmax = 255, cmap=cm.jet )
		#pl.contour(component)
		pl.colorbar(im)
		ax = pl.axes()
		ax.set_yticklabels([])
		ax.set_xticklabels([])
		#ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
		pl.savefig(finalfolder_lin+"/STA-"+str(neurontag)+"-"+str(b)+"-g_.png",format='png', bbox_inches='tight')
		#pl.savefig(stafolder+"/STA-"+str(neurontag)+"-"+str(b)+"-g_.jpg",format='jpg', bbox_inches='tight')
		#del pl
		del component

	if dolog ==1:
		print '\nSaving images in logarithmic scale...'
		for b in range(numberframes+numberframespost):
			#print 'Image ', b
			sys.stdout.write("\r Image %d" %(b ) ) 
			sys.stdout.flush()
			component = stavisual_log[:,:,b] #STA[:,:,b]
			pl.figure()
			#im = pl.imshow(component,interpolation = 'none')
			#im = pl.pcolor(component,vmin = 0,vmax = 255, cmap=cm.jet)
			im = pl.pcolormesh( component,vmin = 0,vmax = 255, cmap=cm.jet )
			#pl.contour(component)
			pl.colorbar(im)
			ax = pl.axes()
			ax.set_yticklabels([])
			ax.set_xticklabels([])
			####ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
			pl.savefig(finalfolder_log+"/STA-"+str(neurontag)+"-"+str(b)+"-g_.png",format='png', bbox_inches='tight')
			#pl.savefig(stafolder+"/STA-"+str(neurontag)+"-"+str(b)+"-g_.jpg",format='jpg', bbox_inches='tight')'''
			#del pl
			del component

	#for b in range(numberframes+numberframespost):
	#	print 'Image ', b
	#	component = stavisual_lin[:,:,b]
	#	#im = pl.pcolor(component,vmin = 0,vmax = 255, cmap=cm.jet)	
	#	misc.imsave(finalfolder_lin+"/STA-"+str(neurontag)+"-"+str(b)+"-g_.png", component)
	#	#plt.imshow(component)
	#	#plt.show()
	#	myImC = Image.open(finalfolder_lin+"/STA-"+str(neurontag)+"-"+str(b)+"-g_.png")
	#   out = ImageChops.invert(myImC)
	#   out.save(finalfolder_lin+"/(inv)_STA-"+str(neurontag)+"-"+str(b)+"-g_.png")

	print '\nSaving mean image in lineal scale...'
	pl.figure()
	#im = pl.imshow(MEANSTA,interpolation = 'none')
	im = pl.pcolormesh(MEANSTA_lin,vmin = 0,vmax = 255, cmap=cm.jet)
	#pl.gray() 
	pl.jet()
	#pl.contour(MEANSTA)
	pl.colorbar(im)
	ax = pl.axes()
	ax.set_yticklabels([])
	ax.set_xticklabels([])
	#ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
	pl.savefig(finalfolder_lin+"/MEANSTA-g_"+str(neurontag)+".png",format='png', bbox_inches='tight')

	if dolog ==1:
		print 'Saving mean image in logarithmic scale...'
		pl.figure()
		#im = pl.imshow(MEANSTA,interpolation = 'none')
		im = pl.pcolormesh(MEANSTA_log,vmin = 0,vmax = 255, cmap=cm.jet)
		#pl.gray() 
		pl.jet()
		#pl.contour(MEANSTA)
		pl.colorbar(im)
		ax = pl.axes()
		ax.set_yticklabels([])
		ax.set_xticklabels([])
		#ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
		pl.savefig(finalfolder_log+"/MEANSTA-g_"+str(neurontag)+".png",format='png', bbox_inches='tight')


	# '''minim = np.min(np.min(MEANSTA))
	# if minim < 0:
		# MEANSTA2 = MEANSTA + np.abs(minim) #lineal shift
	# if minim > 0:
		# MEANSTA2 = MEANSTA - np.abs(minim) #lineal shift
	# else:
		# MEANSTA2 = MEANSTA
	# minim2 = np.min(np.min(MEANSTA2))
	# maxim = np.max(np.max(MEANSTA2))
	# print 'minimo ', minim2
	# print 'maximo ', maxim
	# meanvisual = MEANSTA2*255
	# meanvisual = meanvisual // (maxim*1.0)
	# #print meanvisual
	# minim3 = np.min(np.min(meanvisual))
	# maxim3 = np.max(np.max(meanvisual))
	# print 'minimo visual', minim3
	# print 'maximo visual', maxim3

	# pl.figure()
	# #im = pl.imshow(meanvisual,interpolation = 'none')
	# im = pl.pcolor(meanvisual,vmin = 0,vmax = 255, cmap=cm.jet)
	# #pl.gray() 
	# pl.jet()
	# #pl.contour(meanvisual)
	# pl.colorbar(im)
	# ax = pl.axes()
	# ax.set_yticklabels([])
	# ax.set_xticklabels([])
	# #ax.annotate(str(a+1), (.1, 1.2), bbox=dict(boxstyle="round, pad=0.3", fc="w"), size=52 )
	# pl.savefig(finalfolder+"/MEANSTA2-g_"+str(neurontag)+".png",format='png', bbox_inches='tight')'''

	print 'CELL ' + timestampName + ' FINISHED!!!'
	print '-----------------------END---------------------------'
	del STA_desp 
	del STA 
	del stavisual_lin 
	del spikeframe_matrix
	del imagen
	del acumula
	
	



