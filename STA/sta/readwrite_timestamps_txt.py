#============================================================
# READ WRITE TIME STAMPS OF SPIKES
# AASTUDILLO 2013
#============================================================
import numpy as np 	      # numerical methods lib
import sys    # system lib
import os     # operative system lib
import glob # package for get filenames from files in a folder
# getimagenames = int(sys.argv[1]) #0
print '---------------------BEGIN---------------------------'

tsfolder = 'TS_datos0001/'

try:
  os.mkdir( tsfolder ) # if folder "STA" don't exist, create the folder
except OSError:
  pass

filetimestamps = 'datos0001_timestamps2_02_03.txt'  

f = open( filetimestamps ,'r')
per_row = []
for line in f:
    per_row.append(line.split('\t'))
per_column = zip(*per_row)
print 'len(per_row) ', len(per_row) ,'x', len(per_row[0]) 

for k in range(len(per_row[0])):
	columna1 = per_column[k]
	unit1 = columna1[0]
	print unit1 ,' spikes ', len(columna1)-1
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
	fileoutname = tsfolder+''+unit1+'.txt'
	f2 = open( fileoutname ,'w')
	for linea in col:
		fila = linea + '\n'
		f2.writelines(fila)
	f2.close()
f.close()

# limite = 4
# contador = 0
# # line1 = f.xreadlines()
# # print line1
# for line in f.xreadlines():
   # print line
   # if contador == 0:
      # line1 = line
   # contador = contador + 1
   # if contador == limite:
      # break
# f.close()
# print line1
# print len( line1 )

# v = []
# contador = 0
# k = 0
# for columns in ( raw.strip().split() for raw in f ):  
	# #print columns[0]
	# nombre = columns[0].split()
	# for n in nombre:
		# v.append(n)
		# contador = contador + 1
	# k = k + 1
	# print v[0]
	# numeros = np.array( v[1:len(v)] , 'float64')
	# h = tsfolder+''+v[0]+'.txt'
	# print numeros[0:5]
	# np.savetxt( h, numeros )
	# contador = 0
# f.close()

# for columns in ( raw.strip().split() for raw in f ):  
	# print columns[0]
# f.close()

# rows = (row.strip().split() for row in f)
# zip(*rows)
# print zip(*rows)
# f.close()

print '-----------------------END---------------------------'

# def is_float_try(str):
    # try:
        # float(str)
        # return True
    # except ValueError:
        # return False