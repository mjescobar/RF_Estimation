sr = 20000.0;

% pathCell = '/home/cesar/exp/2016-11-14_periferia/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-11-14_periferia/stim_mini_2016-11-14_periferia.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-11-14_periferia/';
% WN_time = '/home/cesar/exp/sync/2016-11-14_periferia/inicio_fin_frame_2016-11-14_periferia_CHECKERBOARD.txt';
% sta_start= 13;
% sta_end= 30;


% pathCell = '/home/cesar/exp/2016-11-14_periferia/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-11-14_periferia/stim_mini_2016-11-14_periferia.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-11-14_periferia/';
% WN_time = '/home/cesar/exp/sync/2016-11-14_periferia/inicio_fin_frame_2016-11-14_periferia_CHECKERBOARD.txt';
% sta_start= 13;
% sta_end= 30;

% pathCell = '/home/cesar/exp/2016-06-17_ret1_centro/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-06-17_centro/stim_mini_2016-06-17.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-06-17_centro/';
% WN_time = '/home/cesar/exp/sync/2016-06-17_centro/inicio_fin_frame_2016-06-17_centro_CHECKERBOARD.txt';
% sta_start= 13;
% sta_end= 30;

% pathCell = '/home/cesar/exp/2016-09-14_periferia/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-11-14_periferia/stim_mini_2016-11-14_periferia.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-09-14_periferia/';
% WN_time = '/home/cesar/exp/sync/2016-09-14_periferia/inicio_fin_frame_2016-09-14_periferia_CHECKERBOARD.txt';
% sta_start= 13;
% sta_end= 30;

% pathCell = '/home/cesar/exp/2016-09-30_centro/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-09-30_centro/stim_mini_2016-09-30_centro.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-09-30_centro/';
% WN_time = '/home/cesar/exp/sync/2016-09-30_centro/inicio_fin_frame_2016-09-30_centro_CHECKERBOARD.txt';
% sta_start= 13;
% sta_end= 30;

% pathCell = '/home/cesar/exp/2016-06-06_periferia_SD/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-06-06_periferia/stim_mini_2016-06-10.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-06-06_periferia/';
% WN_time = '/home/cesar/exp/sync/2016-06-06_periferia/inicio_fin_frame_2016-06-06_periferia_CHECKERBOARD.txt';
% sta_start= 1;
% sta_end= 18;

% pathCell = '/home/cesar/exp/2016-04-18_ret1_centro/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-04-11_periferia/stim_mini_stim_2016-04-11_periferia.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-04-18_centro/';
% WN_time = '/home/cesar/exp/sync/2016-04-18_centro/2016-04-18_ret1_centroinicio_fin_frame_2016-04-18_ret1_CHECKERBOARD.txt';
% sta_start= 1;
% sta_end= 18;
% 
% pathCell = '/home/cesar/exp/2016-04-11_ret1_periferia/';
% units = dir(pathCell);
% 
% pathStim = '/home/cesar/exp/sync/2016-04-11_periferia/stim_mini_stim_2016-04-11_periferia.mat';
% pathTimeStamp = '/home/cesar/exp/TS/2016-04-11_periferia/';
% WN_time = '/home/cesar/exp/sync/2016-04-11_periferia/inicio_fin_frame_2016-04-11_ret1_CHECKERBOARD.txt';
% sta_start= 1;
% sta_end= 18;

%% Format and read data
addpath('NIMtoolbox/')
dt=1.0/60.0;

% Loading and formatting stim_mini
stim = load(pathStim);
[nx,ny,~,nfr] = size(stim.stim);
tt = stim.stim(:,:,2,:);
stim=reshape(tt,nx,ny,nfr);
clear tt;
clear ny;
clear nx;

% Load bins of Checkerboard 
bins = load(WN_time);
spk_start = bins(1,1)/sr;
spk_end = bins(end,2)/sr;
bins = bins(:,1)/sr - spk_start;


%%
sinNL = [];
for k=3:length(units)
    if units(k).isdir
        cellId = units(k).name(1:end-7);
        fprintf('La unidad para analizar es %s\n',cellId)
        % Creating raster from spikelist
        spks=load([pathTimeStamp, cellId, '.txt']);
        spks_temp = spks(spks < spk_end) - spk_start;
        spks=spks_temp(spks_temp >0);
        fprintf('Unidad con %d spikes.\n',length(spks))
        if ~isempty(spks)
            % spk_stim get the number of spike in each stimuli
            spk_stim=histc(spks,bins);                      
            clear spks_temp;
            clear spks;
            % Loading STA data
            statemp = load([pathCell cellId '_lineal/' 'sta_array_' cellId '.mat']);
            STA_array = statemp.STA_array;
            STA_array = STA_array(:,:,sta_start:sta_end);

            % Creating cell data structure with STA data
            %STA_array = sta./norm(sta(:));
            clear statemp;

            % Reading Guassian fit data
            fit_data = load([pathCell cellId '_lineal/' 'fit_var.mat']);
            fitres = fit_data.fitresult;
            clear fit_data;

            % Ready to launch ComputeNLfromSTA code
            [nlData,fitparams] = ComputeNLfromSTA(stim,spk_stim,STA_array,fitres,round(dt*1000));
            save([pathCell cellId '_lineal/' 'NL.txt'],'fitparams','-ascii');
            save([pathCell cellId '_lineal/' 'NL.mat'],'nlData','-mat');
            PlotNLfromNIM_MJ(nlData,cellId,pathCell,'')
            clear spk_stim;
            clear STA_array;
            clear fitres;
        else
            sinNL = [sinNL;cellId];
        end
    end
end
