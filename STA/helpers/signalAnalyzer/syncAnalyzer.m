function syncAnalyzer(mcdFile,experimentName,entityNumber,distanceFrames,outputFolder)
% Get the sinchronization signal for experiments from MCD file.
% This script can recovery the exact time whe a frame was showed 
% in screen  using the red channel as lead. This channel has a 
% analog signal to the levels of intensities of red channel.
% 
% Keyword arguments:
% 
% 	mcdFile : path to .mcd file
% 	experimentName : Name of experiment
% 	entityNumber : number of channel where is the analog signal  in .mcd file
% 	distanceFrames : number of point between 2 frames. For example for 60fps 
% 					and sampleRating 20000, distanceFrames = 334
% 	outputFolder = directory path to save files 
% 
% 	example: 
% 	signalAnalyzer('../data/raw/exp_a.mcd','Exp_a',20000,1,334,'../data/sync/')
% 
% Returns: 2 files 
% 	(1) outputFolder,'start_end_frames_',experimentName,'.txt'
% 	(2) outputFolder,'repeted_frames_',experimentName,'.txt'
% 
% 	(1) has start end point of the frame showed in the experiment.
% 	(2) has all start point for the repeted frame
%
% AASTUDILLO 17/10/2013
% Modified by Ricardo Villarroel 2/12/2013
% Modified by Monica and Carlos 13/06/2014
% Modified by Cesar Reyes 23/07/2018
% 
% More:
% OPTIONAL SIMPLE ANALYSIS
% 
% 1) cada frame tiene una barra roja al final de su presentacion (en la base)
% 2) para cada barra roja la senal de sincronizacion muestra un pulso (app
% 1ms) de min 16 puntos sobre cierto umbral
% 3) el final de cada pulso representa el final de la presentacion de cada
% frame
% 4) en algunos casos cada frame es presentado dos veces (30 hz de
% presentacion) por lo que un frame en verdad es determinado por dos pulsos
% 5) la distancia  entre un pulso y otro determina el tiempo (en puntos) en
% que un frame fue mostrado.
% 6) el canto de bajada de un pulso de frame determina el final de un frame
% dado
% 7) el punto de inicio de cada frame debe ser estimado a partir de la
% distancia entre frames (en puntos) y el final de cada pulso


if isunix
    addpath('../../lib/NeuroShare/');
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDLibrary.so' );
else
    addpath(fullfile(pwd,'../../lib','NeuroShare'));
	[nsresult] = ns_SetLibrary(fullfile(pwd,'../../lib/NeuroShare','nsMCDlibrary64.dll'));
end

disp('Neuroshare information:')
[~,info] = ns_GetLibraryInfo()
[~, hfile] = ns_OpenFile([mcdFile])
[~,info_file] = ns_GetFileInfo(hfile)
[~,entity] = ns_GetEntityInfo(hfile,entityNumber)
% Analog signal to synchronize 
[~,~,analog_signal] = ns_GetAnalogData(hfile,entityNumber,1,entity.ItemCount); 

%% complete synchrony signal analysis : 

thresh_volts = 0.151111112; % umbral en volts, determina criticamente el performance de la deteccion de frames
wide_pulse = 50; % puntos maximos requeridos para considerar como un pulso de frame

nframes = 0;

for k = wide_pulse+1:length(analog_signal)-2
    if analog_signal(k) > thresh_volts
        before_point  = analog_signal(k-1) > thresh_volts;
        before_pulse = analog_signal(k-wide_pulse) < thresh_volts;
        after_point = analog_signal(k+1) < thresh_volts;
        if before_point && before_pulse && after_point
            nframes = nframes+1;
        end
    end
end

start_frames = zeros(1,nframes);
start_frames_amp = zeros(1,nframes);

nframes = 1;
for k = wide_pulse+1:length(analog_signal)-2
    if analog_signal(k) > thresh_volts
        before_point  = analog_signal(k-1) > thresh_volts;
        before_pulse = analog_signal(k-wide_pulse) < thresh_volts;
        after_point = analog_signal(k+1) < thresh_volts;
        if before_point && before_pulse && after_point
            start_frames(nframes) = k;
            start_frames_amp(nframes) = mean(analog_signal(k-wide_pulse:k));
            nframes = nframes+1;
        end
    end
end

%% Show repeted frames
thr_rep = 0.09;
amp_inter_frame = abs(diff(start_frames_amp));
repeted_frame_point = find(amp_inter_frame < thr_rep);

FIG1 = figure();
plot(amp_inter_frame); hold on
plot(repeted_frame_point,amp_inter_frame(repeted_frame_point),'r*'); hold off
title('Repeted frame'); xlabel('Time points'); ylabel('Diff amp V');
print(FIG1,'-dpdf',[outputFolder,'Figure_repeted_',experimentName,'.pdf']);

%% Show result
% take the time in middle of register to show the synchronizetion signal
middle_reg = start_frames(ceil(nframes/2));
win_plot = 4000;

raw_data_plot = analog_signal(middle_reg:middle_reg+win_plot-1);
start_frame_point = find((start_frames>middle_reg) & (start_frames<middle_reg+win_plot) );
start_frame_time = start_frames(start_frame_point)-middle_reg;

FIG2 = figure();
plot(raw_data_plot); 
hold on;
plot(raw_data_plot,'b.'); 
line([0 win_plot],[thresh_volts thresh_volts],'Color','r'); % thr
plot( start_frame_time , raw_data_plot(start_frame_time),'r*'); 
for j=1:length(start_frame_point)
    sp = start_frame_time(j);
    spv = raw_data_plot(sp);
    line( [sp - distanceFrames sp], [spv spv],'Color','r','LineWidth',2);
end
hold off;
grid;
title('Syncronization signal analysis example'); xlabel('Time points'); ylabel('Amplitude V');

print(FIG2,'-dpdf',[outputFolder,'Figure_Sync_',experimentName,'.pdf']);

%% output and save:
start_frames_repeted = start_frames(repeted_frame_point);
start_end_frame = [start_frames(1:end-1)', start_frames(2:end)'];
save([outputFolder,'start_end_frames_',experimentName,'.txt' ],'start_end_frame', '-ASCII' ,'-DOUBLE');
save([outputFolder,'repeted_frames_',experimentName,'.txt' ],'start_frames_repeted', '-ASCII' ,'-DOUBLE');

