#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gap.py
# (c) 2013 Mikael Vejdemo-Johansson
# BSD License
#
# SciPy function to compute the gap statistic for evaluating k-means clustering.
# Gap statistic defined in
# Tibshirani, Walther, Hastie:
#  Estimating the number of clusters in a data set via the gap statistic
#  J. R. Statist. Soc. B (2001) 63, Part 2, pp 411-423

import scipy
import scipy.cluster.vq
import scipy.spatial.distance
dst = scipy.spatial.distance.euclidean
import random
import numpy as np
import matplotlib.pyplot as plt
#Relative path for RFE LIB
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..','LIB'))
import rfestimationLib as rfe				#Some custom functions
import densityPeaks as dp
from sklearn.cluster import KMeans

clustersColours = ['green', 'red', 'blue', 'yellow', 'black','indigo', \
'#ff006f','#00e8ff','#fcfa00', '#ff0000', '#820c2c', \
'#ff006f', '#af00ff','#0200ff','#008dff','#00e8ff', \
'#0c820e','#28ea04','#ea8404','#c8628f','#6283ff', \
'#5b6756','#0c8248','k','#820cff','#932c11', \
'#002c11','#829ca7']

def gap(data, refs=None, nrefs=400, ks=range(1,11)):
	"""
	Compute the Gap statistic for an nxm dataset in data.
	Either give a precomputed set of reference distributions in refs as an (n,m,k) scipy array,
	or state the number k of reference distributions in nrefs for automatic generation with a
	uniformed distribution within the bounding box of data.
	Give the list of k-values for which you want to compute the statistic in ks.
	"""
	shape = data.shape
	if refs==None:
		tops = data.max(axis=0)
		bots = data.min(axis=0)
		dists = scipy.matrix(scipy.diag(tops-bots))
		rands = scipy.random.random_sample(size=(shape[0],shape[1],nrefs))
		for i in range(nrefs):
			rands[:,:,i] = rands[:,:,i]*dists+bots
	else:
		rands = refs
		
	gaps = scipy.zeros((len(ks),))
	for (i,k) in enumerate(ks):
		#(kmc,kml) = scipy.cluster.vq.kmeans2(data, k)
		km = KMeans(init='k-means++', n_clusters=k, n_init=10,n_jobs=-1)
		km.fit(data)
		kml = km.labels_
		kmc = km.cluster_centers_ 
		disp = sum([dst(data[m,:],kmc[kml[m],:]) for m in range(shape[0])])
		refdisps = scipy.zeros((rands.shape[2],))
		for j in range(rands.shape[2]):
			#(kmc,kml) = scipy.cluster.vq.kmeans2(rands[:,:,j], k)
			km = KMeans(init='k-means++', n_clusters=k, n_init=10,n_jobs=-1)
			km.fit(data)
			kml = km.labels_
			kmc = km.cluster_centers_ 
			refdisps[j] = sum([dst(rands[m,:,j],kmc[kml[m],:]) for m in range(shape[0])])
		gaps[i] = scipy.log(scipy.mean(refdisps))-scipy.log(disp)
	return gaps

N=200
X=np.ones((N,2))
for i in(range(0,200)):
	for j in(range(2)):
		X[i][j]=1000*random.uniform(0.05,0.15)


for i in(range(50,99)):
	for j in(range(2)):
		X[i][j]=1000*random.uniform(0.35,0.45)

for i in range(100,149):
	for j in(range(2)):
		X[i][j]=1000*random.uniform(0.55,0.65)


for i in range(150,199):
	for j in(range(2)):
		X[i][j]=1000*random.uniform(0.85,0.95)


plt.scatter(X[:,0],X[:,1])
plt.show()

gaps=gap(X, refs=None, nrefs=200, ks=range(1,10))

dgaps=np.zeros(len(gaps))
for i in range(len(gaps)-1):
	dgaps[i]=gaps[i]-gaps[i+1]


plt.plot(gaps)
plt.show()

plt.plot(dgaps)
plt.show()

clustersNumber, labels = dp.predict(X, 3)
print 'dp.clustersNumber',clustersNumber

for clusterId in range(clustersNumber):
	for data in range(len(X)):
		if labels[data]==clusterId:
			plt.plot(X[data,0],X[data,1],color=clustersColours[clusterId],marker='o')
plt.show()

clustersNumber=2
from sklearn import mixture
gmix = mixture.GMM(n_components=clustersNumber, covariance_type='spherical')
gmix.fit(X)
labels = gmix.predict(X)

for clusterId in range(clustersNumber):
	for data in range(len(X)):
		if labels[data]==clusterId:
			plt.plot(X[data,0],X[data,1],color=clustersColours[clusterId],marker='o')
plt.show()
