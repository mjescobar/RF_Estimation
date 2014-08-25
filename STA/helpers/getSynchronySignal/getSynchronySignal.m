function getSynchronySignal(mcdFile,outPut);
% GET SYNCHRONY SIGNAL FROM MCD DATA FILE (NEUROSHARE)
% AASTUDILLO OCTOBER 2013

% It is neccessary to have the ns library for Matlab and the DLL file in
% Windows

% Casep, Cambio para cargar la biblioteca correspondiente de acuerdo al OS
if isunix
    % Debiera ser parametro?
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDLibrary.so' )
else
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDlibrary64.dll' )
end
% open mcd lib files 
% [nsresult] = ns_SetLibrary( 'ns/nsMCDlibrary64.dll' )
% ns_SetDLL   Opens a Neuroshare Shared Library (.DLL or .so) in prepearation for other work
[nsresult,info] = ns_GetLibraryInfo()

%% open mcd data container file
% pathname = '';
% filename1 = 'datos0001.mcd';
% filename = '../datos0001.mcd';

%pathname = '';%'C:\Users\ALIEN3\Desktop\resultados_26-12\';

filename2 = outPut;

%filename = [filename2,'.mcd'];

% Casep, ahora desde parametro
filename = mcdFile

[nsresult, hfile] = ns_OpenFile([filename])
[nsresult,info_file] = ns_GetFileInfo(hfile)

EntityNumber =253; % entity number to choose and analyze

EntityCount = info_file.EntityCount; % total number of entities in the file
TimeStampRes = info_file.TimeStampResolution; % time between samples in seconds
TimeSpan = info_file.TimeSpan; % total time in seconds

%% open one entity from mcd data file

% EntityNumber = 253; % entity number to choose and analyze

[nsresult,entity] = ns_GetEntityInfo(hfile,EntityNumber)
%[nsresult,event] = ns_GetEventInfo(hfile,EntityNumber) % Trigger
%[nsresult,timestamp,data,datasize] = ns_GetEventData(hfile,numeroentidad,1) % Trigger
[nsresult,analog] = ns_GetAnalogInfo(hfile,EntityNumber) % Digital data

% get all entities labels:
for k = 1:info_file.EntityCount;
    [nsresult,entity] = ns_GetEntityInfo(hfile,k);
    EntityLabels{k} = entity.EntityLabel;
end

%% get raw data from entity and plot (example)
% EntityNumber = 253; %
entidad1 = EntityLabels{EntityNumber}

%%
bloque = 600;
inicio = bloque*10000+1;
%fin = round(entity.ItemCount/2);
fin = bloque*10000+10000;
BlockSize = 10000; % 500ms

fs = analog.SampleRate;
time_resolution = info_file.TimeStampResolution;

[nsresult,entity] = ns_GetEntityInfo(hfile,EntityNumber)
% [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
[nsresult,count,data] = ns_GetAnalogData(hfile,EntityNumber,inicio,BlockSize); % Digital data

ItemCount = entity.ItemCount;

% figures
xfigura = (inicio:fin)/fs;
yfigura = 1000000*data; %scale amplitude
%yfigura2 = 1000000*y; %scale amplitude

h1=figure;
subplot(3,1,1); plot(xfigura,yfigura);
title('Sync Block Data'); xlabel('Time s'); ylabel('Amplitude uV'); grid;
% subplot(3,1,2); plot(xfigura,yfigura2);
% title('Filtered Block Data'); xlabel('Time s'); ylabel('Amplitude uV'); grid;
% subplot(3,2,5); plot(xfreq,afdata);
% title('DFT Block Data'); xlabel('Frequency Hz'); ylabel('Magnitude'); grid;
% subplot(3,2,6); plot(xfreq,afy);
% title('DFT Filtered Block Data'); xlabel('Frequency Hz'); ylabel('Magnitude'); grid;

print(h1,'-dpdf',['Sync_h253_',filename2,'.pdf']);

%% save sync signal
[nsresult,entity] = ns_GetEntityInfo(hfile,EntityNumber)
% [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
[nsresult,count,datos] = ns_GetAnalogData(hfile,EntityNumber,1,ItemCount); % Digital data

% filename
% scipy.io.savemat('sync_signal_'+file_name+'.mat',mdict ={'datos':data},oned_as='column')
save(['syn_signal1_',filename2,'.mat'],'datos');

