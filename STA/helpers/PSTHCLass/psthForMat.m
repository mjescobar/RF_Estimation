function [psths,spikesperTrial,timebase] = psthForMat(spktimes, stimTs, pre, post, binsz,sr, pathToFile)
% Generates PSTH (spikes/s) for the spikes on the 'spktimes' cell array using stimTs
% as trigger (stimulus timestamp). Computes the PSTH with 'pre' ms before
% the trigger and 'post' ms after the trigger using a bin of size 'binsz'.
%
% INPUTS
% 'spktimes' cell array of 1 x nunits (or transpose) where each cell contains
% the units timestamps in timepoints.
% 'stimTs' is the timestamp of the stimulus
% 'pre' time before stimulus presentation for the psth [ms]
% 'post' time after stimulus presentation for the psth [ms]
% 'binsz' bin size of the psth [ms]
% 'sr' is the sampling rate of the recording
% 'pathToFile' path to file to analyze. Ends with '/' or '\'.
%
% OUTPUTS
% 'psths' is matrix of length(timebase) x nunits, where the columns are
% units and the rows the spike count in the corresponding bin of timebase.
% 'spikesperTrial' is a cell array with the same size than 'psths' where
% each cell is a length(stimTs) x 1 cell array with the time in bins of the 
% spikes respective to stimulus presentation
% 'timebase' is the time vector. i.e. the time of each bin.

%[psths,spikesperTrial] = cellfun(@(x) mpsth(x/sr,stimTs,'pre',pre, 'post', post,'tb',0, 'binsz', binsz), spktimes, 'uniformoutput', 0);
[psths,spikesperTrial] = cellfun(@(x) mpsth(x/sr,stimTs,'pre',pre, 'post', post,'fr',1,'tb',0, 'binsz', binsz), spktimes, 'uniformoutput', 0);
psths = cell2mat(psths); % cell array to matrix.
%psths = psths/(binsz/1000)/length(stimTs); %spikes/bin to spikes/second
timebase = (-1*pre:binsz:post-1); % time vector. bins.
save([pathToFile,'psths_spikesperTrial.mat'], 'psths', 'spikesperTrial','timebase'); % saving