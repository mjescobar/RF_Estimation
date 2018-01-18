function readFormatData(pathCell,cellId,pathStim, pathTimeStamp)
%% Format and read data
%addpath('NIMtoolbox/');
%addpath('.');
addpath('NIMtoolbox/')

% pathCell = '/home/cesar/Dropbox/Experimentos/Clustering/exp/2015-01-29/'
% cellId = 'A8_temp0016-060'
% pathStim = '/home/cesar/exp/2015-01-29/sync/stim_mini_2015-01-29.mat'
% pathTimeStamp = '/home/cesar/Dropbox/Experimentos/Clustering/exp/TS/2015-01-29/'

%cd /home/cesar/Downloads/linealidad_versus_nolinealidad/F4_temp0331-069_lineal
%cellId='F4_temp0331-069';

%cd(pathCell)
dt=1.0/60;
disp(cellId)
% Loading and formatting stim_mini
%stim = load('../stim_mini.mat');

stim = load(pathStim);
[nx,ny,tt,nfr] = size(stim.stim);
tt = stim.stim(:,:,2,:);
stim=reshape(tt,nx,ny,nfr);
clear tt;
clear ny;
clear nx;

% Creating raster from spikelist
%spks=load(['../' cellId '_lineal/' cellId, '.txt']);
spks=load([pathTimeStamp, cellId, '.txt']);
size(spks)
raster=createRaster(spks,nfr,dt);

% Creating data structure
data.stim = stim;
data.raster = raster';
clear raster;
clear stim;
clear spks;

% Loading STA data
statemp = load([pathCell cellId '_lineal/' 'sta_array_' cellId '.mat']);
sta = statemp.STA_array;
clear statemp;
sta = sta(:,:,1:18);
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
dt = round(dt*1000); % Time in msec
[nlData,fitparams] = ComputeNLfromSTA(data,sta_array,fitres,nt,nx,dt);
save([pathCell cellId '_lineal/' 'NL.txt'],'fitparams','-ascii');
save([pathCell cellId '_lineal/' 'NL.mat'],'nlData','-mat');

PlotNLfromNIM_MJ(nlData,cellId,pathCell,'')

