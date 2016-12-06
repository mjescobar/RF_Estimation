function [psthAmp, psthLatency] = PsthAmpLatency(pathToFile, fileName)
% Generates two 2-column arrays of length equal to the number of neurons. Each
% vector contains the maximal amplitude of the ON and OFF part and the
% latencies to the max values, respectively.
% Assumes that the PSTH was already computed and that the psths.mat structure
% exists on the 'pathToFile' folder. Assumes also that the ON pulse comes
% before the OFF pulse. Assumes OFF as t = 0.
%
% INPUT
% 'pathToFile' is the path to the folder with psths.mat. Ends with '/' or
% '\'.
% 'fileName' is the name of the experiment to analyze
%
% OUTPUTS
% 'psthAmp' is a two column vector with the maximal amplitude of the psth
% on the ON and the OFF part, respectively, with respect to the baseline
% defined as the mean firing rate on the last 150ms of each stimulus.
% 'psthLatency' is the same than psthAmp, but with the latencies to the
% maximal peak on each parte of the stimulus.

% loading psths.mat
load([pathToFile,'psths.mat']);

% variables
psthAmp = zeros(size(psths,2),2);
psthLatency = psthAmp;
idx0 = find(timebase==0); % index of the 0 in psth
minT = min(timebase); %  minimal time in psth
dt = timebase(2)- timebase(1); % bin of timebase

% computing the baselines as the last 100ms firing rate for each part
[baseOn] = mean(psths(timebase<0 & timebase>-150,:)); % ON pulse
[baseOff] = mean(psths(timebase>timebase(end-150/dt),:)); % OFF pulse

% splitting psth on On and OFF part.
[psthAmp(:,1), psthLatency(:,1)] = max(psths(timebase<0,:)); % ON pulse
[psthAmp(:,2), psthLatency(:,2)] = max(psths(timebase>0,:)); % OFF pulse

 psthAmp(:,1) = psthAmp(:,1) - baseOn';
 psthAmp(:,2) = psthAmp(:,2) - baseOff';
% indexes to psth bins
psthLatency(:,1) = -minT + timebase(psthLatency(:,1));
psthLatency(:,2) = timebase(psthLatency(:,2)+idx0);

% histogram
[OnampH, OnampC] = hist(psthAmp(:,1),30);
[OffampH, OffampC] = hist(psthAmp(:,2),30);
[OnLatH, OnLatC] = hist(psthLatency(:,1),30);
[OffLatH, OffLatC] = hist(psthLatency(:,2),30);

figure;
% Plotting amplitudes
subplot(2,2,1)
plot(OnampC,OnampH/sum(OnampH)*100, 'color', 'r', 'linewidth', 2);hold on
plot(OffampC,OffampH/sum(OffampH)*100, 'color', 'b', 'linewidth', 2); hold on
title ('PSTH Peak')
xlabel('Maximal PSTH Amplitude (Hz)');
ylabel('Percentage of All Cells (%)');
legend('ON Pulse', 'OFF Pulse')

% Plotting latencies
subplot(2,2,2)
plot(OnLatC,OnLatH/sum(OnLatH)*100, 'color', 'r', 'linewidth', 2);hold on
plot(OffLatC,OffLatH/sum(OffLatH)*100, 'color', 'b', 'linewidth', 2); hold on;
title ('Latency to PSTH Peak')
xlabel('Latency to PSTH Peak (ms)');
ylabel('Percentage of All Cells (%)');

% Plotting Latencyes vs Peak scatter
% On Pulse
subplot(2,2,3)
plot(psthAmp(:,1),psthLatency(:,1), 'ro');hold on
title ('Latency vs ON PSTH Peak')
ylabel('Latency to PSTH Peak (ms)');
xlabel('Maximal PSTH Amplitude (Hz)');

% Off pulse
subplot(2,2,4)
plot(psthAmp(:,2),psthLatency(:,2), 'bo');hold on
title ('Latency vs OFF PSTH Peak')
ylabel('Latency to PSTH Peak (ms)');
xlabel('Maximal PSTH Amplitude (Hz)');


% Saving
print(gcf,'-djpeg', [fileName,'_PSTH_Peak_Latencies.jpg']);
close(gcf);



