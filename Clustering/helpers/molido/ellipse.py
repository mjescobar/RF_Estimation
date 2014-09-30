#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ellipse.py
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
#  

from pylab import figure, show, rand
from matplotlib.patches import Ellipse

def main():
	
	NUM = 250

	ells = [Ellipse(xy=rand(2)*10, width=rand(), height=rand(), angle=rand()*360) for i in range(NUM)]

	fig = figure()
	ax = fig.add_subplot(111, aspect='equal')
	for e in ells:
		ax.add_artist(e)
		e.set_clip_box(ax.bbox)
		e.set_alpha(rand())
		e.set_facecolor(rand(3))

	ax.set_xlim(0, 10)
	ax.set_ylim(0, 10)

	show()

	return 0

if __name__ == '__main__':
	main()

