import numpy as np, h5py 
import argparse 							#argument parsing
import os


parser = argparse.ArgumentParser(prog='GetTime_spykingcircus.py',description='Get spiketimes  preocesed in SpyKingCircus',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--spiketimesFile',help='file name without .extension.hdf5, generated by SpyKingCircus',type=str, required=True)
parser.add_argument('--number',help='number of merge ',  default='', type=str, required=False)
parser.add_argument('--offset',help='time of spontaneous activity ',  default=0, type=float, required=False)
parser.add_argument('--outputFolder',help='Output folder',type=str, required=True)
	 
args = parser.parse_args()

filename = args.spiketimesFile+'.result'+args.number+'.hdf5'
clustername = args.spiketimesFile+'.clusters'+args.number+'.hdf5'
outputFolder = args.outputFolder

offset = args.offset
sample = 20000.0
mintime = 20
i = 0
if outputFolder[-1] != '/':
	outputFolder = outputFolder + '/'
try:
  os.mkdir( outputFolder ) 
except OSError:
  pass

hfile = h5py.File(filename,'r') 
clusterfile = h5py.File(clustername,'r') 
f = hfile.get("spiketimes")
cluster = clusterfile.get("electrodes")
for key  in f.keys():
	data = f.get(key)
	data2 = np.array(data)/sample + offset
	if len(data) < mintime:
		if data2.size > mintime:
			data2 = np.transpose(data2)
		else:
			print key+': No superera el minimo de '+str(mintime)+' timestamp, dimension'+str(data2.shape)
	np.savetxt(outputFolder+key+'_'+str(int(cluster[0][i]))+'.txt',data2)
	i += 1
