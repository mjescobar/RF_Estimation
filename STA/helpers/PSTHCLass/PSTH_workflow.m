%% Script to extract the stimuluss time, compute the PSTH and classify cells
% according to their PSTH's.

%% Extractin stimulus Time
% extracts the time of OFF pulse
% 
% mcdfilepath = '/media/cesar/b366be05-7adf-4619-92ad-d57100e63487/2015-11-17/ret1_centro/MCD/'
% mcdfilename = '2015-11-17_ret1_centro_analogo.mcd'; % mcd file name with extension
% in_stim = 10*60+11+30*60+15.4; % beginning of protocol
% fin_stim = 10*60+11+30*60+15.4+2*60+4; % end of protocol

% mcdfilepath = '/media/cesar/experiments/2016-04-18/2016-04-18_ret1/raw/'
% mcdfilename = '2016-04-18_ret1_centro_analogo.mcd'; % mcd file name with extension
% in_stim = 2122; % beginning of protocol
% fin_stim = 2164; % end of protocol

%mcdfilepath = '/media/cesar/experiments/2016-06-06/raw/'
%mcdfilename = '2016-06-06_periferia.mcd'; % mcd file name with extension
%in_stim = 1428; % beginning of protocol
%fin_stim = 1469; % end of protocol

% mcdfilepath = '/media/cesar/experiments/2016-06-08/raw/'
% mcdfilename = '2016-06-08_centro.mcd'; % mcd file name with extension
% in_stim = 5959; % beginning of protocol
% fin_stim = 6004; % end of protocol

% mcdfilepath = '/media/cesar/experiments/2016-06-10/raw/'
% mcdfilename = '2016-06-10_periferia.mcd'; % mcd file name with extension
% in_stim = 197.84; % 197.84 | 4724 beginning of protocol
% fin_stim = 239.09; % 239.09 | 4766 end of protocol

% mcdfilepath = '/media/cesar/experiments/2016-04-11/raw/'
% mcdfilename = '2016-04-11_ret1_periferia.mcd'; % mcd file name with extension
% in_stim = 5*60+30*60+22; % beginning of protocol
% fin_stim = 5*60+30*60+22+46; % end of protocol

% mcdfilepath='/media/cesar/experiments/2016-06-08/raw/'
% mcdfilename='2016-06-08_ret1_centro.mcd'
% in_stim=1244;% 1244  5982
% fin_stim=1283;% 1283  6020
% 
% mcdfilepath='/home/cesar/exp/2016-06-17/raw/'
% mcdfilename='2016-06-17.mcd'
% in_stim= 1131;%934 984 1032 1080 1131 6267
% fin_stim= 1173;%976 1026 1075 1122 1173 6309
% 
% mcdfilepath = '/media/cesar/experiments/2016-09-30/raw/'
% mcdfilename = '2016-09-30_centro_analogo.mcd'; % mcd file name with extension
% in_stim = 118959972/20000; % beginning of protocol 12549287 . 16338534 118969972
% fin_stim = 119764912/20000; % end of protocol 13382899 . 17161590 119764912

%mcdfilepath = '/media/cesar/experiments/2016-10-28/raw/'
%mcdfilename = 'Analoga Degu_centro_28_10_2016.mcd'; % mcd file name with extension
%in_stim = 126043537/20000; % beginning of protocol 22300862
%fin_stim = 126850361/20000; % end of protocol 23171802

% mcdfilepath = '/media/cesar/experiments/2016-11-08/raw/'
% mcdfilename = 'Degu_11_08_2016_analogo.mcd'; % mcd file name with extension
% in_stim = 16300133/20000; % beginning of protocol 16307133, 152896858
% fin_stim = 17145072/20000; % end of protocol 17102072, 153739351

mcdfilepath = '/home/cesar/exp/2016-11-14_periferia/raw/'
mcdfilename = '2016-11-14_periferia_analogo.mcd'; % mcd file name with extension
in_stim = 21437771/20000; % beginning of protocol 21467771 22397664 - 125959242
fin_stim = 22302711/20000; % end of protocol 22262711 23252604 - 125959242



sr = 20000; % sampling rate
[stimTS] = OnOffPulses(mcdfilepath,mcdfilename,in_stim,fin_stim,sr);

%% Computing the psth in spikes / s FOR *.mat FILE
% fileName = 'Degu Viejo N3j t2.spiketimes1';
% pre = 400; % time before stimulus in ms
% post = 400; % time after stimulus in ms
% binsz = 5; % psth bin size in ms
% spktimes = load([fileName,'.mat']); % loading spiketimes on spktimes structure
% f = fields(spktimes); % gets the fields of the structure
% spktimes = spktimes.(f{1}); % takes only the spiketimes
% [psths,spikesperTrial,timebase] = psthForMat(spktimes, stimTS, pre, post, binsz,sr,'./');


%% Computing the psth in spikes / s FOR *.txt FILE
% filePath = '/media/cesar/experiments/2016-04-11/ret1_periferia/sorting/2016-04-11_ret1_periferia/TS_merge/';
% fileName = '2016-04-11_ret1_periferia'
% TSfile =  dir(filePath);
% TSfile(1:2) =[]; 
% %spktimes = cell(1,length(TSfile)-2);
% 
% for k=1:length(TSfile)
%     spktimes{str2num(TSfile(k).name(6:end-4))} = importdata(strcat(filePath,TSfile(k).name))*sr;
%     id_valido{str2num(TSfile(k).name(6:end-4))} = 1;
% end   
% for k = 1:length(id_valido)
%     if id_valido{k} == 1
%     else
%         id_valido{k}=0
%     end
% end
% id_validoArray = cell2mat(id_valido)
% pre = 400; % time before stimulus in ms
% post = 1000; % time after stimulus in ms
% binsz = 5; % psth bin size in ms
% [psths,spikesperTrial,timebase] = psthForMat(spktimes, stimTS, pre, post, binsz,sr,filePath);


%% Computing the psth in spikes / s FOR *.HDF5 FILE

% Comentado mientras no se ocupe.
% filePath = '/media/cesar/19b0ef23-21f8-4369-86a0-87721fc349aa/2016-05-05/ret2/2016-05-05_ret2_periferia/';
% fileName = '2016-05-05_ret2_periferia.result.hdf5'

% filePath = '/media/cesar/19b0ef23-21f8-4369-86a0-87721fc349aa/2016-05-05/ret1/2016-05-05_ret1_centro/';
% fileName = '2016-05-05_ret1_centro.result.hdf5'
% filePath = '/media/cesar/19b0ef23-21f8-4369-86a0-87721fc349aa/2016-04-29/ret1/Degu_2016-04-29_Trozo_1/';
% fileName = 'Degu_2016-04-29_Trozo_1.result.hdf5'

% filePath = '/media/cesar/b366be05-7adf-4619-92ad-d57100e63487/2016-04-11/ret1_periferia/2016-04-11_ret1_periferia/'
% fileName = '2016-04-11_ret1_periferia.result.hdf5'
% filePath = '/media/cesar/experiments/2016-06-02/sorting/2016-06-02_ret1_centro/'
% fileName = '2016-06-02_ret1_centro.result.hdf5'
% filePath = '/home/cesar/exp/2016-06-17/sorting/2016-06-17/'
% fileName = '2016-06-17.result3.hdf5'
% filePath = '/media/cesar/experiments/2016-04-18/2016-04-18_ret1/sorting/2016-04-18_ret1_centro/'
% fileName = '2016-04-18_ret1_centro.result2.hdf5'
% filePath = '/media/cesar/experiments/2016-06-06/sorting/2016-06-06_periferia/'
% fileName = '2016-06-06_periferia.result1.hdf5'
% filePath = '/media/cesar/experiments/2016-09-30/sorting/2016-09-30_centro/'
% fileName = '2016-09-30_centro.result-3.hdf5'

% pathflash = '/media/cesar/experiments/2016-09-30/sorting/Flash/'
% filePath = '/media/cesar/experiments/2016-10-28/Degu_centro_28_10_2016/'
% fileName = 'Degu_centro_28_10_2016.result.hdf5'

% pathflash = '/media/cesar/experiments/2016-11-08/sorting/Flash/'
% filePath = '/media/cesar/experiments/2016-11-08/sorting/Degu_11_08_2016/'
% fileName = 'Degu_11_08_2016.result.hdf5'

pathflash = '/home/cesar/exp/2016-11-14_periferia/sorting/'
filePath = '/home/cesar/exp/2016-11-14_periferia/sorting/2016-11-14_periferia/'
fileName = '2016-11-14_periferia.result.hdf5'


pathsave = [pathflash, 'Flash/']
mkdir(pathsave)

pre = 400; % time before stimulus in ms
post = 1000; % time after stimulus in ms
binsz = 5; % psth bin size in ms
spktimes = loadTSfromHdf5(filePath,fileName,1); % loading spiketimes on spktimes cell array.
[psths,spikesperTrial,timebase] = psthForMat(spktimes, stimTS, pre, post, binsz,sr,pathsave);
% for k = 1:length(spktimes)
%     id_valido{k} == 1
% end
% id_validoArray = cell2mat(id_valido)


%% Selection PSTH's according to their reliability
% This will generate the list of Selected units that we can use for any
% analysis.
ccThr = 0.3; % threshold for correlation coeficient
ntrials = 0.5; % 50% of the pairs of trials are correlatad above ccThr
[psthSelection] = psthFilter(spikesperTrial,timebase, ccThr, ntrials, pathsave);

%% Saving a new *.mat with the selected units.
[selectedUnits] = selectUnitsAndSave(pathsave, fileName, psthSelection);
% This new *.mat will be the one that we will use for STA and for the other
% analysis.
%% Classifying the PSTHS using threshold computed from the psth's data

Onini = -pre; % beginning of ON pulse in ms relative to stimulus presentation
Offini = 0; % beginning of ON pulse  in ms relative to stimulus presentation
sdfac = 1.5; % factor to set the threshold for classification
%psthClasses = psthOnOffClassifier(psths,Onini,Offini,sdfac,timebase);
%mkdir('Raw Psth'); % creating folder for the Raw Psths.
%cd('./Raw Psth'); 
%psthClassesRaw = psthOnOffClassifier(psths,Onini,Offini,sdfac,timebase);
%cd('..');
%mkdir('Selected PSTH');
%cd('./Selected PSTH'); 
% using only selected psths to the classification.
% psthClasses = psthOnOffClassifier(psths,Onini,Offini,sdfac,timebase,filePath,id_validoArray');
psthClasses = psthOnOffClassifier(psths,Onini,Offini,sdfac,timebase,pathflash);
%cd('..');

%%
pathsave = [pathflash, 'PSTH/']
mkdir(pathsave)
for indice = 1:length(psths)
    arreglo = zeros(30,1500);
    arreglo(:,1:400)=1;
    figure('visible', 'off');
    subplot(2,1,1);
    for i = 1:29
        a = spikesperTrial{indice}{i};
        for c = a
            
            if c < 0
                arreglo(i,c+401)=2;
            else
                arreglo(i,c+401)=2;
            end
        end 
    end
    imagesc(arreglo);

    subplot(2,1,2)
    plot(timebase,psths(:,indice),'r');
    title(['Unit ',num2str(indice-1)]);
    print(gcf,'-djpeg', [pathsave 'temp' num2str(indice-1) '.jpeg']);
    close all
end