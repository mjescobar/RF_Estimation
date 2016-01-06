import numpy as np, h5py 
import argparse 							#argument parsing
import os


parser = argparse.ArgumentParser(prog='GetTime_spykingcircus.py',description='Get spiketimes from preocesed in SpyKingCircus',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--spiketimesFile',help='fresult hdf5 file generated from SpyKingCircus',type=str, required=True)
parser.add_argument('--outputFolder',help='Output folder',type=str, required=True)
	 
args = parser.parse_args()

filename = args.spiketimesFile
outputFolder = args.outputFolder
sample = 20000
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
	data = np.array(data)/sample
	if len(data) > mintime:
		np.savetxt(outputFolder+key+'.txt',data)
