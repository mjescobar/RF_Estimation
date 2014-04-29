#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prueba_carga.py
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
#  

import neuroshare as ns
import numpy as np
import matplotlib.pyplot as plt

##  Script de prueba par carga de datos desde .mcd
#   Carga y grafica datos
#

##  nsMCDLibrary.so debe estar en alguna de las siguientes paths
#   ~/.neuroshare
#   /usr/lib/neuroshare
#   /usr/local/lib/neuroshare
#   la biblioteca se encuentra en el repo /RF_Estimation/Clustering/lib

fd = ns.File('/var/tmp/datos0003.mcd')
analog = 2
data = dict()
font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
for i, entity in enumerate(fd.entities):
    if entity.entity_type == analog:
		data1,time,count = entity.get_data()
		channelName = entity.label[0:4]+entity.label[23:]
		datos = np.array(data1)
		largo_datos = len(datos)
		data[channelName] = datos
		print channelName
		print len(datos)
		x = np.linspace(1, largo_datos, largo_datos)
		fig = plt.figure()
		plt.title('Voltages/spikes', fontdict=font)
		plt.xlabel('tiempo', fontdict=font)
		plt.ylabel('voltage (uV)', fontdict=font)
		plt.xlim([-1, largo_datos+1])
		plt.ylim([-0.001, 0.001])
		plt.subplots_adjust(left=0.15)
		plt.plot(x, datos)
		#plt.show()
		fig.savefig(channelName+'.png', dpi=fig.dpi)

