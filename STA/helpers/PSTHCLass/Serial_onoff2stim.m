%% Generating .stim files for all folder+

folderName = 'C:\Users\Spike Degus\Desktop\DatosSTA\Spyking Circus';
cd (folderName);
fStruc = dir;
fid = [fStruc(:).isdir];
fNames = {fStruc(fid).name}';
fNames = fNames(3:end);
fNames=strcat(fNames,'\'); % adding the '\'.
nfolders = length(fNames); % number of folders
sr = 20000;
%%
for i = 1: nfolders
    cd(fNames{i});
    if sum(size(dir('*OffPulses.txt')))<=1
        continue
    end
    if i == 1 || i==2 || i ==3 % da los indices de los exps que usaron otro protocolo
        pre = 0.4;
        post = 0.4;
    else
        pre = 0.4;
        post = 1;
    end
    
    OffPulses2StimFile('.\', pre, post, sr)
    cd('..')
end
        