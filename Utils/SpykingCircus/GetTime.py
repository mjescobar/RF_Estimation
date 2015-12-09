import numpy as np, h5py 
import os
pathFile = '/media/experiments/2015-10-15_retina1_periferia_SpykingCircus/2015-10-15_ret1_periferia/'
filename = pathFile.split('/')[-2]+'.spiketimes.mat'
outputFolder = pathFile+'TS/'
sample = 20000
mintime = 40

try:
  os.mkdir( outputFolder ) 
except OSError:
  pass

f = h5py.File(pathFile+filename,'r') 

for key in f.keys():
	data = f.get(key)
	data = np.array(data)/sample
	if len(data) > mintime:
		np.savetxt(outputFolder+key+'.txt',data)



