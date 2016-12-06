% Computing Measures from the PSTH: Maximal Amplitude for the On and OFF
% pulse, its respective latencies and the bias index
% Assumes the psth was already computed (psths.mat) and is inside each folder
folderName = 'C:\Users\Spike Degus\Desktop\DatosSTA\Spyking Circus';
cd (folderName);
fStruc = dir;
fid = [fStruc(:).isdir];
fNames = {fStruc(fid).name}';
fNames = fNames(3:end);
fNames=strcat(fNames,'\'); % adding the '\'.
nfolders = length(fNames); % number of folders

% Global variables
psthAmp = cell(nfolders,1);
psthLatency = psthAmp;
BiasIdx = psthAmp;

for f=1:nfolders
    if f==2 || f==3 || f==4 || f==5 || f ==9 || f==10 || f==17
        continue
    end
    cd(fNames{f});
    disp(['Analyzing Experiment ',fNames{f}(1:end-1), '...']);
    
    [psthAmp{f}, psthLatency{f}] = PsthAmpLatency('./', fNames{f}(1:end-1));
    [BiasIdx{f}] = psthBiasIndex(psthAmp{f}, fNames{f}(1:end-1));
    psthBiasAmpLatencyScatter(psthAmp{f}, psthLatency{f}, BiasIdx{f}, fNames{f}(1:end-1));
    
    disp(['Experiment ',fNames{f}(1:end-1), ' Finished ! =D yahooo']);
    
    cd('..');
end

%% Computing conditions statistics

DJAmp = psthAmp{1};
DVAmp = cell2mat([psthAmp(6:8);psthAmp(11:12)]);
XFADAmp = cell2mat(psthAmp(13:16));
WTAmp = cell2mat(psthAmp(18:end));

DJLat = psthLatency{1};
DVLat = cell2mat([psthLatency(6:8);psthLatency(11:12)]);
XFADLat = cell2mat(psthLatency(13:16));
WTLat = cell2mat(psthLatency(18:end));

%% plotting
% degu joven
[DJBiasIdx] = psthBiasIndex(DJAmp, 'Young Degu');
psthBiasAmpLatencyScatter(DJAmp, DJLat, DJBiasIdx, 'Young Degu');

% degu viejo
[DVBiasIdx] = psthBiasIndex(DVAmp, 'Old Degu');
psthBiasAmpLatencyScatter(DVAmp, DVLat, DVBiasIdx, 'Old Degu');

% 5xfad
[XFADBiasIdx] = psthBiasIndex(XFADAmp, '5XFAD Mice');
psthBiasAmpLatencyScatter(XFADAmp, XFADLat, XFADBiasIdx,'5XFAD Mice');

% WT
[WTBiasIdx] = psthBiasIndex(WTAmp, 'WT Mice');
psthBiasAmpLatencyScatter(WTAmp, WTLat, WTBiasIdx, 'WT Mice');




