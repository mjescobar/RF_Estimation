import numpy as np
import os
import shutil


inputFile = '/home/monica/Documentos/Estimulos/bars.list'
fblank = '/home/monica/Documentos/Estimulos/blank_400x400.jpg'
fred_255 = '/home/monica/Documentos/Estimulos/red_255_400x400.jpg'
fred_128 = '/home/monica/Documentos/Estimulos/red_128_400x400.jpg'


print "> Copying first list..."
f=open (inputFile,'r')
k=0
sourceFolder='/home/monica/Documentos/Estimulos/StraightBar/'
for line in f:
	tmptxt='/home/monica/Documentos/Estimulos/StraightBarSeparated/bar00%06d.jpg' % k
	shutil.copy(fred_255,tmptxt)
	k+=1
	nimagPerDir=0
	line=line[:-1]
	directory=sourceFolder+ line
	
	for image in sorted(os.listdir(directory)) :  
		print image
		nimagPerDir+=1
		path=sourceFolder+line+'/'+ image
		tmptxt='/home/monica/Documentos/Estimulos/StraightBarSeparated/bar00%06d.jpg' % k
		shutil.copy(path,tmptxt)
		k+=1  
            
	tmptxt='/home/monica/Documentos/Estimulos/StraightBarSeparated/bar00%06d.jpg' % k
	shutil.copy(fred_128, tmptxt)
	k+=1
	nimag=0
	
	while (nimag < nimagPerDir):
		tmptxt = '/home/monica/Documentos/Estimulos/StraightBarSeparated/bar00%06d.jpg' % k
		shutil.copy (fblank, tmptxt)
		k+=1
		nimag+=1
    

print "> DONE!!"

