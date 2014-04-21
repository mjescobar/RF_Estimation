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
from os import walk
import sys

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

##  @var archivos
#   Aca se almacena listado de archivos procesados        
archivos = []

##  colour_picker Seleccionar uno de los 7 colores de python (blanco 
#   exlcluido) para el color de la espiga
#   @param x x-esima espiga a graficar
#   los colores a utilizar son
#   b, g, r, c, m, y, k
#   seleccionados secuencialmente
def colour_picker(x):
	modulo = x % 7
	if modulo == 0:
		return 'b'
	elif modulo == 1:
		return 'g'
	elif modulo == 2:
		return 'r'
	elif modulo == 3:
		return 'c'
	elif modulo == 4:
		return 'm'
	elif modulo == 5:
		return 'y'
	elif modulo == 6:
		return 'k'


##  carga_spikes Dado un directorio carga los spikes desde los archivos
#   disponibles (*txt) en el.
#   @param directorio diretorio que contiene los .txt (se recibe como 
#   parametro de ejecución)
#   @param spikes matriz donde se cargaran los tiempos de ocurrencia de
#   los spikes
#   @param archivos matriz donde se cargaran los nombres de los archivos
#   de los cuales se recuperaron las matrices
def carga_sipkes(directorio,spikes,archivos):
    for (dirpath, dirnames, filenames) in walk(directorio):
		for archivo in filenames:
			archivos.append(archivo)
			spikes_archivo = []
			f = open(directorio+archivo, 'r')
			for line in f:
				spikes_archivo.append(float(line))
			f.close()
			spikes.append(spikes_archivo)


##  grafica_todas_spikes Dado los spikes recuperados realiza una unica grafica
#   @param spikes matriz de los timestamps de las espigas, cargado en
#   funcion carga_spikes
#   @param archivos matriz con los nombres de los archivos desde los
#   que se recupero los timestamps
def grafica_todas_spikes(spikes,archivos):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in range(0,len(spikes)):
		largo_datos = len(spikes[i])
		y = []
		y = y + [i*4]*(largo_datos - len(y))
		ax.plot(spikes[i],y,colour_picker(i)+'x') 
	plt.title('Spikes en el tiempo', fontdict=font)
	plt.xlabel('Tiempo', fontdict=font)
	plt.ylabel('Unidades (neuronas)', fontdict=font)
	plt.xlim(0,1050)
	plt.ylim([0, len(spikes)*4])
	ax.set_yticks(range(0,len(archivos)*4,4))
	ax.set_yticklabels(archivos)
	plt.setp(ax.get_yticklabels(), fontsize=10)
	plt.subplots_adjust(left=0.15)
	plt.savefig('Spikes_en_tiempo.png', format='png', bbox_inches='tight')
	plt.show()

if len(sys.argv) == 2:
	carga_sipkes(sys.argv[1],spikes,archivos)
	grafica_todas_spikes(spikes,archivos)
else:
	print "Usage "
	print "./grafica_spikes.py folder_with_timestamps"
