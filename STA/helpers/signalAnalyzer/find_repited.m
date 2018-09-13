mcdFile = '/home/cesar/exp/Chirp_data/2018-04-18/raw/2018-04-18_analogo.mcd';
EntityNumber = 1;

addpath('../../lib/NeuroShare/');
[nsresult] = ns_SetLibrary( '../../lib/NeuroShare/nsMCDLibrary.so' )

% % 
 [nsresult,info] = ns_GetLibraryInfo()
% % 
[nsresult, hfile] = ns_OpenFile(mcdFile)
[nsresult,info_file] = ns_GetFileInfo(hfile)

[nsresult,entity] = ns_GetEntityInfo(hfile,EntityNumber)
% % 
% [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
[nsresult,count,data] = ns_GetAnalogData(hfile,EntityNumber,1,entity.ItemCount); % Digital data

%%
txtfile = '/home/cesar/exp/Chirp_data/2018-04-18/sync/protocols_time/times/041.txt';
synctime = load(txtfile );
ampitude_data = zeros(length(synctime),1);
for k=1:length(synctime)
    amplitude_data(k) = mean(data(synctime(k)-20:synctime(k)));
end
diff_data = abs(diff(amplitude_data));
pos = find(diff_data<0.05);
disp(pos)
disp(synctime(pos))
plot(diff_data)

%%
plot(data(synctime(pos)-1000:synctime(pos)+1000))