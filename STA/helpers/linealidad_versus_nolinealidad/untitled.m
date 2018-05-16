figure()
for k=1:18
    subplot(3,6,k)
    pcolor(STA_array(:,:,k))
%     pcolor(sSTA(:,:,k))
%     pcolor(reshape(aa(k,:,:),4,4))
%     caxis([-.014 -0.00364])
end
%%
figure()
temp = reshape(nlData.mods.filtK,18,32);
for k=1:18
    subplot(3,6,k)
    
    imagesc(reshape(temp(k,:),8,4))
    caxis([-.2 0.2])
end
%%
aa = reshape(fit0.mods.filtK,18,20);
% aa = reshape(nlData{1}.mods.filtK,20,16);
% aa = reshape(nlData{1}.mods.filtK,18,32);
% aa = permute(aa,[2,3,1]);
figure()
imagesc(aa)

%%
% sSTA = reshape(STA_array(ceil(centerRF(2)),ceil(centerRF(1)),:),18,1);
sSTA = reshape(STA_array(13,3,:),18,1);
sSTIM = reshape(data.stim(13,3,:),108000,1);
%sSTIM = sSTIM - mean(sSTIM(:));
stim_dt = 0.016666;
% Format data for fitting
nLags = 20; % number of time lags for estimating stimulus filters
up_samp_fac = 1; % temporal up-sampling factor applied to stimulus 
tent_basis_spacing = 1; % represent stimulus filters using tent-bases with this spacing (in up-sampled time units)
params_stim = NIMcreate_stim_params( nLags, stim_dt, up_samp_fac, tent_basis_spacing );

% Create T x nLags 'Xmatrix' representing the relevant stimulus history at each time point
Xstim = create_time_embedding( sSTIM, params_stim ); 

% Bin spikes at analysis resolution
Robs = histc(spks,(0:(size(Xstim,1)-1))*params_stim.dt); % Prob w conventions

% Create and fit a (regularized) GLM (single linear filter LN model)
mod_signs = [1]; % determines whether input is exc or sup (doesn't matter in the linear case)
NL_types = {'lin'}; % define subunit as linear 

% Create regularization parameter structure (in this case we're only using a
% smoothness penalty in time (2nd deriv with respect to the time)
params_reg = NIMcreate_reg_params( 'lambda_d2T', 200 ); 
silent = 0; % set to 1 if you want to suppress the optimization display

% Initialize NIM (use 'help NIMinitialize_model' for more details about the 
% model struct components).
fit0 = NIMinitialize_model( params_stim, mod_signs, NL_types, params_reg ); 

% Fit stimulus filters
fit0 = NIMfit_filters( fit0, Robs, Xstim, [], [], silent ); 

% Display linear filter (first one) -- SHOULD WE BE USING "MODS"
filtfig = figure;
plot(fit0.mods(1).filtK,'k');

%%

zz = Xstim.*Robs;
za = zz(Robs>0,:);
mean(za,2)
mean(za,1)
plot(mean(za,1))

%%
temp = zeros(35,35,18);
index = find(raster);
index = index(index>18);
data.stim=data.stim;
for k=1:length(index)
    temp=temp+data.stim(:,:,index(k)-17:index(k))*raster(index(k));
end
% temp = temp./sum(Robs);
figure()
for k=1:18
    subplot(3,6,k)
    pcolor(temp(:,:,k))
end