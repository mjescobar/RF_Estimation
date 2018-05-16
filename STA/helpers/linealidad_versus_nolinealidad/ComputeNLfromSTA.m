function [nlData,fit_params] = ComputeNLfromSTA(stim,spk_stim,STA_array,fitres,dt)
% [nlData] = ComputeNLfromSTA(stim,spk_stim,STA_array,fitres,mem,STAlen)

% Codigo Ruben Herzog, modificado por Maria Jose Escobar y César Reyes
% Computes the spiking nonlinearity using the STA as a linear filter. Uses
% Non-linear Input Model to estimate the Nonlinearity assuming a log-exp
% function. 

% Generating Variables for the fit
mod_signs = 1; % using 1 filter
NL_types = {'lin'}; % define filter as linear 
[STAblocks,~,STAlen]=size(STA_array);

% looking for the maximum semi-axis of ellipse to select a sub-area to compute NL
maxrad = max([fitres(3) fitres(4)]); % max(semi-a, semi-b)
centerRF = [fitres(5) fitres(6)]; % x0, y0

% Defining square region of 2*maxrad x 2*maxrad around the center of the RF
lims = [(centerRF(1)-maxrad) (centerRF(1)+maxrad) (centerRF(2)-maxrad) (centerRF(2)+maxrad)];
lims(lims<1)=1; % if some values are  less than 1 set to 1
lims(lims>STAblocks)=STAblocks; % if some values are greater than STAlen set to STAlen
lims = ceil(lims); % rounding high

% loads STA and stim regions selected.
sSTA = STA_array(lims(3):lims(4),lims(1):lims(2),:); 
sSTIM = stim(lims(3):lims(4),lims(1):lims(2),:);

% Adjust Stim for algorithm
[nx,ny,~] = size(sSTIM); % stim size without reshaping
sSTIM = permute(sSTIM, [3 1 2]);
sSTIM = (sSTIM -mean(sSTIM(:)))/max(sSTIM(:)); % setting mean of the region to zero

% flipping order of temporal filter to make the convolution and transfor 
% to vector the STA matrix
sSTA = sSTA(:,:,STAlen:-1:1); 
sSTA = permute(reshape(sSTA,nx*ny,STAlen),[2 1]); 
sSTA = reshape(sSTA, STAlen*nx*ny,1);

% Initilizing Fitting
% Stimulus is a T x M matrix T time stemps, M = nx*ny (spatialdims)
% Format data for fitting
% [nx,ny] = size(sSTIM);
% STAlen = length of STA
% dt = step of stimulus
params_stim = NIMcreate_stim_params( [STAlen nx ny], dt);
Xstim = create_time_embedding(sSTIM,params_stim); % stim in time embedding form

% fitting NL with STA as filter  
% fit0 = NIMinitialize_model( params_stim, mod_signs, NL_types,[], sSTA );% intilizes the NIM model 
fit0 = NIMinitialize_model( params_stim, mod_signs, NL_types,[]);% intilizes the NIM model 
fit0 = NIMfit_filters( fit0, spk_stim, Xstim, [], [], 1 );  

%%

% Data for plotting
fit_params = fit0.spk_NL_params;
[~, ~, ~, fit0.G] = NIMmodel_eval(fit0,spk_stim,Xstim);
fit0.G = fit0.G - fit0.spk_NL_params(1);
dist_bins = 200;
nonpar_bins = 100;
fit0.bin_edges = my_prctile(fit0.G,linspace(0.05,99.95,nonpar_bins));
fit0.bin_centers = 0.5*fit0.bin_edges(1:end-1) + 0.5*fit0.bin_edges(2:end);
[fit0.n,fit0.x] = hist(fit0.G,dist_bins);
fit0.nonpar = nan(nonpar_bins-1,1);
for j = 1:nonpar_bins-1
    cur_set = find(fit0.G >= fit0.bin_edges(j) & fit0.G < fit0.bin_edges(j+1));
    if ~isempty(cur_set)
        fit0.nonpar(j) = mean(spk_stim(cur_set));
    end
end    
fit0.pred = fit_params(3)*log(1 + exp(fit_params(2)*(fit0.bin_centers + fit_params(1))));
nlData = fit0;    