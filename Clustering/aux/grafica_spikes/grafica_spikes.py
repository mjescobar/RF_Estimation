#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  grafica_spikes.py
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

import numpy as np
import matplotlib.pyplot as plt

##  @package grafica_spikes
#   Script de prueba para graficado spikes timestamps sin procesamiento
#   Utiliza los datos generados por procesos STA
#   Busca representar ubicación de spikes en el tiempo
#   

##  @var font
#   Utilizada para estilo de texto en grafica
font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

##  @var spikes
#   Aca se almacena valores cargados desde archivo        
spikes = []
##  @var f
#   Archivo que contiene timestamps de los spikes
f = open('../clustering_mj/TS_datos0003_2/A2a.txt', 'r')
for line in f:
	spikes.append(float(line))
f.close()

##  @var largo_datos
#   auxiliar para largo de datos obtenidos
largo_datos = len(spikes)
##  @var y
#   Arreglo de '1' para utilizar como coordenada de grafica
y = []
y = y + [1]*(largo_datos - len(y))

plt.title('Spikes en el tiempo', fontdict=font)
plt.xlabel('tiempo', fontdict=font)
plt.ylabel('eventos', fontdict=font)
#plt.xlim([spikes[0], spikes[-1]])
plt.xlim(0,2000)
plt.ylim([0, 2])
plt.subplots_adjust(left=0.15)
plt.plot(spikes,y,'g^') 
plt.show()

