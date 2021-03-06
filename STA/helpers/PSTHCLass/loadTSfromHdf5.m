function [ts] = loadTSfromHdf5(pathName,fileName,cellOp)
% Load timestamps on ts matrix of N x max(num_ts)
%
% INPUTS
% pathName = path to the folder where the hdf5 file is. Ends with '/' or
% '\'.
% fileName = name of the file to load with extension
% cellOp = logic operator for cell array or matrix. If cellOp = 0, then
% generates a matrix. Otherwise, it generates a cellarray of 1 x nunits.
%
% OUTPUT
% ts = max(num_ts) x N matrix where in rows are the neurons and on columns
% the timestamps.

% Getting the hdf5 info
fileinfo = h5info([pathName,fileName]);

nunits = length(fileinfo.Groups(2).Datasets); % getting the number of units
tsarray = cell(1,nunits);
for i=1:nunits
    unt = strsplit(fileinfo.Groups(2).Datasets(i).Name,'_');
    tsarray{1+str2num(cell2mat(unt(2)))}= double(h5read([pathName,fileName],['/spiketimes/',fileinfo.Groups(2).Datasets(i).Name])');  

end

if cellOp~=0 % if user asked for cellarray
    ts = tsarray;
else
    maxSize = max(cellfun(@numel,tsarray));
    fcn = @(x) [x zeros(1,maxSize-numel(x))];  %# Create an anonymous function
    rmat = cellfun(fcn,tsarray,'UniformOutput',false);
    ts = vertcat(rmat{:})' ;
end
