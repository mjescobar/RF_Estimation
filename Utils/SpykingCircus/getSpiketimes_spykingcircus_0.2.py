import numpy as np, h5py 
import argparse 							#argument parsing
import os


parser = argparse.ArgumentParser(prog='GetTime_spykingcircus.py',description='Get spiketimes from preocesed in SpyKingCircus',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--spiketimesFile',help='fresult hdf5 file generated from SpyKingCircus',type=str, required=True)
parser.add_argument('--offset',help='time of spontaneous activity ',  default=0, type=float, required=False)
parser.add_argument('--outputFolder',help='Output folder',type=str, required=True)
	 
args = parser.parse_args()

filename = args.spiketimesFile
outputFolder = args.outputFolder
offset = args.offset
sample = 20000.0
mintime = 40

if outputFolder[-1] != '/':
	outputFolder = outputFolder + '/'
try:
  os.mkdir( outputFolder ) 
except OSError:
  pass

hfile = h5py.File(filename,'r') 
f = hfile.get("spiketimes")
for key in f.keys():
	data = f.get(key)
	data2 = np.array(data)/sample + offset
	if len(data) < mintime:
		if data2.size > mintime:
			data2 = np.transpose(data2)
		else:
			print key+': No superera el minimo de '+str(mintime)+' timestamp'
	np.savetxt(outputFolder+key+'.txt',data2)
