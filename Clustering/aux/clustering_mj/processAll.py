#!/usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.io
import scipy
import sys

inmat = scipy.io.loadmat('temp_curves_150_50.mat')

tempCurves = inmat['tc']
tempCurvesSpl = inmat['tci']
idx = inmat['idx']
xc = inmat['xc']

print "Shape of tempCurves: ", np.shape(tempCurves)
print "Shape of tempCurvesSpl: ", np.shape(tempCurvesSpl)
print "Shape of idx: ", np.shape(idx)

ntime, ncells = np.shape(tempCurves)
ntimeSpl, ncells = np.shape(tempCurvesSpl)
print "nTime: ", ntime, " - nCells: ", ncells
nclusters = np.max(idx)
print "Number of clusters: ", nclusters
cluster_colors = ['blue', 'red', 'green', 'orange', 'black']

meanCurves = np.zeros( (nclusters,ntimeSpl) )
meanCount = np.zeros( (nclusters,1) )

# Computing mean values
for i in range(ncells):
    if( idx[i] == 1 ):
        meanCurves[0,:] += tempCurvesSpl[:,i]
        meanCount[0] += 1
    if( idx[i] == 2 ):
        meanCurves[1,:] += tempCurvesSpl[:,i]
        meanCount[1] += 1
    if( idx[i] == 3 ):
        meanCurves[2,:] += tempCurvesSpl[:,i]
        meanCount[2] += 1
    if( idx[i] == 4 ):
        meanCurves[3,:] += tempCurvesSpl[:,i]
        meanCount[3] += 1
    if( idx[i] == 5 ):
        meanCurves[4,:] += tempCurvesSpl[:,i]
        meanCount[4] += 1

print meanCount[0], "-", cluster_colors[0]
print meanCount[1], "-", cluster_colors[1]
print meanCount[2], "-", cluster_colors[2]
print meanCount[3], "-", cluster_colors[3]
print meanCount[4], "-", cluster_colors[4]


for i in range(nclusters):
    meanCurves[i,:] /= meanCount[i]

# Plotting figures

plt.figure()
for i in range(ncells):   
    plt.plot(tempCurves[:,i], cluster_colors[idx[i]-1], alpha=0.2)
plt.grid(True)

plt.figure()
for i in range(ncells):   
    plt.plot(xc, tempCurvesSpl[:,i], cluster_colors[idx[i]-1], linewidth=0.5, alpha=0.15)
for i in range(nclusters):
    plt.plot(xc, meanCurves[i,:], cluster_colors[i], linewidth=4, label= "n = %d cells" % meanCount[i])
plt.grid(True)
plt.xlabel('Time before spike [ms]')
plt.ylim(-0.4,0.4)
plt.legend(loc=2)
plt.savefig('Clusters_50uM-150uM.pdf', format='pdf', bbox_inches='tight')


plt.show()


