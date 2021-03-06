#============================================================
# SPIKE TRIGGERED AVERAGE (STA) ALGORITHM IN CHAIN
# Do STA for a list of Unit Cells.
# AASTUDILLO 2014
#============================================================

#============================================================
# Package import section:
#============================================================
# import matplotlib     # Graph and plot library
# matplotlib.use("Agg") # for save images without show it in windows (for server use)
# import pylab as pl
# import matplotlib.cm as cm      	  # plot lib
# import matplotlib.pyplot as plt 	  # plot lib (for figures)
# import mpl_toolkits.mplot3d.axes3d as p3d # 3D Plot lib
# from matplotlib.pyplot import *  	    # plot lib python
# from matplotlib.ticker import NullFormatter # ticker formatter
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
import time 	# System timer options
#import scipy.misc as scim # scientific python package for image basic process
import glob # package for get file names from files in a folder
# import matplotlib.pyplot as plt
#from pylab import * 	# laboratory and plot methods lib 
#from scipy import misc
#from PIL import Image, ImageChops

from sta_functions import *

import gc # garbage collector

#=============================================
# GET SPIKE TIME FILE NAMES
#=============================================

archivosruta = 'D:/Experimentos_CINV/datos_20-11-2013_bga50um_2/'
#
archivosfolder = 'TS_datos0003/'
archivofiltro = '*.txt'

globstring     =  archivosruta + archivosfolder +'/'+ archivofiltro
archivofilenames = glob.glob(globstring) # get file names from folder
archivofilenames.sort()

print "\t length filenames: ", len(archivofilenames)
print "\t last filenames : ",archivofilenames[len(archivofilenames)-2]

getimagenames = 0
openimagesandwrite = 0
calculatemeanrf = 0 
tipoalgoritmo = 2

# =============================================
# SET OTHERS OPTIONS
# =============================================

# FOLDER NAME TO SAVE EACH FOLDER RESULTS
stafolder = 'STA_datos0003'

# FOLDER NAME TO LOAD STIMULUS ENSEMBLE: IMAGE STIMULUS FOLDER
imageruta = 'D:/'
imagefolder = 'checkImages'
imagefiltro = '*.png'

# SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS
timefolder = archivosfolder #'TS_datos0003_2/'

# SET THE ADQUISITION SAMPLING RATE OF THE RECORDS
samplingRate = 20000 # Hz

# SET THE NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALIZE:
# number of frames previous to each spike for STA windows
numberframes = 13 
# number of frames posterior to each spike for STA windows
numberframespost = 5 

# SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
# IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
synchronyfile = 'inicio_fin_frame_datos0003.txt'
#inicio_fin_frame = np.loadtxt(synchronyfile)

# SET THE SIZE OF EACH FRAME IN PIXELS
sizex = 380 #500 #750
sizey = 380 #500 #700

# set if do logarithm analysis for plot:
dolog = 0

#timestampName = archivofilenames[118]
c = 1
inicio = 536+10+10+10+10+10+10+10+10+10+10+10+10+10+10
final  = inicio + 10

for unitname in archivofilenames[inicio:final]:
	timestampName1 = os.path.basename(unitname)

	timestampName = os.path.splitext(timestampName1)[0]

	print 'Analyzing Unit ',timestampName, ' loop :', c ,' unit n ', c + inicio
	sta_each( getimagenames,openimagesandwrite,calculatemeanrf,tipoalgoritmo,timestampName ,stafolder ,imageruta ,imagefolder ,imagefiltro ,timefolder ,samplingRate ,numberframes ,numberframespost , synchronyfile ,sizex ,sizey, dolog)
	
	c = c +1
	gc.collect()

