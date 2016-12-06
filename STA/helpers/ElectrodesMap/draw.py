
import numpy 
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse 	


parser = argparse.ArgumentParser(prog='calculaMeans.py',
	description='Calcula firing rate de las units procesadas con el neuroexplorer',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
	help='Source folder',
	type=str, required=True)
parser.add_argument('--outputFolder',
	help='Output folder',
	type=str, required=True)
parser.add_argument('--Flashes',
	help='List of types flash',
	type=str, required=False, default='')
args = parser.parse_args()
 

coordenadas = []
unidades = []
sourceFolder = args.sourceFolder
outputFolder = args.outputFolder
pathFlashes = args.Flashes

if sourceFolder[-1] != '/':
	sourceFolder = sourceFolder+'/'
name_experiment = sourceFolder.split('/')[-3]
for unit in os.listdir(sourceFolder):
	dir = sourceFolder + unit 
	if os.path.isdir(dir):
		if os.path.isfile(dir+"/resultado.txt"):
			coordenadas.append(numpy.loadtxt(dir+"/resultado.txt"))
			unidades.append(unit)

if pathFlashes != '':
	if os.path.isfile(pathFlashes):
 		flashes = numpy.loadtxt(pathFlashes)

		
salida = []

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')

for iter in range(len(coordenadas)):
	frame = coordenadas[iter][0]
	amp = coordenadas[iter][1]
	a = coordenadas[iter][3]*50#/2.0
	b = coordenadas[iter][4]*50#/2.0
	angulo = coordenadas[iter][2]
	x0 = numpy.abs(coordenadas[iter][5])*50
	y0 = numpy.abs(coordenadas[iter][6])*50
	z0 = coordenadas[iter][7]

	splitname = unidades[iter].split("_")
	salida.append([a, b, numpy.around(x0), numpy.around(y0), splitname[0]+' '+splitname[1]])



	template = int(splitname[1][4:-4])
	#template = int(splitname[1])-1 #especial para 2016-04-11
	# if pathFlashes != '':
	# 	if flashes[template] == 1:
	# 		flashcolor = 'r'
	# 	elif flashes[template] == 2:
	# 		flashcolor = 'b'
	# 	elif flashes[template] == 3:
	# 		flashcolor = 'g'
	# 	else:
	# 		flashcolor = 'none'
	# else:
	# 	flashcolor = 'b'
	flashcolor = 'r'
	#pellipse = patches.Ellipse((x0,y0),a*2,b*2,angle=angulo,facecolor=flashcolor,alpha=0.2, edgecolor='none')
	#ax.add_patch(pellipse)
	pellipse = patches.Ellipse((x0,y0),a*2,b*2,angle=angulo,fill=False, edgecolor=flashcolor, alpha=0.6)
	ax.add_patch(pellipse)
	plt.annotate(splitname[1][5:-4],xy=(x0,y0),fontsize=7, color=numpy.random.rand(3,))
	#if flashcolor != 'none':
	#plt.text(x0,y0, splitname[1][5:-4], fontsize=7, color=numpy.random.rand(3,))

#plt.title("Mapa campos receptivos,"+name_experiment)
plt.xlabel('[um]')
plt.ylabel('[um]')
lim = [-4*50,35*50]
minor_ticks = numpy.arange(lim[0], lim[1], 100)                                              
major_ticks = numpy.arange(0, lim[1], 400)                                               

ax.set_xticks(major_ticks)                                                       
ax.set_xticks(minor_ticks, minor=True)                                           
ax.set_yticks(major_ticks)                                                       
ax.set_yticks(minor_ticks, minor=True)     
ax.grid(which='both')   
ax.grid(which='minor', alpha=0.2)                                                
ax.grid(which='major', alpha=0.5)  
ax.set_xlim(lim[0], lim[1])
ax.set_ylim(lim[0], lim[1])


fig.savefig(outputFolder+"mapaelectrodo.png", format='png', dpi=300, bbox_inches='tight')
fig.savefig(outputFolder+"mapaelectrodo.pdf", format='pdf', dpi=300, bbox_inches='tight')

salida.sort(key=lambda tup: (tup[2], tup[3]))
for kiter in range(len(salida)):
	print "%f\t %f\t %d\t %d\t %s" % (salida[kiter][0], salida[kiter][1], salida[kiter][2], salida[kiter][3], salida[kiter][4])
print '-----------------------------------------------------------------------------------------------------'
salida.sort(key=lambda tup: (tup[3], tup[2]))
for kiter in range(len(salida)):
	print "%f\t %f\t %d\t %d\t %s" % (salida[kiter][0], salida[kiter][1], salida[kiter][2], salida[kiter][3], salida[kiter][4])


# merge = raw_input("Deseas hacer un merge propuesto? (s/n)")
# if merge is 's':
# 	print '-----------------------------------------------------------------------------------------------------'
# else:
# 	exit(0)

# estado = 0
# merge_stage = numpy.zeros(1000)
# nueva_salida = numpy.array(salida)
# nueva_salida = nueva_salida[:,4]

# for kiter in range(len(salida)-1):
# 	if salida[kiter][2] == salida[kiter+1][2] and salida[kiter][3] == salida[kiter+1][3]:
# 		if estado:
# 			print "\t %1.2f\t %1.2f\t %d\t %d\t %s (%d)" % (salida[kiter+1][0], salida[kiter+1][1], salida[kiter+1][2], salida[kiter+1][3], salida[kiter+1][4], nueva_salida[kiter+1])

# 			merge = raw_input('merge (s/n): ')
# 			if merge is 's':
# 				if salida[menor][4] > salida[kiter+1][4]:
# 					for n in range(kiter+2,len(nueva_salida)):
# 						if nueva_salida[menor] < nueva_salida[n]:
# 							nueva_salida[n] -= 1
# 				else:
# 					for n in range(kiter+2,len(nueva_salida)):
# 						if nueva_salida[kiter+1] < nueva_salida[n]:
# 							nueva_salida[n] -= 1
# 			elif merge is 'n':
# 				print 'no se hace MERGE'
# 			else:
# 				print 'no se hizo nada'


# 		else:
# 			print "\n\t %1.2f\t %1.2f\t %d\t %d\t %s (%d)" % (salida[kiter][0], salida[kiter][1], salida[kiter][2], salida[kiter][3], salida[kiter][4], nueva_salida[kiter])
# 			print "\t %1.2f\t %1.2f\t %d\t %d\t %s (%d)" % (salida[kiter+1][0], salida[kiter+1][1], salida[kiter+1][2], salida[kiter+1][3], salida[kiter+1][4], nueva_salida[kiter+1])
# 			estado = 1

# 			merge = raw_input('merge (s/n): ')
# 			if merge is 's':
# 				if salida[kiter][4] > salida[kiter+1][4]:
# 					menor = kiter+1
# 					for n in range(kiter+2,len(nueva_salida)):
# 						if nueva_salida[kiter] < nueva_salida[n]:
# 							nueva_salida[n] -= 1
# 				else:
# 					menor = kiter
# 					for n in range(kiter+2,len(nueva_salida)):
# 						if nueva_salida[kiter+1] < nueva_salida[n]:
# 							nueva_salida[n] -= 1
# 			elif merge is 'n':
# 				print 'no se hace MERGE'
# 			else:
# 				print 'no se hizo nada'

# 	else:
# 		if estado:
# 			estado = 0
# 		else:
# 			print "%1.2f\t %1.2f\t %d\t %d\t %s (%d)" % (salida[kiter][0], salida[kiter][1], salida[kiter][2], salida[kiter][3], salida[kiter][4], nueva_salida[kiter])
