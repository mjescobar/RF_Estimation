 
"""
File	bootstrap.py
Author  Ernesto P. Adorio, PhD.
		UPDEPP(U.P. at Clarkfield)
Version 0.0.1 Sep. 25, 2010 # basic
		0.0.2 Oct   9, 2011 # with bias output, smoothing(sigma >0)
				 Feb 12, 2013 # fixed two bugs discovered by Steve Whitehead.
"""
import random
import scipy.stats as stat
import quantile #http://adorio-research.org/wordpress/?p=125
 
def mean(X):
	return sum(X)/ float(len(X))
 
def bootstrap(sample, samplesize = None, nsamples = 1000, statfunc = mean, sigma= None, conf = 0.95):
	"""
	Arguments:
	   sample - input sample of values
	   nsamples - number of samples to generate
	   samplesize - sample size of each generated sample
	   statfunc- statistical function to apply to each generated sample.
	   sigma - if not None, resmple valuew will have an added normal component
			   with zero mean and sd sigma.
 
	Returns bootstrap sample of statistic(computed by statfunc), bias and confidence interal.
	"""
	if samplesize is None:
		samplesize=len(sample)
	#print "input sample = ",  sample
	n = len(sample)
	X = []
	for i in range(nsamples):
		#print "i = ",  i,
		resample = [random.choice(sample) for j in range(n)] # changed i to j.
		# resample = [sample[j] for j in stat.randint.rvs(0, n-1,\
		#	size=samplesize)]  # older version.
		if sigma and sigma > 0:  # apply smoothing?
		   nnormals = scipy.normal.rvs(n, 0, sigma)
		   resample = [x + z for x,z in zip (resample, nnormals)]
		x = statfunc(resample)
		X.append(x)
	bias = sum(X)/float(nsamples) - statfunc(sample)
 
	plower  = (1-conf)/2.0
	pupper  = 1 -plower
	symconf = (quantile.quantile(X, plower), quantile.quantile(X, pupper)) # corrected.
	return X, bias,symconf
