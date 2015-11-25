
import numpy 
import os
from numpy import linspace
from scipy import pi,sin,cos
import pylab as p
import argparse 	


parser = argparse.ArgumentParser(prog='calculaMeans.py',
	description='Calcula firing rate de las units procesadas con el neuroexplorer',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFolder',
	help='Source folder',
	type=str, required=True)
	 
args = parser.parse_args()
 
def Ellipse(a,b,an,x0,y0): #an is the rotational angle
    points=100 #Number of points whicnh needs to construct the elipse
    cos_a,sin_a=cos(an*pi/180),sin(an*pi/180)
    the=linspace(0,2*pi,points)
    #Here goes the general ellpse, x0, y0 is the origin of the ellipse in xy plane
    X=a*cos(the)*cos_a-sin_a*b*sin(the)+x0
    Y=a*cos(the)*sin_a+cos_a*b*sin(the)+y0
    return X,Y

coordenadas = []
sourceFolder = args.sourceFolder

for unit in os.listdir(sourceFolder):
	dir = sourceFolder + unit 
	if os.path.isdir(dir):
		coordenadas.append(numpy.loadtxt(dir+"/resultado.txt")) 	
		

fig = p.figure(figsize=(8,15))
p.axis([0,31,0,31])
i = 0
for iter in range(len(coordenadas)):
	frame = coordenadas[iter][0]
	amp = coordenadas[iter][1]
	a = coordenadas[iter][3]/2.0
	b = coordenadas[iter][4]/2.0
	angulo = coordenadas[iter][2]
	x0 = coordenadas[iter][5]
	y0 = coordenadas[iter][6]
	z0 = coordenadas[iter][7]
	X,Y=Ellipse(a,b,angulo,x0,y0)
	i += 1
	print i, frame, amp, a, b, angulo, x0, y0, z0
	# p.plot(X,Y,"b.-") 
	# if a > 1.5 or b > 1.5 :
	# 	p.plot(X,Y) 
	# 	p.gca().set_color_cycle(None)
	p.plot(X,Y) 
	p.title("Mapa campos receptivos, exp 20140620 con SpyKing Circus")
	p.gca().set_color_cycle(None)

 
# X,Y=Ellipse(5,8,45,0,0)
# p.plot(X,Y,"r.-")
 
# X,Y=Ellipse(5,8,90,0,0)
# p.plot(X,Y,"g.-")
 
# X,Y=Ellipse(5,8,135,0,0)
# p.plot(X,Y,"y.-")
# #Draw me some circles, the circles are independent of the angle theta! Check it yourself
# X,Y=Ellipse(5,5,0,0,0)
# p.plot(X,Y)
 
# X,Y=Ellipse(8,8,0,0,0)
# p.plot(X,Y)

p.grid(True)
p.axes().set_aspect('equal')
p.show()