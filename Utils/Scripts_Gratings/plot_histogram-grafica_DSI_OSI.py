from matplotlib.pylab import hist, show, figure, savefig, plot, grid, xlim, ylim, xticks, xlabel, ylabel, title, legend
import numpy 
dsi_file = "./DSI_max.txt"  #Valores de DSI_max para cada unidad para realizar el histograma
osi_file = "./OSI_max.txt"  #Valores de OSI_max con DSI_max < 0.5 para cada unidad para realizar el histograma
dsi_resumen05_file = "./DSI_resumen05.txt" #numero de repeticiones DSI>0.5 según velocidad y ancho en el orden. V2[067,125,250],V4[067,125,250],V8[067,125,250]
osi_resumen05_file = "./OSI_resumen05.txt" #numero de repeticiones OSI>0.5 según velocidad y ancho en el orden. V2[067,125,250],V4[067,125,250],V8[067,125,250]

dsi_data = numpy.loadtxt(dsi_file)
osi_data = numpy.loadtxt(osi_file)
dsi_resumen05 = numpy.loadtxt(dsi_resumen05_file)
osi_resumen05 = numpy.loadtxt(osi_resumen05_file)

fig = figure()
hist([dsi_data,osi_data],bins=[0, 0.1, 0.2, 0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], alpha=0.8, histtype='bar', rwidth=0.8, color=['crimson', 'burlywood'], label=['DSI', 'OSI, DSI<0.5'] )
legend()
savefig("hist_DSI.png",format='png', bbox_inches='tight')


#fig = figure()
#hist(osi_data,20, (-1,1),histtype='bar', stacked=True)
#savefig("hist_OSI.png",format='png', bbox_inches='tight')

vel = [2,4,8]
vel_labels = ['2','4','8'] 

fig = figure()
plot(vel,dsi_resumen05[0:9:3]/numpy.sum(dsi_resumen05[0:9:3])*100,'r',vel,dsi_resumen05[0:9:3]/numpy.sum(dsi_resumen05[0:9:3])*100,'bo')
xticks(vel,vel_labels)
title("067")
xlim(0, 10)
ylim(0,100)
xlabel('cycle/s')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("velocidad_dsi_067.png", format='png', dpi=300)

fig = figure()
plot(vel,dsi_resumen05[1:9:3]/numpy.sum(dsi_resumen05[1:9:3])*100,'r', vel,dsi_resumen05[1:9:3]/numpy.sum(dsi_resumen05[1:9:3])*100,'bo')
xticks(vel,vel_labels)
title("125")
xlim(0, 10)
ylim(0,100)
xlabel('cycle/s')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("velocidad_dsi_125.png", format='png', dpi=300)

fig = figure()
plot(vel,dsi_resumen05[2:9:3]/numpy.sum(dsi_resumen05[2:9:3])*100,'r',vel,dsi_resumen05[2:9:3]/numpy.sum(dsi_resumen05[2:9:3])*100,'bo')
xticks(vel,vel_labels)
title("250")
xlim(0, 10)
ylim(0,100)
xlabel('cycle/s')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("velocidad_dsi_250.png", format='png', dpi=300)

#--------------------------------------------------------------------------------------

fig = figure()
plot(vel,osi_resumen05[0:9:3]/numpy.sum(osi_resumen05[0:9:3])*100,'r',vel,osi_resumen05[0:9:3]/numpy.sum(osi_resumen05[0:9:3])*100,'bo')
xticks(vel,vel_labels)
title("067")
xlim(0, 10)
ylim(0,100)
xlabel('cycle/s')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("velocidad_osi_067.png", format='png', dpi=300)

fig = figure()
plot(vel,osi_resumen05[1:9:3]/numpy.sum(osi_resumen05[1:9:3])*100,'r', vel,osi_resumen05[1:9:3]/numpy.sum(osi_resumen05[1:9:3])*100,'bo')
xticks(vel,vel_labels)
title("125")
xlim(0, 10)
ylim(0,100)
xlabel('cycle/s')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("velocidad_osi_125.png", format='png', dpi=300)

fig = figure()
plot(vel,osi_resumen05[2:9:3]/numpy.sum(osi_resumen05[2:9:3])*100,'r',vel,osi_resumen05[2:9:3]/numpy.sum(osi_resumen05[2:9:3])*100,'bo')
xticks(vel,vel_labels)
title("250")
xlim(0, 10)
ylim(0,100)
xlabel('cycle/s')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("velocidad_osi_250.png", format='png', dpi=300)



#------------------------------------------------------------------------
#------------------------------------------------------------------------
vel = [100,200,400]
vel_labels = ['100','200','400'] 

fig = figure()
plot(vel,dsi_resumen05[0:3]/numpy.sum(dsi_resumen05[0:3])*100,'r',vel,dsi_resumen05[0:3]/numpy.sum(dsi_resumen05[0:3])*100,'bo')
xticks(vel,vel_labels)
title("V2")
xlim(0, 500)
ylim(0,100)
xlabel('um')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("widebar_dsi_V2.png", format='png', dpi=300)

fig = figure()
plot(vel,dsi_resumen05[3:6]/numpy.sum(dsi_resumen05[3:6])*100,'r', vel,dsi_resumen05[3:6]/numpy.sum(dsi_resumen05[3:6])*100,'bo')
xticks(vel,vel_labels)
title("V4")
xlim(0, 500)
ylim(0,100)
xlabel('um')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("widebar_dsi_V4.png", format='png', dpi=300)

fig = figure()
plot(vel,dsi_resumen05[6:9]/numpy.sum(dsi_resumen05[6:9])*100,'r',vel,dsi_resumen05[6:9]/numpy.sum(dsi_resumen05[6:9])*100,'bo')
xticks(vel,vel_labels)
title("V8")
xlim(0, 500)
ylim(0,100)
xlabel('um')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("widebar_dsi_V8.png", format='png', dpi=300)

#--------------------------------------------------------------------------------------

fig = figure()
plot(vel,osi_resumen05[0:3]/numpy.sum(osi_resumen05[0:3])*100,'r',vel,osi_resumen05[0:3]/numpy.sum(osi_resumen05[0:3])*100,'bo')
xticks(vel,vel_labels)
title("V2")
xlim(0, 500)
ylim(0,100)
xlabel('um')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("widebar_osi_V2.png", format='png', dpi=300)

fig = figure()
plot(vel,osi_resumen05[3:6]/numpy.sum(osi_resumen05[3:6])*100,'r', vel,osi_resumen05[3:6]/numpy.sum(osi_resumen05[3:6])*100,'bo')
xticks(vel,vel_labels)
title("V4")
xlim(0, 500)
ylim(0,100)
xlabel('um')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("widebar_osi_V4.png", format='png', dpi=300)

fig = figure()
plot(vel,osi_resumen05[6:9]/numpy.sum(osi_resumen05[6:9])*100,'r',vel,osi_resumen05[6:9]/numpy.sum(osi_resumen05[6:9])*100,'bo')
xticks(vel,vel_labels)
title("V8")
xlim(0, 500)
ylim(0,100)
xlabel('um')
ylabel('% of cells with OSI >= 0.5')
grid(True)
savefig("widebar_osi_V8.png", format='png', dpi=300)
