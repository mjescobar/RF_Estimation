function [nlData,fit_params] = ComputeNLfromSTA(data,STA_array,fitres,mem,pixs,dt)
% [nlData] = ComputeNLfromSTA(data,STA_array,fitres,mem,pixs)

% Computes the spiking nonlinearity using the STA as a linear filter. Uses
% Non-linear Input Model to estimate the Nonlinearity assuming a log-exp
% function. 
%nunits = length(STA_array); % Codigo Ruben
[nunits,~]=size(STA_array);
mod_signs = 1; % using 1 filter
NL_types = {'lin'}; % define filter as linear 
nlData = cell(1,nunits);
for i = 1: nunits
    
    % Generating Variables for the fit
    if sum(isempty(fitres(i)) | isnan(fitres{i}))~=0 % if is empty or if is nan continue with the next unit
        continue
    end
    maxrad = max([fitres{i}(3) fitres{i}(4)]); % looking for the maximum semi-axis of ellipse
    pars = [pixs-fitres{i}(5) fitres{i}(6)]; % x0, y0
    % Defining square region of 2*maxrad x 2*maxrad around the center of the RF
    lims = [(pars(1)-maxrad) (pars(1)+maxrad) (pars(2)-maxrad) (pars(2)+maxrad)];
    if isempty(find(lims <= 0, 1))==0; % if some values are negative set to 1
        lims(lims <= 0)=1;
    end
    if isempty(find(lims > pixs, 1))==0; % if some values are greater than pixs set to pixs
        lims(lims > pixs)=pixs;
    end
    
    lims = ceil(lims); % rounding high
    
    % -- Visualizing STA
    %tt = STA_array{2};
    %mintt = min(min(min(tt)))
    %maxtt = max(max(max(tt)))
    %tt = 255*(tt-mintt)/(maxtt-mintt);
    %for k=1:mem
    %    figure();
    %    imagesc(tt(:,:,k),[0 255]);
    %end
    % --
    
   
    STA = STA_array{i,2}(lims(3):lims(4),lims(1):lims(2),:); % loads STA and selects regions.
    
    % -- Visualizing cut STA
    %size(STA)
    %tt = STA;
    %tt = 255*(tt-mintt)/(maxtt-mintt);
    %for k=1:mem
    %    figure();
    %    imagesc(tt(:,:,k),[0 255]);
    %end
    % --
    
    stim = data.stim(lims(3):lims(4),lims(1):lims(2),:); % loads stim and selects same region backroung of stim
    [nx,ny,~] = size(stim); % stim size without reshaping
    %stim = reshape(stim,nx*ny,length(stim))'; % stimulus in 2D form
    stim = permute(stim, [3 1 2]);
    STA = STA(:,:,mem:-1:1); % flipping order of temporal filter for consistency
    STA = permute(reshape(STA,nx*ny,mem),[2 1]); 
    STA = reshape(STA, mem*nx*ny,1);
    stim = (stim/max(stim(:)) -mean(stim(:)/max(stim(:))))/2; % setting mean of the region to zero
    

    
    Robs = data.raster(i,:)';    
        
    % Initilizing Fitting
    % Stimulus is a T x M matrix T time stemps, M = nx*ny (spatialdims)
    % Format data for fitting
    %[nx,ny] = size(stim);
    params_stim = NIMcreate_stim_params( [mem nx ny], dt);
    Xstim = create_time_embedding(stim,params_stim); % stim in time embedding form
    
    % fitting NL with STA as filter  
    fit0 = NIMinitialize_model( params_stim, mod_signs, NL_types,[], STA );% intilizes the NIM model 
    disp(fit0)
    %disp(fit0.mods(imod).filtK)
    fit0 = NIMfit_filters( fit0, Robs, Xstim, [], [], 1 );  
    
    % Data for plotting
    fit_params = fit0.spk_NL_params;
    [~, ~, ~, fit0.G] = NIMmodel_eval(fit0,Robs,Xstim);
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
            fit0.nonpar(j) = mean(Robs(cur_set));
        end
    end    
    fit_params
    fit0.pred = fit_params(3)*log(1 + exp(fit_params(2)*(fit0.bin_centers + fit_params(1))));
    nlData{i} = fit0;    
    
end