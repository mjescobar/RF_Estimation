#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gaussFit.py
#  
#  Copyright 2014 Carlos "casep" Sepulveda <casep@alumnos.inf.utfsm.cl>
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
#   FMGAUSSFIT Create/alter optimization OPTIONS structure.
#   [fitresult,..., rr] = fmgaussfit(xx,yy,zz) uses ZZ for the surface 
#   height. XX and YY are vectors or matrices defining the x and y 
#   components of a surface. If XX and YY are vectors, length(XX) = n and 
#   length(YY) = m, where [m,n] = size(Z). In this case, the vertices of the
#   surface faces are (XX(j), YY(i), ZZ(i,j)) triples. To create XX and YY 
#   matrices for arbitrary domains, use the meshgrid function. FMGAUSSFIT
#   uses the lsqcurvefit tool, and the OPTIMZATION TOOLBOX. The initial
#   guess for the gaussian is places at the maxima in the ZZ plane. The fit
#   is restricted to be in the span of XX and YY.
#   See:
#       http://en.wikipedia.org/wiki/Gaussian_function
#
# Traduccion a Python del codigo de Nathan Orloff.

import numpy as np			#python utilities

def prepareSurfaceData(matrizSTA):
	# prepare surface data using meshgrid
	# matrizSTA = double(matrizSTA)
	vec1 = []
	vec2 = []
	vec3 = []
	[n_filas,n_columnas] = matrizSTA.shape
	
	[Xpixel2D,Ypixel2D] = np.meshgrid(np.linspace(0,n_columnas-1,n_columnas),np.linspace(0,n_filas-1,n_filas))

	for y in range (n_filas):
		for x in range (n_columnas):
			Xpixels = np.append(vec1,Xpixel2D[y,x])
			Ypixels = np.append(vec2,Ypixel2D[y,x])
			valores = np.append(vec3,matrizSTA[y,x])
			vec1 = Xpixels
			vec2 = Ypixels
			vec3 = valores

	Xpixels = np.array(Xpixels).transpose()
	Ypixels = np.array(Ypixels).transpose()
	valores = np.array(valores).transpose()

	return Xpixels, Ypixels, valores, Xpixel2D, Ypixel2D
