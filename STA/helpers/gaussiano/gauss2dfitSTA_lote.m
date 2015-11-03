function gauss2dfitSTA_lote(folder)
 
  subfolder=dir([folder,'\*lineal']);
  subfolder=struct2table(subfolder);
  cell_fullname=subfolder(:,1).name;
  strcell=char(cell_fullname);
  subfolder=strcat(folder,{'\'},cell_fullname);
  cell_name = cell(length(strcell),1);
  for k = 1:length(strcell)
      i=1;
      str_cellname=char.empty(0,1);
      while ~strcmp(strcell(k,i),'_')
          str_cellname=[str_cellname,strcell(k,i)];
          i=i+1;
      end
      gauss2dfitSTA([char(subfolder(k)),'\'],str_cellname);
      %cell_name(k)=cellstr(str_cellname);
  end 

