function [psthSelection] = psthFilter(spikesperTrial,timebase, ccThr, ntrials, pathToFile)
% Selects neurons whose PSTH has at least 'ntrials' with a Pearson
% cross-correlation index bigger or equal to 'ccThr'.
%
% INPUTS
% 'psths' is matrix of length(timebase) x nunits, where the columns are
% units and the rows the spike count in the corresponding bin of timebase.
% 'spikesperTrial' is a cell array with the same size than 'psths' where
% each cell is a length(stimTs) x 1 cell array with the time in bins of the 
% spikes respective to stimulus presentation
% 'timebase' is the time vector. i.e. the time of each bin.
% 'ccThr' scalar between 0 and 1 setting the minimal Pearson
% cross-correlation index between trials to be considered
% 'ntrials' a scalar between 0 and 1. Is the min number of pair of trials
% that have correlations above or eaqual to 'ccThr';
% 'pathToFile' path to file to analyze. Ends with '/' or '\'.
%
% OUTPUTS
% 'psthSelection' is a list with the selected units.

nunits = length(spikesperTrial);
list = (1:nunits)';
idx = zeros(nunits,1);


for i = 1: nunits
    spikes = cellfun(@(x) histc(x, timebase), spikesperTrial{i}, 'uniformoutput', 0); % computing the spikes for each trial
    spikes = cellfun(@(x) x(:), spikes,'UniformOutput',0);
    disp(i)
    spikes = cat(2,spikes{:}); % converting cell array to matrix
    cc = nonzeros(triu(corrcoef(spikes),1)); % computing the cross correlation between all trials and keeping only the upper matrix as vector.
    cc(cc>=ccThr) = 1; % 1 if satifyies condition
    cc(cc<ccThr) = 0; % setting to 0 if is lower than threshold
    
    if sum(cc)/length(cc) >= ntrials/length(cc)
        idx(i) = 1; % if nauron satifyies the condition
    else
        idx(i) = 0; % if it doesnt
    end
end
psthSelection = list(idx==1);
save([pathToFile(1:end-1),'_PSTH_selection.txt'], 'psthSelection', '-ascii');
    

