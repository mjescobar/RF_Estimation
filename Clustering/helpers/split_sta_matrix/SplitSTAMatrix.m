function SplitSTAMatrix ( STA_File, outputFolder)
% ------------------------------------------------------------
% Takes the STA matrix and splits it in different subfolders. Useful to use
% Neuroexplorer Reverse Correlation results
% ------------------------------------------------------------
% Monica Otero 2014
% ------------------------------------------------------------
load (STA_File,'-mat');
nunits = size(STA_fxf_norm,1);
units_name=STA_fxf_norm{:,1};
%disp (units_name);
nframes = size(STA_fxf_norm{1,2},3);

for i=1:nunits
    unitname=STA_fxf_norm{i,1};
    name=[unitname,'_lineal'];
    mkdir(outputFolder,name);
   for f=1:nframes
        STA_array(:,:,f) = STA_fxf_norm{i,2}(:,:,f); 
        
   end
    carpeta = [outputFolder,'/',unitname,'_lineal','/', 'sta_array_',unitname,];
    save ([carpeta, '.mat'],'STA_array');

end

