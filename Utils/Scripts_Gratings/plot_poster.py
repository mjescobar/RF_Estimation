import numpy as npy 
import matplotlib.cm as cm      	  # plot lib
import matplotlib.pyplot as plt 	  # plot lib (for figures)
from matplotlib import rc

exp1Categoria = npy.loadtxt('/home/monica/Dropbox/Cesar/Gratings/exp1_DSIporcategoria.txt')
exp2Categoria = npy.loadtxt('/home/monica/Dropbox/Cesar/Gratings/exp2_DSIporcategoria.txt')
exp1subCategoria = npy.loadtxt('/home/monica/Dropbox/Cesar/Gratings/exp1_DSIporSUBcategoria.txt')
exp2subCategoria = npy.loadtxt('/home/monica/Dropbox/Cesar/Gratings/exp2_DSIporSUBcategoria.txt')
datos = 'suball'
ymin, ymax = 0, 1
outputFolder = '/home/monica/Dropbox/Cesar/Gratings/Resultsssss/'

if datos == 'all':
	V2 = exp2Categoria[0:3]+exp1Categoria[0:3]
	V4 = exp2Categoria[3:6]+exp1Categoria[3:6]
	V8 = exp2Categoria[6:9]+exp1Categoria[6:9]
	A067 = exp2Categoria[0:9:3]+exp1Categoria[0:9:3]
	A125 = exp2Categoria[1:9:3]+exp1Categoria[1:9:3]
	A250 = exp2Categoria[2:9:3]+exp1Categoria[2:9:3]
elif datos == 'exp1':
	V2 = exp1Categoria[0:3]
	V4 = exp1Categoria[3:6]
	V8 = exp1Categoria[6:9]
	A067 = exp1Categoria[0:9:3]
	A125 = exp1Categoria[1:9:3]
	A250 = exp1Categoria[2:9:3]
elif datos == 'exp2':
	V2 = exp2Categoria[0:3]
	V4 = exp2Categoria[3:6]
	V8 = exp2Categoria[6:9]
	A067 = exp2Categoria[0:9:3]
	A125 = exp2Categoria[1:9:3]
	A250 = exp2Categoria[2:9:3]
elif datos == 'suball':
	V2 = (exp2subCategoria[0:3]+exp1subCategoria[0:3])/float(npy.sum(exp2subCategoria[0:3])+npy.sum(exp1subCategoria[0:3]))*100
	V4 = (exp2subCategoria[3:6]+exp1subCategoria[3:6])/float(npy.sum(exp2subCategoria[3:6])+npy.sum(exp1subCategoria[3:6]))*100
	V8 = (exp2subCategoria[6:9]+exp1subCategoria[6:9])/float(npy.sum(exp2subCategoria[6:9])+npy.sum(exp1subCategoria[6:9]))*100
	A250 = (exp2subCategoria[0:9:3]+exp1subCategoria[0:9:3])/float(npy.sum(exp2subCategoria[0:9:3])+npy.sum(exp1subCategoria[0:9:3]))*100
	A125 = (exp2subCategoria[1:9:3]+exp1subCategoria[1:9:3])/float(npy.sum(exp2subCategoria[1:9:3])+npy.sum(exp1subCategoria[1:9:3]))*100
	A067 = (exp2subCategoria[2:9:3]+exp1subCategoria[2:9:3])/float(npy.sum(exp2subCategoria[2:9:3])+npy.sum(exp1subCategoria[2:9:3]))*100
elif datos == 'subexp1':
	V2 = exp1subCategoria[0:3]
	V4 = exp1subCategoria[3:6]
	V8 = exp1subCategoria[6:9]
	A067 = exp1subCategoria[0:9:3]
	A125 = exp1subCategoria[1:9:3]
	A250 = exp1subCategoria[2:9:3]
elif datos == 'subexp2':
	V2 = exp2subCategoria[0:3]
	V4 = exp2subCategoria[3:6]
	V8 = exp2subCategoria[6:9]
	A067 = exp2subCategoria[0:9:3]
	A125 = exp2subCategoria[1:9:3]
	A250 = exp2subCategoria[2:9:3]


barra = [100,200,400]
bar_labels = ['100','200','400']
velocidad =  [2,4,8]
vel_labels = ['2','4','8'] 



fig = plt.figure() 
plt.plot(barra,V2,'bo',barra,V2,'k')
plt.xticks(barra,bar_labels)
plt.xlim(0, 500)
plt.ylim(ymin,ymax)
plt.xlabel(r' [$\mu $m]')
plt.ylabel('Normalized Number Cell')
plt.grid(True)
plt.savefig(outputFolder+"V2_barra.eps", format='eps', dpi=300)

fig = plt.figure() 
plt.plot(barra,V4,'bo',barra,V4,'k')
plt.xticks(barra,bar_labels)
plt.xlim(0, 500)
plt.ylim(ymin,ymax)
plt.xlabel(r' [$\mu $m]')
plt.ylabel('Normalized Number Cell')
plt.grid(True)
plt.savefig(outputFolder+"V4_barra.eps", format='eps', dpi=300)

fig = plt.figure() 
plt.plot(barra,V8,'bo',barra,V8,'k')
plt.xticks(barra,bar_labels)
plt.xlim(0, 500)
plt.ylim(ymin,ymax)
plt.xlabel(r' [$\mu $m]')
plt.ylabel('Normalized Number Cell')
plt.grid(True)
plt.savefig(outputFolder+"V8_barra.eps", format='eps', dpi=300)

#############################

fig = plt.figure() 
plt.plot(velocidad,A067,'bo',velocidad,A067,'k')
plt.xticks(velocidad,vel_labels)
plt.xlim(0, 10)
plt.ylim(ymin,ymax)
plt.xlabel('(cycle/s)')
plt.ylabel('Normalized Number Cell')
plt.grid(True)
plt.savefig(outputFolder+"067_velocidad.eps", format='eps', dpi=300)

fig = plt.figure() 
plt.plot(velocidad,A125,'bo',velocidad,A125,'k')
plt.xticks(velocidad,vel_labels)
plt.xlim(0, 10)
plt.ylim(ymin,ymax)
plt.xlabel('(cycle/s)')
plt.ylabel('Normalized Number Cell')
plt.grid(True)
plt.savefig(outputFolder+"125_velocidad.eps", format='eps', dpi=300)

fig = plt.figure() 
plt.plot(velocidad,A250,'bo',velocidad,A250,'k')
plt.xticks(velocidad,vel_labels)
plt.xlim(0, 10)
plt.ylim(ymin,ymax)
plt.xlabel('(cycle/s)')
plt.ylabel('Normalized Number Cell')
plt.grid(True)
plt.savefig(outputFolder+"250_velocidad.eps", format='eps', dpi=300)




#plt.show()


