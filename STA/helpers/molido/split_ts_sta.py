#============================================================
# SPLIT TIME STAMPS FILE
# Split the time stamps txt file that contains the spike 
# time stamps of all units.
#
# INPUTS
# TS_FOLDER: the output folder for save each spike
# time stamp file.
# TS_FILE: the original time stamp file resulting from the
# spike sorting stage. This file should be a txt file where
# each column is a unit with its time stamps and the 
# separator are tabs.
#
# USAGE:
# >python split_ts_sta.py --ts_folder TS_1 --ts_file /sta_05/datos0044_timestamps_24_02.txt
#
# AASTUDILLO 2013
#============================================================
import numpy as np 	      # numerical methods lib
import sys    # system lib
import os     # operative system lib
import glob # package for get filenames from files in a folder
import argparse #argument parsing

print '---------------------BEGIN---------------------------'

# --------------------------------
# Inputs
parser = argparse.ArgumentParser(prog='split_ts_sta.py',
 description='Split the spike time stamps txt file to individual unit files',
 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--ts_folder',
 help='Time stamps individual files output folder',
 type=str, default='TS_datos0001', required=True)
 
parser.add_argument('--ts_file',
 help='Spike time stamp file (complete path) (txt)',
 type=str, default='datos0001_timestamps_CTRL50_2.txt', required=True)
args = parser.parse_args()


#tsfolder = sys.argv[1]# 'TS_datos0001/'
tsfolder = args.ts_folder
# tsfolder = 'TS_datos0001/'

#filetimestamps = sys.argv[2]
filetimestamps = args.ts_file
#filetimestamps = 'datos0001_timestamps_CTRL50_2.txt'

# --------------------------------
try:
  os.mkdir( tsfolder ) # if folder "STA" don't exist, create the folder
except OSError:
  pass

f = open( filetimestamps ,'r')
per_row = []
for line in f:
    per_row.append(line.split('\t'))
per_column = zip(*per_row)
print 'Total Length of a Row', len(per_row) ,'x', len(per_row[0]) 

for k in range(len(per_row[0])-2): # -2 to ignore the AllFile Column (end of the row in the txt files)
	columna1 = per_column[k]
	unit1 = columna1[0]
	#print unit1 ,' spikes ', len(columna1)-1
	p = 0
	for elemento in columna1:
		try:
			float(elemento)
			g= True
		except ValueError:
			g= False
		if g:
			p = p + 1
	print unit1 ,' spikes ', p
	col = columna1[1:p] #columna1[1:len(columna1)]
	fileoutname = tsfolder+'/'+unit1+'.txt'
	f2 = open( fileoutname ,'w')
	for linea in col:
		fila = linea + '\n'
		f2.writelines(fila)
	f2.close()
f.close()

print '-----------------------END---------------------------'

