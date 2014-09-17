#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pca.py
#  
#  Copyright 2014 Carlos "casep" Sepulveda <casep@fedoraproject.org>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Perform PCA using the sklearn library
#  http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

import numpy as np
from sklearn.decomposition import PCA

def main():	
	
	X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
	
	print X
	
	pca = PCA(n_components=4, copy=False)
	newX = pca.fit(X)
	
	print newX
	
	print X
	
	print pca.components_
	
	print pca.explained_variance_
	return 0

if __name__ == '__main__':
	main()
