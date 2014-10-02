function signalAnalyzerSimulado(mcdFile,experimentName,sampleRating,entityNumber,distanciaFrames,tiempoTotal,outputFolder);

if isunix
    % Debiera ser parametro?
    addpath('../../lib/NeuroShare/');
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDLibrary.so' )
else
    addpath(fullfile(pwd,'../../lib','NeuroShare'))
	[nsresult] = ns_SetLibrary(fullfile(pwd,'../../lib/NeuroShare','nsMCDlibrary64.dll'))
end

% % 
 [nsresult,info] = ns_GetLibraryInfo()
% % 
[nsresult, hfile] = ns_OpenFile([mcdFile])
[nsresult,info_file] = ns_GetFileInfo(hfile)
disp(info_file);

[nsresult,entity] = ns_GetEntityInfo(hfile,entityNumber)
% % 
% [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
[nsresult,count,data] = ns_GetAnalogData(hfile,entityNumber,1,entity.ItemCount); % Digital data

umbral_volts = 0.151111112; %0.1511 ; % umbral en volts, determina criticamente el performance de la deteccion de frames
puntos_pulso = 50; %24*2; 24; % puntos maximos requeridos para considerar como un pulso de frame

duracion_min = length(data)/sampleRating/60; % duracion en minutos de la senal
disp (duracion_min)
for k = puntos_pulso+1:length(data)-2
    if data(k) > umbral_volts
        if (data(k-1)>umbral_volts) && (data(k-puntos_pulso)< umbral_volts) && (data(k+1)<umbral_volts) && (data(k+1)<umbral_volts)
            primerPunto = k
            break
        end
    end
end

valorFinal= tiempoTotal*sampleRating*60;
iterations= floor(valorFinal/334); 
inicioFrames= zeros(iterations,2);
puntoActual=primerPunto;


for j = 1:iterations
    inicioFrames(j,1)=puntoActual;
    if (mod(j,2)==0)
        puntoActual=puntoActual+334;
        inicioFrames(j,2)=puntoActual;
    else 
        puntoActual=puntoActual+335;
        inicioFrames(j,2)=puntoActual;
    end
end

save([outputFolder,'Inicio_Frames',experimentName,'.txt' ],'inicioFrames', '-ASCII' ,'-DOUBLE');
    



disp (primerPunto)