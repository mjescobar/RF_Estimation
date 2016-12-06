function [selectedUnits] = selectUnitsAndSave(pathToFile, fileName, unitsSelected)

% Loads *.mat file with spiketimes, selects only those units of 'list' and
% then saves the file on the same folder with the same name but with
% '_selected' appended to the name.

% INPUTS
% 'pathToFile' is the path to the *.mat file with spiketimes with '/' or
% '\' at the end.
% 'fileName' is the name of the file with extension (*.mat or *.hdf5).
% 'list' is a list with the selected units

% OUTPUT
% selectedUnits is a cellarray with the selected units to save

% Cheking if file is *.mat of hdf5
[~,name, ext] = fileparts([pathToFile,fileName]);

if strcmp(ext,'.mat')
    
    aux = load([pathToFile,fileName,'.mat']); % loading spiketimes file
    f = fields(aux); % list of field of 'aux' structure
    spiketimes = aux.(f{1}); % 
elseif strcmp(ext,'.hdf5')
   spiketimes = loadTSfromHdf5(pathToFile,fileName,1); % loading spiketimes on spktimes cell array.
else
    errordlg('Wrong File Format')
   return;
end


selectedUnits = spiketimes(unitsSelected); % selecting only units on 'list'(in this case unitsSelected)
newname = [pathToFile,fileName,'_selected.mat']; % generating new name with full path
save(newname,'selectedUnits'); % saving on the same path of the original file

