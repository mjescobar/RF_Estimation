%function psthClasses = psthOnOffClassifier(psths,Onini,Offini,sdfac,timebase, pathToFile,idValido)
function psthClasses = psthOnOffClassifier(psths,Onini,Offini,sdfac,timebase, pathToFile)
% Classifies units as ON, OFF or ON-OFF according to their psth. Uses
% sdfac*std + mean of the psth as threshold for detecting responses to the
% ON or OFF stimulus.
%
% INPUTS
% 'psths' length(timebase) x nunits matrix with psths. Output of psthForMat.m function
% 'Onini' beginning of On pulse in ms
% 'Offini' beginning of Off pulse in ms
% 'sdfac' is a factor that multiplies the std to get a threshold
% 'timebase' is the time vector of the psth. Output of psthForMat.m
% 'pathToFile' is the path for the file to analyze. Ends with '/' or'\'.
%
% OUTPUT
% 'psthClasses' is a 1 x length(psths) vector where 1 is for ON, 2 for OFF
% and 3 for ON-OFF and 0 if doesn't satifies the conditions.
% Generates and saves a figure with the ON, OFF, ON-OFF and null
% population. Saves the figure on the working folder. Also generates
% figures with each cell independently.
%pathToFile =filePath

nunits = size(psths,2); % number of units
nombres = {'Null','ON', 'OFF','ON-OFF','THRESH' };

if Onini < Offini % ON pulse comes before OFF
    
    onidx = 1; % OB starts on the first bin
    offidx = find(timebase==Offini); % index of OFF pulse beginning.
    
    % splitting in ON and OFF part
    onpsth = psths(onidx:offidx-1,:);
    offpsth = psths(offidx:end,:);

else % OFF pulse comes before ON
    onidx = find(timebase==Onini); % index of ON pulse beginning.
    offidx = 1; % index of OFF pulse beginning.
    
    % splitting in ON and OFF part
    offpsth = psths(offidx:onidx-1,:);
    onpsth = psths(onidx:end,:);
end

ps = psths;
ps(ps==0)=NaN;
frate = nanmean(ps); % firing rate of each unit
%frate = mean(psths); % firing rate of each unit
sdpsth = nanstd(ps,[],1);
%sdpsth = std(psths); % std of each unit
maxpsthall = max(psths);
umbral = frate + sdfac*sdpsth; % threshold
onmaxval = max(onpsth); % max value on ON interval for each unit
offmaxval = max(offpsth); % max value on OFF interval for each unit

onunits = onmaxval > umbral; % ON units exceeding the threshold
offunits = offmaxval > umbral; % OFF units exceeding the threshold
validunits = maxpsthall > 20;
joint = [onunits; offunits;validunits;]; % don't smoke this

% Asigning cell classes null = 0, ON = 1, OFF = 2, ON-OFF = 3, threh = 4
tipos = zeros(1,nunits);

for i =1:nunits
    if joint(1,i)==0 && joint(2,i)==0 && joint(3,i)==0% doesn't satify criteria
        tipos(i) = 0;
    
    elseif joint(1,i)==1 && joint(2,i)==1 && joint(3,i)==1 % ON/OFF
        tipos(i) = 3; % unit exceeds threnshold on both pulses
        
    elseif joint(1,i)==1 && joint(2,i)==0 && joint(3,i)==1% ON
        tipos(i) = 1; % unit exceeds threnshold only on ON pulse
        
    elseif joint(1,i)==0 && joint(2,i)==1 && joint(3,i)==1% OFF
        tipos(i) = 2; % unit exceeds threnshold only on ON pulse
    elseif (joint(1,i)==1 || joint(2,i)==1) && joint(3,i)==0% OFF
        tipos(i) = 4; % unit exceeds threnshold only on ON pulse
    end
end

psthClasses = tipos';


% plotting summary figure (all cells together by type)
figure;
for i =1:5
    
    subplot(2,3,i)
    if isempty(psths(:,tipos==(i-1)))
        continue
    end
    
    
    if Onini < Offini % ON pulse comes before OFF
        if max(max(psths(:,tipos==(i-1))))~=0
%             h=area([timebase(offidx) timebase(end)], [max(psths(:)) max(max(psths(:,tipos==(i-1))))], 'facecolor', [0.9 0.9 0.9]); hold on
            h=area([timebase(offidx) timebase(end)], [max(psths(:)) max(psths(:))], 'facecolor', [0.9 0.9 0.9]); hold on
            ylim([0 max(max(psths(:,tipos==(i-1))))]);
            child=get(h,'Children');
            set(child,'FaceAlpha',0.5);
        end
        
    else
        h=area([timebase(offidx) timebase(onidx-1)], [max(psths(:)) max(max(psths(:,tipos==(i-1))))], 'color', [0.9 0.9 0.9]); hold on
        child=get(h,'Children');
        set(child,'FaceAlpha',0.5);
    end
    xlim([timebase(1) timebase(end)]);
    ylim([0 max(psths(:))]);
    %plot(timebase,psths(:,(tipos==(i-1) & idValido==1)));
    plot(timebase,psths(:,(tipos==(i-1))));
    hold on
    %title([num2str(sum((tipos==(i-1) & idValido==1))),' ',nombres{i}]);
    title([num2str(sum((tipos==(i-1)))),' ',nombres{i}]);
    
xlabel('Time Relative to Stimulus (ms)');
ylabel('Spikes/bin');
end

%saveas(gcf,[pathToFile(1:end-1),'_PSTH_OnOFF_Clustering.jpg'],'jpg');
%saveas(gcf,[pathToFile(1:end-1),'_PSTH_OnOFF_Clustering.pdf'],'pdf');
saveas(gcf,[pathToFile,'PSTH_OnOFF_Clustering.jpg'],'jpg');
saveas(gcf,[pathToFile,'PSTH_OnOFF_Clustering.pdf'],'pdf');


%% Gŕafica y guarda 4 clases en plots de 6x6


for tip =1:5
    
    ntip = length(find(tipos==tip-1));
    cont =0;
    if ntip>36
        while cont<=ntip
            figure('visible', 'off', 'paperunits', 'points','paperposition',[0 0 800 600]);
            for i =1:36
                if i+cont>ntip
                    break
                end
                idx_class = find(tipos==tip-1);
                subplot(6,6,i);

                
                if Onini < Offini % ON pulse comes before OFF
                    %if max(max(psths(:,tipos==(i-1))))~=0
                        h=area([timebase(offidx) timebase(end)], [max(psths(:,idx_class(i+cont))) max(psths(:,idx_class(i+cont)))], 'facecolor', [0.9 0.9 0.9]); hold on
                        %ylim([0 max(psths(:,idx_class(i+cont)))]);
                        child=get(h,'Children');
                        set(child,'FaceAlpha',0.5);
                    %end
                    
                else
                    h=area([timebase(offidx) timebase(onidx-1)], [max(psths(:,idx_class(i+cont))) max(psths(:,idx_class(i+cont)))], 'color', [0.9 0.9 0.9]); hold on
                    child=get(h,'Children');
                    set(child,'FaceAlpha',0.5);
                end
                
                plot(timebase,psths(:,idx_class(i+cont)),'r');
                hold on
                line([timebase(1) timebase(end)],[umbral(idx_class(i+cont)) umbral(idx_class(i+cont))],'color','k');hold on;
                title(['Unit ',num2str(idx_class(i+cont)-1)]);
                xlim([timebase(1) timebase(end)]);
                
                if sum(ismember([31:36], i)) ==0
                    set(gca, 'xtick', []);
                else
                    set(gca,'xtick', [timebase(1) 0 timebase(end)], 'fontsize', 10);
                end
                
            end
            cont = cont+36;
            %print(gcf,'-djpeg', [pathToFile(1:end-1) nombres{tip},num2str(cont/36) '.jpg']);
            print(gcf,'-djpeg', [pathToFile nombres{tip},num2str(cont/36) '.jpg']);
            close all
        end
        
    else
        figure('visible', 'off', 'paperunits', 'points','paperposition',[0 0 800 600]);
        for i =1:ntip
            idx_class = find(tipos==tip-1);
            subplot(6,6,i);

            
            if Onini < Offini % ON pulse comes before OFF
                %if max(max(psths(:,tipos==(i-1))))~=0
                    h=area([timebase(offidx) timebase(end)], [max(psths(:,idx_class(i))) max(psths(:,idx_class(i)))], 'facecolor', [0.9 0.9 0.9]); hold on
                    if max(psths(:,idx_class(i))) == 0
                        ylim([0 1]);
                    else
                        ylim([0 max(psths(:,idx_class(i)))]);
                    end
                    child=get(h,'Children');
                    set(child,'FaceAlpha',0.5);
                %end
                
            else
                h=area([timebase(offidx) timebase(onidx-1)], [max(psths(:,idx_class(i))) max(psths(:,idx_class(i)))], 'color', [0.9 0.9 0.9]); hold on
                child=get(h,'Children');
                set(child,'FaceAlpha',0.5);
            end
            
            plot(timebase,psths(:,idx_class(i)),'r'); 
            hold on
            %plot(timebase,umbral(idx_class(i)),'k');hold on;
            line([timebase(1) timebase(end)],[umbral(idx_class(i+cont)) umbral(idx_class(i+cont))],'color','k');hold on;
            title(['Unit ',num2str(idx_class(i)-1)]);
            xlim([timebase(1) timebase(end)]);
            
            if sum(ismember([31:36], i)) ==0
                set(gca, 'xtick', []);
            else
                set(gca,'xtick', [timebase(1) 0 timebase(end)], 'fontsize', 10);
            end
        end
        %print(gcf,'-djpeg', [pathToFile(1:end-1) nombres{tip} '.jpeg']);
        print(gcf,'-djpeg', [pathToFile nombres{tip} '.jpeg']);
        close all
    end
    
end

% nameTemp = []
% for k=1:length(psthClasses)
%     nameTemp(k,:) = strcat('temp',num2str(k-1,'%04d'));
% end

% save([pathToFile(1:end-1),'_PSTH_OnOffList.txt'],'psthClasses', '-ascii');
% save([pathToFile(1:end-1),'_psthClustering.mat'],'psthClasses');
save([pathToFile,'PSTH_OnOffList.txt'],'psthClasses', '-ascii');
save([pathToFile,'psthClustering.mat'],'psthClasses');
