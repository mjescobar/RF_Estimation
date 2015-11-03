#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

on=np.loadtxt('/home/monica/Dropbox/Cesar/on_area.txt')
dsi_on=np.loadtxt('/home/monica/Dropbox/Cesar/dsi_on.txt')
off=np.loadtxt('/home/monica/Dropbox/Cesar/off_area.txt')
dsi_off=np.loadtxt('/home/monica/Dropbox/Cesar/dsi_off.txt')
dsi_on_off=np.loadtxt('/home/monica/Dropbox/Cesar/dsi_on_off.txt')
on_off=np.loadtxt('/home/monica/Dropbox/Cesar/on_off_area.txt')


xtic=[1,2,3]
plt.scatter(on,dsi_on, s=50,color='g')
plt.scatter(off,dsi_off,s=50,color='b')
plt.scatter(on_off,dsi_on_off,s=50,color='r')
#plt.scatter(on,dsi_on,s=50,color='b', alpha=0.5)
#plt.scatter(on_off,dsi_on_off,s=50,color='r', alpha=0.5)
#plt.scatter(off,dsi_off,s=50,color='#000000', alpha=0.5)
#plt.xticks(xtic,xlab)
plt.xlim(-0.5, 180000)
plt.ylim(0,1.1)
plt.legend(loc="upper left") 
plt.legend('on_cells', 'off_cells','on_off_cells')
plt.show()
