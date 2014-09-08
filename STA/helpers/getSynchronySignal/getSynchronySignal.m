function getSynchronySignal(mcdFile,outputFolder,fileName,channelNumber);
% GET SYNCHRONY SIGNAL FROM MCD DATA FILE (NEUROSHARE)

%% Parameters

% mcdFile: Full path to the mcd file to analyze 'K:\2014-09-05\001.mcd'
% outputFolder : Full path to the output folder 'K:\2014-09-05\'
% fileName : filename for the syncrony signal file '2014_09_05'
% channelNumber : by dafault the analog data is the 253

%%
% Casep, Cambio para cargar la biblioteca correspondiente de acuerdo al OS
if isunix
    % Debiera ser parametro?
    addpath('../../lib/NeuroShare/');
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDLibrary.so' )
else
	addpath(fullfile(pwd,'../../lib','NeuroShare'))
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDlibrary64.dll' )
end

[nsresult,info] = ns_GetLibraryInfo()

%% open mcd data container file

% Casep, ahora desde parametro
[nsresult, hfile] = ns_OpenFile([mcdFile])
[nsresult,info_file] = ns_GetFileInfo(hfile)

EntityNumber =253; % entity number to choose and analyze

EntityCount = info_file.EntityCount; % total number of entities in the file
TimeStampRes = info_file.TimeStampResolution; % time between samples in seconds
TimeSpan = info_file.TimeSpan; % total time in seconds

%% open one entity from mcd data file

[nsresult,entity] = ns_GetEntityInfo(hfile,channelNumber)
%[nsresult,event] = ns_GetEventInfo(hfile,EntityNumber) % Trigger
%[nsresult,timestamp,data,datasize] = ns_GetEventData(hfile,numeroentidad,1) % Trigger
[nsresult,analog] = ns_GetAnalogInfo(hfile,channelNumber) % Digital data

% get all entities labels:
for k = 1:info_file.EntityCount;
    [nsresult,entity] = ns_GetEntityInfo(hfile,k);
    EntityLabels{k} = entity.EntityLabel;
end

%% get raw data from entity and plot (example)
% EntityNumber = 253; %
entidad1 = EntityLabels{channelNumber}

%%
bloque = 600;
inicio = bloque*10000+1;
%fin = round(entity.ItemCount/2);
fin = bloque*10000+10000;
BlockSize = 10000; % 500ms

fs = analog.SampleRate;
time_resolution = info_file.TimeStampResolution;

[nsresult,entity] = ns_GetEntityInfo(hfile,channelNumber)
% [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
[nsresult,count,data] = ns_GetAnalogData(hfile,channelNumber,inicio,BlockSize); % Digital data

ItemCount = entity.ItemCount;

% figures
xfigura = (inicio:fin)/fs;
yfigura = 1000000*data; %scale amplitude


h1=figure;
subplot(3,1,1); plot(xfigura,yfigura);
title('Sync Block Data'); xlabel('Time s'); ylabel('Amplitude uV'); grid;

print(h1,'-dpdf',[outputFolder,'Sync_',num2str(channelNumber),'_',fileName,'.pdf']);

%% save sync signal
[nsresult,entity] = ns_GetEntityInfo(hfile,channelNumber)
% [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
[nsresult,count,datos] = ns_GetAnalogData(hfile,channelNumber,1,ItemCount); % Digital data

save([outputFolder,'syn_signal_',fileName,'.mat'],'datos');

