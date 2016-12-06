function [BiasIdx] = psthBiasIndex(psthAmp, fileName)
% computes the Bias Index (Carcieri et al. 2003) as (A1 – A2)/(A1 + A2),
% where A1 and A2 is the PSTH On and OFF maximal amplitude, respectively,
% with respect to the baseline.
% Plots a histogram of BiasIndexes
%
% INPUTS
%   
% 'psthAmp' is a 2-column vector, where in the columns are the ON and OFF
% maximal amplitued and in rows the neurons.
% 'fileName' is the name of the experiment to analyze
%
% OUPUTS
% 
% 'BiasIdx' is the bias index (A1 – A2)/(A1 + A2)

BiasIdx = (psthAmp(:,1) - psthAmp(:,2))./(psthAmp(:,1) + psthAmp(:,2));


% histogram
[bidxFreq, bidxC] = hist(BiasIdx, 30);
figure;
plot(bidxC,bidxFreq/sum(bidxFreq)*100, 'linewidth', 2)
xlabel('Bias Index');
ylabel('Percentage of All Cells (%)');
% Saving
print(gcf,'-djpeg', [fileName,'_Bias_Idx_Histogram.jpg']);
close(gcf);