#!/usr/bin/env python
import numpy as np
import argparse as ap
import scipy.linalg as scil
import scipy.io as scio
import h5py
import matplotlib.pyplot as plt

#parse arguments
parser = ap.ArgumentParser( prog = 'raw-stc.py' , description = 'Computes Raw STC (and STA for prior validation)' , formatter_class = ap.ArgumentDefaultsHelpFormatter )
parser.add_argument( '--stimuli' , help = 'Matlab (v7.3) fixed stimuli matrix file' , type = str , default = 'stim.mat' , required = False )
parser.add_argument( '--staData' , help = 'Matlab (v7-7.2) STA matrix file' , type = str , default = 'sta-E2a.mat' , required = False )
parser.add_argument( '--spikes' , help = 'Text file containing spike times' , type = str , default = 'E2a.txt' , required = False )
parser.add_argument( '--stimTimes' , help = 'Text file with stimuli start/end times' , type = str , default = 'sync.txt' , required = False )
parser.add_argument( '--staFileProp' , help = 'File where to save our sta' , type = str , default = 'sta-prop.npy' , required = False )
parser.add_argument( '--stcFile' , help = 'File where to save stc matrix' , type = str , default = 'stcMatrix.gz' , required = False )
parser.add_argument( '--cmFile' , help = 'File where to save covariance matrix' , type = str , default = 'CovMatrix.gz' , required = False )
parser.add_argument( '--eigenValuesFile' , help = 'File where to save eigenvalues' , type = str , default = 'eigenValues.txt' , required = False )
parser.add_argument( '--eigenVectorsFile' , help = 'File where to save eigenvectors' , type = str , default = 'eigenVectors.txt' , required = False )
parser.add_argument( '--framesAfterSpike' , help = 'Amount of frames after the spike' , type = int , default = '0' , required = False )
args = parser.parse_args()

#read files
aux = scio.loadmat( args.staData )
presta = aux['STA_array'] # (31,31,20)
aux = h5py.File( args.stimuli ,'r')
prestim = aux['stim'] # (108000, 3, 31, 31)
spk = np.loadtxt( args.spikes )
stimTimes = np.loadtxt( args.stimTimes )[:,1] #store ending times only
del aux

#convert h5py data to numpy array
prestim = np.array( prestim )

#convert RGB stimuli to grayscale
gstim = 0.299 * prestim[:,0,:,:] + 0.587 * prestim[:,1,:,:] + 0.144 * prestim[:,2,:,:]
del prestim

#get STA data
lenSTA = presta.shape[2]
xshape = presta.shape[0]
yshape = presta.shape[1]

#containers for data blocks
stim = np.zeros( ( gstim.shape[0] , xshape * yshape ) )
sta = np.zeros( ( lenSTA , xshape * yshape ) )

#generate data blocks: images as columns, concatenating rows. For both stimuli and STA
for i in xrange( gstim.shape[0] ):
	stim[i,:] = np.hstack( gstim[i,:,:] )

del gstim

for i in xrange( lenSTA ):
	sta[i,:] = np.hstack( presta[:,:,i] )

del presta

#adapt spk file values (seconds) to stim file values ("points")
spk *= 2e4

#normalize stimuli: compute its mean and subtract it from each stimulus
aux = np.sum( stim , 0 ) 
aux /= stim.shape[0]
for i in xrange( stim.shape[0] ):
	stim[i,:] -= aux
del aux

#container for stc and covariance matrix
stc = np.zeros( ( stim.shape[1] * lenSTA , stim.shape[1] * lenSTA ) )
cm = np.zeros( stc.shape )

#compute sta to validate
auxsta = np.zeros ( sta.shape )

#sta as a vector
#vecsta = np.hstack( sta )
#convert to matrix (column) to make the computation clearer
#vecsta = np.matrix( vecsta ).T

#for each spike, find the block of stimuli (of lenSTA) that precedes this spike, and compute sta
for i in spk:
	#if spike is over the ending of stimuli's presentation, stop
	if i > stimTimes.max():
		break
	else:
		#if there are not enough frames to capture, don't consider
		if i < stimTimes.min():
			pass
		else:
			frameIndex = np.where( i < stimTimes )[0][0] + 1 + args.framesAfterSpike #more efficient way than np.where()? #gets index of immediate after
			#if there are not enough frames to capture, don't consider
			if frameIndex < lenSTA:
				pass
			else:
				block = stim[frameIndex-lenSTA:frameIndex,:] #no need to add one as we captured index immediately after
				del frameIndex
				#sta to validate
				auxsta += block

#normalize sta
auxsta /= ( 1. * spk.shape[0] )

#sta as a vector
vecsta = np.hstack( auxsta )
#convert to matrix (column) to make the computation clearer
vecsta = np.matrix( vecsta ).T

#for each spike, find the block of stimuli (of lenSTA) that precedes this spike, and compute stc
for i in spk:
	#if spike is over the ending of stimuli's presentation, stop
	if i > stimTimes.max():
		break
	else:
		#if there are not enough frames to capture, don't consider
		if i < stimTimes.min():
			pass
		else:
			frameIndex = np.where( i < stimTimes )[0][0] + 1 + args.framesAfterSpike #more efficient way than np.where()? #gets index of immediate after
			#if there are not enough frames to capture, don't consider
			if frameIndex < lenSTA:
				pass
			else:
				block = stim[frameIndex-lenSTA:frameIndex,:] #no need to add one as we captured index immediately after
				del frameIndex
				#transform block into a vector
				vecblock = np.hstack( block )
				del block
				#convert to matrix (column) to make the computation clearer
				vecblock = np.matrix( vecblock ).T
				#add to stc
				stc += np.dot( (vecblock-vecsta).T , (vecblock-vecsta) )

#compute covariance matrix
for i in xrange( stim.shape[0] ):
	block = stim[i:i+lenSTA]
	#transform block into a vector
	vecblock = np.hstack( block )
	del block
	#convert to matrix (column) to make the computation clearer
	vecblock = np.matrix( vecblock ).T
	#add to the covariance matrix
	cm += np.dot( vecblock.T , vecblock )
	
#normalize stc and covariance matrix
stc /= ( spk.shape[0] - 1. )
cm /= ( stim.shape[0] - 1. )

#save these precious matrices
np.savetxt( args.stcFile , stc )
np.savetxt( args.cmFile , cm )

'''
#compute difference to obtain excitatory and inhibitory eigenvectors
diff = stc - cm
#compute eigenvectors
eigenValues , eigenVectors = scil.eig( diff )
#sort the result from higher to lower eigenvalues
idx = eigenValues.argsort()[::-1]
eigenValues = eigenValues[idx]
eigenVectors = eigenVectors[:,idx]
del idx

#save the eigenStuff
np.savetxt( args.eigenValuesFile , eigenValues )
np.savetxt( args.eigenVectorsFile , eigenVectors )

#plot highest valued eigenvector in a spatio-temporal representation
fig = plt.figure()
for i in xrange( lenSTA ) :
	ax = fig.add_subplot( 1, lenSTA , i )
	#adapt it for imshow
	eigenHighest = eigenVectors[:,0].reshape( ( lenSTA , xshape * yshape ) )
	for j in xrange( stim.shape[0] ):
		eigenHighest[j,:] = eigenHighest[j,:].reshape( ( xshape , yshape ) )
	ax.imshow( eigenHighest[j,:] )

#plot eigenvalues
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot( np.arange( eigenValues.shape[0] ) , eigenValues , 'bo' )
'''

#plot stas
fig = plt.figure()
aux = np.zeros( ( lenSTA , xshape , yshape ) )
ori = np.zeros( ( lenSTA , xshape , yshape ) )
for i in xrange( lenSTA ) :
	ax = fig.add_subplot( 2, lenSTA , i+1 )
	#adapt it for imshow
	aux[i,:,:] = auxsta[i,:].reshape( ( xshape , yshape ) )
	ori[i,:,:] = sta[i,:].reshape( ( xshape , yshape ) )
	#print aux.min() , aux.max(), ori.min() , ori.max()
	#add normal
	ax.set_axis_off()
	ax.imshow( ori[i,:,:] )
	#and ours
	ax = fig.add_subplot( 2, lenSTA , i+lenSTA+1 )
	ax.set_axis_off()
	ax.imshow( aux[i,:,:] )

#TODO: other plots

#store our sta
np.save( args.staFileProp , aux )

#show plots
plt.show()

