function readFormatData(pathCell,cellId,stim, pathTimeStamp, spk_start, spk_end, sta_start, sta_end)
% % pathCell: ruta donde esta la carpeta con los archivos del STA
% % cellId: nombre de la unidad que se quiere analisar
% % stim: ruta completa del archivo .mat donde esta el estimulo del WN
% % pathTimeStamp: ruta de la carpeta donde esta el archivo .txt con los TS
% % spk_start: tiempo donde comienza el WN en el registro (en seg)
% % spk_end: tiempo donde termina el WN en el registro (en seg)
% % sta_start: frame de inicio del filtro STA
% % sta_end: frame de termino del filtro STA

% % sta_start y sta_end permiten definir los el largo del filtro del STA, 
% % esto dado que hay diferentes largos de filtros en los experimentos.

%% Format and read data
addpath('NIMtoolbox/')

% pathCell = '/home/cesar/Dropbox/Experimentos/Clustering/exp/2015-01-29/'
% cellId = 'A8_temp0016-060'
% pathStim = '/home/cesar/exp/2015-01-29/sync/stim_mini_2015-01-29.mat'
% pathTimeStamp = '/home/cesar/Dropbox/Experimentos/Clustering/exp/TS/2015-01-29/'

% pathCell = '/home/cesar/Dropbox/Experimentos/Clustering/stim/';
% cellId = 'A4_temp0163-216';
% cellId = 'B3_temp0402-211';
% pathStim = '/home/cesar/Dropbox/Experimentos/Clustering/stim/stim_mini_2016-06-10.mat';
% pathTimeStamp = '/home/cesar/Dropbox/Experimentos/Clustering/stim/';

dt=1.0/60.0;
fprintf('Unidad en analisis %s\n',cellId)

% Loading and formatting stim_mini
% stim = load(pathStim);
% [nx,ny,tt,nfr] = size(stim.stim);
% tt = stim.stim(:,:,2,:);
% stim=reshape(tt,nx,ny,nfr);
% clear tt;
% clear ny;
% clear nx;

%% Creating raster from spikelist
[~,~,~,nfr] = size(stim);
spks=load([pathTimeStamp, cellId, '.txt']);
spks_temp = spks(spks < spk_end) - spk_start;
spks=spks_temp(spks_temp >0);
fprintf('Unidad con %d spikes.\n',length(spks))
raster=createRaster(spks,nfr,dt);

%% Creating data structure
data.stim = stim;
data.raster = raster';
clear raster;
% clear stim;
clear spks;

% Loading STA data
statemp = load([pathCell cellId '_lineal/' 'sta_array_' cellId '.mat']);
sta = statemp.STA_array;
clear statemp;
sta = sta(:,:,sta_start:sta_end);
[nx,ny,nt]=size(sta);
for i=1:nt
    statemp(:,:,i)=sta(:,:,nt-i+1); % Inverting temporal data
end
clear i;

% Creating cell data structure with STA data
sta_array{1} = 0;
sta_array{2} = statemp;
sta_array = cellfun(@(x) x./norm(x(:)),sta_array,'uniformoutput',0);
clear statemp;
clear sta;

% Reading Guassian fit data
fit_data = load([pathCell cellId '_lineal/' 'fit_var.mat']);
fitres{1} = fit_data.fitresult;
clear fit_data;

%% Ready to launch ComputeNLfromSTA code
[nlData,~] = ComputeNLfromSTA(data,sta_array,fitres,nt,nx,round(dt*1000));
save([pathCell cellId '_lineal/' 'NL.txt'],'fitparams','-ascii');
save([pathCell cellId '_lineal/' 'NL.mat'],'nlData','-mat');

PlotNLfromNIM_MJ(nlData,cellId,pathCell,'')

