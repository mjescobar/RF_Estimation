function [stim_ts_secs] = OnOffPulses(mcdfilepath,mcdfilename,in_stim,fin_stim,sr)

% Finds beginning of OFF pulses (no pulses on the analog signal) for the 
% signal on *.mcd file with path 'mcdfilepath' and name 'mcdfilename' in
% the interna [in_stim fin_stim].
%
% INPUTS
% mcdfilepath = path to mcd file. Ends with '/' or '\';
% mcdfilename = name of the file with extension
% in_stim = beginning of protocol in seconds
% fin_stim = end of protocol in seconds
% sr = sampling rate of the analog file
%
% OUTPUT
% stim_ts_sec = timestamps of OFF pulses in seconds.
% Generates a figure with the analog signal and the detected peaks.
%
%

% initilization
if isunix
    % Debiera ser parametro?
    addpath('../../lib/NeuroShare/');
    [nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDLibrary.so' )
elseif ispc
    libpath = which('nsMCDlibrary64.dll');
    [nsresult] = ns_SetLibrary( libpath );
    
end
channel = 1
mcdfile = [mcdfilepath,mcdfilename]; % full path and name to mcd file.
[nsresult,info] = ns_GetLibraryInfo()
[nsresult, hfile] = ns_OpenFile(mcdfile);
[nsresult,info]=ns_GetFileInfo(hfile);
[nsresult,entity] = ns_GetEntityInfo(hfile,channel);
[nsresult,analog] = ns_GetAnalogInfo(hfile,channel);
[nsresult,count,data]=ns_GetAnalogData(hfile,channel,1,entity.ItemCount);

% selecting only data from interval [in_stim fin_stim].
in_stim = ceil(in_stim*sr); % to time points
fin_stim = ceil(fin_stim*sr);

if fin_stim>length(data)% if fin_stim is larger than data
    data = data(in_stim:end); % selecting only the interval
else
    data = data(in_stim:fin_stim); % selecting only the interval
end


% finding last peak before absence of pulse
thresh = max(data)/3; % threshold to detect peaks
[~,locs] = findpeaks(data,'MinPeakHeight',thresh);

% taking the derivative of locs and finding the positions of the maximum
dlocs = diff(locs); % deerivatuve of the peak positions
ini = locs(diff(locs)>max(dlocs)/2); % position of OFF pulses
stim_ts = ini;
stim_ts(end+1)=locs(end); % adding the last pulse
stim_ts = stim_ts + in_stim; % correcting to original time
stim_ts_secs = (stim_ts/sr); % to seconds

% plotting and saving analog signal + detected peaks
figure;
plot(data);hold on; plot((stim_ts - in_stim), repmat(thresh,length(stim_ts)), 'ro');
saveas(gcf,[mcdfilepath,mcdfilename(1:end-4),'_OFF_peaks.jpg'],'jpg');
save([mcdfilepath,mcdfilename(1:end-4),'_OffPulses.txt'], 'stim_ts_secs', '-ascii');
%close(gcf);