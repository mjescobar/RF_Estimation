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
import sys  # system lib
import os  # operative system lib
import random  # Random number methods
import time         # System timer options
import argparse  # A|rgument parsing
from multiprocessing import Pool, freeze_support  # Parallel powa!

import matplotlib  # Graph and plot library
matplotlib.use("Agg")  # For save images without show it in windows (for server use)
import matplotlib.cm as cm        # plot lib
import matplotlib.pyplot as plt       # plot lib (for figures)

#-----------------------------------------------------------
# Methods, Signal processing, etc:
#-----------------------------------------------------------
from scipy.io import loadmat, savemat
import scipy.misc as scim  # Scientific python package for image basic process
import numpy as npy  # Numerical methods lib

#=============================================
# Inputs
#=============================================
parser = argparse.ArgumentParser(
    prog='sta.py',
    description='Performs STA from a stimuli ensemble',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
parser.add_argument(
    '--getimagenames',
    default=0,
    help='0,1 load image name list with the stimulus ensemble',
    type=int,
    choices=[0, 1],
    required=False
    )
parser.add_argument(
    '--openimagesandwrite',
    default=0,
    help='0,1 DO TESTS FOR READ AND WRITE IMAGES',
    type=int,
    choices=[0, 1],
    required=False,
    )
parser.add_argument(
    '--calculatemeanrf',
    default=0,
    help='0,1 LOAD ALL THE IMAGES FROM THE STIMULOS ENSEMBLE \
    AND CALCULATE THE MEAN STIMULUS',
    type=int,
    choices=[0, 1],
    required=False,
    )
parser.add_argument(
    '--algorithm',
    default=4,
    help='1,2,4 How to perform STA, \
    1 load all spike triggered stimuli,\
    2 for sequentially load \
    4 from text',
    type=int,
    choices=[1, 2],
    required=False,
    )
parser.add_argument(
    '--startUnit',
    help='From which units should be processed',
    type=int,
    default=0,
    required=False,
    )
parser.add_argument(
    '--endUnit',
    help='Up to which units should be processed',
    type=int,
    default=2,
    required=False,
    )
parser.add_argument(
    '--outputFolder',
    help='Output folder',
    type=str,
    default='.',
    required=False,
    )
parser.add_argument(
    '--path',
    help='Path to files (DEPRECATED, do not use)',
    type=str,
    default='.',
    required=False,
    )
parser.add_argument(
    '--sourceFolder',
    help='Folder with the files containing the timestamps for each unit',
    type=str,
    default='.',
    required=True,
    )
parser.add_argument(
    '--fileTypeFilter',
    help='Filter for the file containing timestamps',
    type=str,
    default='*.txt',
    )
parser.add_argument(
    '--timefolder',
    help='SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS \
    (DEPRECATED, do not use)',
    type=str,
    default='.',
    required=False,
    )
parser.add_argument(
    '--syncFile',
    help='SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE \
    IT CONTAINS THEINITIAL AND FINAL TIME STAMPS OF EACH FRAME',
    type=str,
    default='.',
    required=True,
    )
parser.add_argument(
    '--samplingRate',
    help='ADQUISITION SAMPLING RATE FOR THE RECORDS',
    type=int,
    default=20000,
    required=False,
    )
parser.add_argument(
    '--framesNumber',
    help='NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALISE',
    type=int,
    default=18,
    required=False,
    )
parser.add_argument(
    '--numberframespost',
    help='number of frames posterior to each spike for STA windows',
    type=int,
    default=2,
    required=False,
    )
parser.add_argument(
    '--xSize',
    help='SIZE OF EACH FRAME IN PIXELS X',
    type=int,
    default=31,
    required=False,
    )
parser.add_argument(
    '--ySize',
    help='SIZE OF EACH FRAME IN PIXELS Y',
    type=int,
    default=31,
    required=False,
    )
parser.add_argument(
    '--dolog',
    help='0,1 logarithm analysis for plot',
    type=int,
    default=0,
    choices=[0, 1],
    required=False,
    )
parser.add_argument(
    '--stimMini',
    help='Stimuli matrix from *.mat or *.hdf5',
    type=str,
    required=True,
    )
parser.add_argument(
    '--characterisation',
    help='Characterisation',
    type=str,
    required=False,
    )
parser.add_argument(
    '--numberProcesses',
    help='Number of processes to spawn',
    type=int,
    default=1,
    choices=[1, 2, 3, 4, 5, 6],
    required=False,
    )
args = parser.parse_args()


# =============================================
# GET SPIKE TIME FILE NAMES
# =============================================

archivosruta = args.path

# Source folder of the files with the timestamps
sourceFolder = args.sourceFolder
# Check for trailing / on the folder
if sourceFolder[-1] != '/':
    sourceFolder+='/'

fileTypeFilter = args.fileTypeFilter.rsplit('.', 1)[1]

# FOLDER NAME TO SAVE RESULTS
outputFolder = args.outputFolder
if outputFolder[-1] != '/':
    outputFolder+='/'

# SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
# IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
syncFile = args.syncFile

getimagenames = args.getimagenames #must be 0
openimagesandwrite = args.openimagesandwrite #must be 0
calculatemeanrf = args.calculatemeanrf #must be 0
tipoalgoritmo = args.algorithm

# SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS
timefolder = sourceFolder

# SET THE ADQUISITION SAMPLING RATE OF THE RECORDS
samplingRate = args.samplingRate # Hz

# SET THE NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALIZE:
# number of frames previous to each spike for STA windows
framesNumber = args.framesNumber
# number of frames posterior to each spike for STA windows
numberframespost = args.numberframespost

# SET THE SIZE OF EACH FRAME IN PIXELS
xSize = args.xSize #31
ySize = args.ySize #31

# set if do logarithm analysis for plot:
dolog = args.dolog

# SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
# IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
if not os.path.isfile(syncFile):
    print 'File [' + syncFile + '] not found'
    sys.exit()
inicio_fin_frame = npy.loadtxt(syncFile)
vector_inicio_frame = inicio_fin_frame[:, 0]
vector_fin_frame = inicio_fin_frame[:, 1]
spikeStart = vector_fin_frame[framesNumber]
lenSyncFile = len(vector_fin_frame)

# load image mat file stim_mini
stimMini = args.stimMini
if stimMini.lower().endswith('.mat'):
    try:
        ensemble = loadmat(stimMini)
        estimulos = ensemble['stim']
    except NotImplementedError:
        import h5py
        with h5py.File(stimMini, 'r') as hf:
            estimulos = hf['stim'][...]
    except ValueError as verror:
        verror('There are problems with {} file'.format(stimMini))
    xSize, ySize, nchannels, lenEstimulos = estimulos.shape
    estim = npy.zeros((xSize, ySize, lenEstimulos))
    for ke in range(lenEstimulos):
        rgb = estimulos[:, :, :, ke]
        gray = npy.dot(rgb[..., :3], [0.299, 0.587, 0.144])
        estim[:, :, ke] = gray
    estim = npy.asarray(estim)
elif stimMini.lower().endswith('.hdf5'):
    import h5py
    with h5py.File(stimMini, 'r') as hf:
        estimulos = hf['checkerboard'][...]
    estimulos = npy.transpose(estimulos, (2, 3, 1, 0))
    xSize, ySize, nchannels, lenEstimulos = estimulos.shape
    estim = npy.zeros((xSize, ySize, lenEstimulos))
    for ke in range(lenEstimulos):
        rgb = estimulos[:, :, :, ke]
        gray = npy.dot(rgb[..., :3], [0.299, 0.587, 0.144])
        estim[:, :, ke] = gray
    estim = npy.asarray(estim)
elif stimMini.lower().endswith('.npy'):
    estim = npy.load(stimMatrix)
else:
    raise ValueError('It necesary load a stim File')

xSize, ySize, lenEstimulos = estim.shape
if lenEstimulos < lenSyncFile:
    lenSyncFile = lenEstimulos


meanimagearray = npy.add.reduce(estim, axis=2) // (1.0*100000)

startUnit = args.startUnit
endUnit = args.endUnit

# Dumb validation about limits
if startUnit < 0:
    print ''
    print 'startUnit can not be lesser than 0'
    sys.exit()

if startUnit > endUnit:
    print ''
    print 'startUnit can not be lesser than endUnit'
    sys.exit()

#vectores units y caracterizacion provienen de la tabla excel
#pero como no la tenemos...la primera vez se deben ignorar
per_row = []
for unitFile in os.listdir(sourceFolder):
    if unitFile.rsplit('.', 1)[1] == fileTypeFilter:
        per_row.append(unitFile.rsplit('.', 1)[0])

recoveredUnits = len(per_row)
if endUnit > recoveredUnits:
    endUnit = recoveredUnits

#If the characterisationFile is not provided an array of length of the
# units must be provided.
characterisationFile = args.characterisation
if not characterisationFile:
    characterization = npy.ones((len(per_row),), dtype=npy.int)
else:
    if not os.path.isfile(characterisationFile):
        print ''
        print 'File [' + characterisationFile + '] not found'
        sys.exit()
    else:
        characterization = npy.loadtxt(characterisationFile)

#Final lesser than Start
if endUnit > len(characterization):
    endUnit=len(characterization)-startUnit

try:
  os.mkdir( outputFolder )
except OSError:
  pass

def sta_1():
    # LOAD ALL THE FRAMES ACCORDING TO THE TIME STAMPS OF THE CELL
    # NOT FUNCTIONAL ANYMORE
    limite3 = len(stimei)
    kframe = 0
    spk = npy.zeros((500,500,framesNumber,limite3))

    for kiter in range(limite3):
        kframe = stimei[kiter]
        for b in range(framesNumber):
            print ' kiter: ',kiter, ' kframe: ',kframe, ' b: ',b
            line = ifn2[kframe-(framesNumber-1)+ b ]
            imagen = scim.imread(line, flatten=True)
            spk[:,:,b,kiter] = imagen - meanimagearray

    N = len(stimei)
    STA = ( npy.add.reduce(spk,axis=3) / (1.0 * N) )
    MEANSTA = ( npy.add.reduce(STA,axis=2) / (1.0 * framesNumber) )

def sta_2():
    # LOAD EACH FRAME AND CALCULATES THE STA SEQUENTIALLY
    timeAlgorithm2Ini = time.time()
    kframe = 0
    cadena_texto = "mean_image"
    contenedor = loadmat(outputFolder+cadena_texto+'.mat')
    meanimagearray = contenedor['meanimagearray']
    del contenedor
    xSize = 380
    ySize = 380
    acumula = npy.zeros((xSize,ySize,framesNumber+numberframespost))
    print 'Get the spike triggered stimuli: \n '
    for kiter in range(limite3):
        timeProcessIni = time.time()
        kframe = stimei[kiter]
        for b in range(framesNumber+numberframespost):
            line = ifn2[kframe-(framesNumber-1)+ b]
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
    minimosta = npy.min(npy.min(npy.min(STA)))
    maximosta = npy.max(npy.max(npy.max(STA)))
    print '\nmin sta ', minimosta, ' max sta ', maximosta
    if minimosta < 0:
        STA_desp = STA + npy.abs(minimosta) # lineal shift
    if minimosta >= 0:
        STA_desp = STA - npy.abs(minimosta) # lineal shift
    minimosta_desp = npy.min(npy.min(npy.min(STA_desp)))
    maximosta_desp = npy.max(npy.max(npy.max(STA_desp)))
    print 'min sta with bias', minimosta_desp
    print 'max sta with bias', maximosta_desp
    stavisual_lin = STA_desp*255 # it is visualized with lineal scale
    stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
    print 'min sta visual lineal', npy.min(npy.min(npy.min(stavisual_lin)))
    print 'max sta visual lineal', npy.min(npy.max(npy.max(stavisual_lin)))
    # FINAL NORMALIZATION FOR THE MEAN STA
    MEANSTA_lin =  npy.add.reduce(stavisual_lin,axis=2)
    timeAlgorithm2End = time.time()
    timeAlgorithm2Total = timeAlgorithm2End - timeAlgorithm2Ini
    print " Time process ", timeAlgorithm2Total, ' seg (', timeAlgorithm2Total/60, ' min)'

def sta_3():
    timeAlgorithm3Ini = time.time()
    print 'Get the spike triggered stimuli: \n '
    sizechunk = 40
    sizesmall = 20
    acumula = npy.zeros((xSize,ySize,framesNumber+numberframespost))
    if dosmall:
        acumulaSmall = npy.zeros((sizesmall,sizesmall,framesNumber+numberframespost))
    for kblock in range(npy.round(limite3/sizechunk)):
        spk = npy.zeros((xSize,ySize,framesNumber+numberframespost,sizechunk))
        if dosmall:
            spkSmall = npy.zeros((sizesmall,sizesmall,framesNumber+numberframespost,sizechunk))
        for kiter in range(sizechunk):
            kframe = stimei[kiter+kblock*sizechunk]
            for b in range(framesNumber+numberframespost):
                line = ifn2[kframe-(framesNumber-1)+ b ]
                imagen = scim.imread(line, flatten = True )
                if dosmall:
                    imagenSmall = scim.imresize(imagen, [sizesmall,sizesmall] , interp = 'bilinear' , mode = None )
                spk[:,:,b,kiter] = imagen
                if dosmall:
                    spkSmall[:,:,b,kiter] = imagenSmall
        del imagen
        del line
        if dosmall:
            del imagenSmall
        acuchunk = ( npy.add.reduce(spk,axis=3) )
        acumula[:,:,:] = acumula[:,:,:] + acuchunk
        if dosmall:
            acuchunkSmall = ( npy.add.reduce(spkSmall,axis=3) )
            acumulaSmall[:,:,:] = acumulaSmall[:,:,:] + acuchunkSmall
        if kblock > npy.round(limite3/sizechunk):
            break
        sys.stdout.write("\r%d%%" % ((kblock+1)*100.0 /(npy.round(limite3/sizechunk)), ) )
        sys.stdout.flush()
    N = limite3
    STA = acumula // N
    for b in range(framesNumber+numberframespost):
        STA[:,:,b] = STA[:,:,b] - meanimagearray
    if dosmall:
        meansmall = scim.imresize(meanimagearray,[sizesmall,sizesmall], interp='bilinear', mode=None)
        STASmall = acumulaSmall // N
        for b in range(framesNumber+numberframespost):
            STASmall[:,:,b] = STASmall[:,:,b] - meansmall
    print ' \n '
    minimosta = npy.min(npy.min(npy.min(STA)))
    maximosta = npy.max(npy.max(npy.max(STA)))
    if minimosta < 0:
        STA_desp = STA + npy.abs(minimosta) # lineal shift
    if minimosta >= 0:
        STA_desp = STA - npy.abs(minimosta) # lineal shift
    minimosta_desp = npy.min(npy.min(npy.min(STA_desp)))
    maximosta_desp = npy.max(npy.max(npy.max(STA_desp)))
    stavisual_lin = STA_desp*255 # it is visualized with lineal scale
    stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
    # FINAL NORMALIZATION FOR THE MEAN STA
    MEANSTA_lin = ( npy.add.reduce(stavisual_lin,axis=2) / (1.0 * (framesNumber+numberframespost) ) )
    if dosmall:
        minstasmall = npy.min(npy.min(npy.min(STASmall)))
        maxstasmall = npy.max(npy.max(npy.max(STASmall)))
        if minstasmall < 0:
            STA_Small_desp = STASmall + npy.abs(minstasmall) # lineal shift
        if minstasmall >= 0:
            STA_Small_desp = STASmall - npy.abs(minstasmall) # lineal shift
        minstasmall_desp = npy.min(npy.min(npy.min(STA_Small_desp)))
        maxstasmall_desp = npy.max(npy.max(npy.max(STA_Small_desp)))
        sta_small_visual_lin = STA_Small_desp * 255 # it is visualized with lineal scale
        sta_small_visual_lin = sta_small_visual_lin // (maxstasmall_desp *1.0) # it is normalized with lineal scale
        # FINAL NORMALIZATION FOR THE MEAN STA
        MEAN_STA_small_lin = ( npy.add.reduce(sta_small_visual_lin,axis=2) / (1.0 * (framesNumber+numberframespost) ) )

    timeAlgorithm3End = time.time()
    timeAlgorithm3Total = timeAlgorithm3End - timeAlgorithm3Ini
    print " Time process ", timeAlgorithm3Total, ' seg (', timeAlgorithm3Total/60, ' min)'

def sta_4(args):
    stimei = args
    timeAlgorithm4Ini = time.time()
    STA = npy.zeros( ( xSize,ySize, framesNumber+numberframespost ) ) # complete sta matrix

    # for numeroframe in range(framesNumber): #for 18 frames
    #     bigsta18 = npy.zeros( ( xSize,ySize ) )
    #     for kiter in range(len(stimei)):
    #         bigsta18[:,:] = bigsta18[:,:] + estim[ :,:,stimei[kiter]-numeroframe ] - meanimagearray
    #     sta18 = bigsta18 / (1.0 * len(stimei) ) # one part of the sta matrix
    #     STA[:,:,framesNumber-1 - numeroframe] = sta18
    for kframe in stimei:
        STA[:,:,:] += estim[ :,:,kframe-framesNumber:kframe+numberframespost]
    for k in range(framesNumber+numberframespost):
        STA[:,:,k] = STA[:,:,k]/float(len(stimei)) - meanimagearray

    # for kframe in range(numberframespost): #for 18 frames
    #     bigsta18 = npy.zeros( ( xSize,ySize ) )
    #     for kiter in range(len(stimei)-numberframespost):
    #         bigsta18[:,:] = bigsta18[:,:] + estim[ :,:,stimei[kiter]+kframe+1] - meanimagearray
    #     sta18 = bigsta18 / (1.0 * len(stimei) ) # one part of the sta matrix
    #     STA[:,:,framesNumber+kframe] = sta18

    minimosta = npy.min(npy.min(npy.min(STA)))
    maximosta = npy.max(npy.max(npy.max(STA)))
    STA_desp = STA - minimosta
    minimosta_desp = npy.min(npy.min(npy.min(STA_desp)))
    maximosta_desp = npy.max(npy.max(npy.max(STA_desp)))
    stavisual_lin = STA_desp * 255 # it is visualized with lineal scale
    stavisual_lin = stavisual_lin // (maximosta_desp *1.0) # it is normalized with lineal scale
    # FINAL NORMALIZATION FOR THE MEAN STA
    MEANSTA_lin = ( npy.add.reduce(stavisual_lin,axis=2) / (1.0 * (framesNumber+numberframespost) ) )
    timeAlgorithm4End = time.time()
    timeAlgorithm4Total = timeAlgorithm4End - timeAlgorithm4Ini
    print " Time process ", timeAlgorithm4Total, ' seg (', timeAlgorithm4Total/60, ' min)'
    #print '\nsize STA: ',len(STA),'x',len(STA[0]),'x',len(STA[0][0])
    return (STA , stavisual_lin, MEANSTA_lin, STA_desp)

def calculaSTA(args):
    start, finish = args
    if finish > endUnit:
        finish = endUnit

    for kunit in range(start,finish):
        timestampName = per_row[kunit]
        if characterization[kunit] > 0:
            print 'Analysing Unit ',timestampName #, ' loop :', c ,' unit n ', c + startUnit
            #--------------------------------------------------------
            # get spike time stamps from file
            #--------------------------------------------------------
            neurontag = timestampName # tag or number of cell
            rastercelulatxtfile = timefolder + timestampName +'.txt'
            timestamps = npy.loadtxt(rastercelulatxtfile) # text file containing time spikes in datapoints
            neuronresultfolder_lin = str(neurontag)+'_lineal'
            try:
              os.mkdir( outputFolder+neuronresultfolder_lin ) # create the folder
            except OSError:
              pass
            finalfolder_lin = outputFolder+neuronresultfolder_lin
            #print 'size time stamps vector: ', len(timestamps) #, 'x',len(timestamps[0])
            #--------------------------------------------------------
            # get time spikes depending of the stimulus start (frame do not start in time=0)
            #--------------------------------------------------------
            #--------------------------------------------------------
            # Conversion of spike times from seconds to POINTS:
            #--------------------------------------------------------

            vector_spikes = timestamps[timestamps>vector_inicio_frame[0]/samplingRate] # without first id zero column (1 COLUMMN)
            vector_spikes = vector_spikes[vector_spikes<vector_fin_frame[-1]/samplingRate]
            vector_spikes = vector_spikes*samplingRate
            nspikes = len(vector_spikes)

            stimei = []  # initialize time spike index depending of image time
            spikeframe_matrix = npy.zeros( (len(vector_spikes), 4) ) # [spike time, frame id, ini time frame, end time frame]
            #--------------------------------------------------------
            # convert stimes (SPIKE TIMES) to frame indexes (image index):
            #--------------------------------------------------------
            primer_frame = framesNumber
            frame_ant = framesNumber
            #print 'Get the spike triggered stimuli indices: \n'
            contator = 0
            contator2 = 0

            for punto_spike in vector_spikes:
                condicion = 1
                for i in range(primer_frame, lenSyncFile- numberframespost):
                    if (vector_inicio_frame[i] < punto_spike) & (punto_spike <= vector_fin_frame[i]):
                        # if the spike time is into a frame time points (start and ends)
                        spikeframe_matrix[contator,0] = punto_spike
                        spikeframe_matrix[contator,1] = i
                        spikeframe_matrix[contator,2] = inicio_fin_frame[i,0]
                        spikeframe_matrix[contator,3] = inicio_fin_frame[i,1]
                        stimei.append(i)
                        frame_ant = i
                        break
                contator += 1
                sys.stdout.write("\r%d%%" %contator2)
                sys.stdout.flush()
                contator2 = contator * 100 // float( nspikes )
                primer_frame = frame_ant

            limite3 = len(stimei)
            print '\nNro de frames: {:d} |'.format(limite3)
            #print 'length frames times vector', lenSyncFile
            #print "length time stamps vector: ", len(timestamps)
            #print "length spike triggered stimuli time i vector: ", len(stimei)
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
            if(tipoalgoritmo == 4 and len(stimei)>0): # LOAD entire matrix stimuli AND CALCULATES THE STA SEQUENTIALLY
                STA , stavisual_lin , MEANSTA_lin, STA_desp = sta_4(stimei)

                # #----------------------------------------------------
                # # save spike time stamp and frame index
                # #----------------------------------------------------
                # spikeframe_matrix_array =  npy.array(spikeframe_matrix)
                # spikeframe_filename = "spikeframe_matrix"+str(neurontag)
                # #print "Save spike frame matrix as mat file: ",spikeframe_filename
                # savemat(finalfolder_lin+'/'+spikeframe_filename+'.mat',mdict={'spikeframe_matrix':spikeframe_matrix_array},oned_as='column')

                #----------------------------------------------------
                # save true STA matrix (NON SCALED for visual plot)
                #----------------------------------------------------
                STA_array = npy.array(STA)
                cadena_texto = "sta_array_"+str(neurontag)
                #print "Saving NON rescaled STA as mat file: ",cadena_texto
                savemat(finalfolder_lin+'/'+cadena_texto+'.mat',mdict={'STA_array':STA_array},oned_as='column')

                #----------------------------------------------------
                # save visual STA matrix ( RE SCALED for visual plot)
                #----------------------------------------------------
                stavisual_lin_array = npy.array(stavisual_lin)
                cadena_texto = "stavisual_lin_array_"+str(neurontag)
                #print "Saving visual STA (lineal) as mat file: ",cadena_texto
                savemat(finalfolder_lin+'/'+cadena_texto+'.mat',mdict={'STAarray_lin':stavisual_lin_array},oned_as='column')

                #print 'Saving images in lineal scale...'

                plt.close('all')
                nrow = (framesNumber+numberframespost)/6+1
                fig = plt.figure(1, figsize=(6,nrow))
                for ksubplot in range(framesNumber+numberframespost):
                    ax = fig.add_subplot(nrow,6,ksubplot+1)
                    ax.pcolormesh( stavisual_lin[:,:,ksubplot],vmin = 0,vmax = 255, cmap=cm.plasma )
                    ax.set_xlim([0, xSize])
                    ax.set_ylim([0, ySize])
                    ax.set_aspect(1)
                    ax.axis('off')

                plt.savefig(finalfolder_lin+"/STA-"+str(neurontag)+"_.png",format='png', bbox_inches='tight', dpi=300)
                plt.savefig(outputFolder+"STA-"+str(neurontag)+"_.png",format='png', bbox_inches='tight',dpi=300)
                plt.show()
                plt.clf()
                plt.close()
                #------------------------------------------------------

                #print 'Saving mean image in lineal scale...'
                plt.figure()
                im = plt.pcolormesh(MEANSTA_lin,vmin = 0,vmax = 255, cmap=cm.plasma)
                plt.colorbar(im)
                plt.savefig(finalfolder_lin+"/MEANSTA-g_"+str(neurontag)+".png",format='png', bbox_inches='tight')
                plt.close()
                print '\n CELL ' + timestampName + ' FINISHED!!!'

                del STA_desp
                del STA
                del stavisual_lin
                del spikeframe_matrix



def main():
    length = endUnit-startUnit
    np = args.numberProcesses
    p = Pool(processes=np)
    p.map(calculaSTA, [(startPosition,startPosition+length//np) for startPosition in  range(startUnit, length, length//np)])

if __name__=="__main__":
    freeze_support()
    main()
