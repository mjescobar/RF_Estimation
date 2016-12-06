function psthBiasAmpLatencyScatter(psthAmp, psthLatency, BiasIdx, fileName)
% Plots a 2 x 2 figure with scatter plots of BiasIdx vs psthAmp and vs
% psthLatency
%
% INPUTS
% 'psthAmp' is a two column vector with the maximal amplitude of the psth
% on the ON and the OFF part, respectively
% 'psthLatency' is the same than psthAmp, but with the latencies to the
% maximal peak on each parte of the stimulus.
% 'BiasIdx' is the bias index (A1 – A2)/(A1 + A2)
% 'fileName' is the name of the experiment to analyze

% BiasIdx vs ON Amp
subplot(2,2,1)
plot(BiasIdx, psthAmp(:,1), 'ro');hold on;
plot(BiasIdx, psthAmp(:,2), 'bo');hold on;
xlabel('Bias Index (AU)');
ylabel('Maximal PSTH Amplitude (Hz)');
legend('ON Pulse', 'OFF Pulse');

% BiasIdx vs ON Amp
subplot(2,2,2)
plot(BiasIdx, psthLatency(:,1), 'ro');hold on;
plot(BiasIdx, psthLatency(:,2), 'bo');hold on;
xlabel('Bias Index (AU)');
ylabel('Latency to PSTH Peak (ms)');

% BiasIdx vs ON Amp
subplot(2,2,3:4)
plot3(BiasIdx,psthAmp(:,1),psthLatency(:,1), 'ro');hold on;
plot3(BiasIdx,psthAmp(:,2), psthLatency(:,2), 'bo');hold on;
xlabel('Bias Index (AU)');
ylabel('Maximal PSTH Amplitude (Hz)');
zlabel('Latency to PSTH Peak (ms)');

% Saving
print(gcf,'-djpeg', [fileName,'_PSTH_BiasIdx_Amp_Latency.jpg']);
close(gcf);
