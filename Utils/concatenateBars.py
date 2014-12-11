import numpy as np
import os
import shutil


inputFile = 'bars.list'
fblank = 'blank_400x400.jpg'
fred_255 = 'red_255_400x400.jpg'
fred_128 = 'red_128_400x400.jpg'


print "> Copying first list..."
f=open (inputFile,'r')
k=0
sourceFolder='/home/monica/Documentos/Estimulos/StraightBar/'
for line in f :
	print line
	tmptxt='StraightBarSeparated/bar00%06d.jpg' % k
	shutil.copy(fred_255,tmptxt)
	k+=1
	nimagPerDir=0
	line=line[:-1]
	directory=sourceFolder+ line
	
	for image in os.listdir(directory) :  
		nimagPerDir+=1
		path=sourceFolder+line+'/'+ image
		tmptxt='StraightBarSeparated/bar00%06d.jpg' % k
		shutil.copy(path,tmptxt)
		k+=1  
            
	tmptxt='StraightBarSeparated/bar00%06d.jpg' % k
	shutil.copy(fred_128, tmptxt)
	k+=1
	nimag=0
	
	while (nimag < nimagPerDir):
		tmptxt = 'StraightBarSeparated/bar00%06d.jpg' % k
		shutil.copy (fblank, tmptxt)
		k+=1
		nimag+=1
    

print "> DONE!!"

