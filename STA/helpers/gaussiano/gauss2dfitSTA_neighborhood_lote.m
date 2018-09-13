function gauss2dfitSTA_neighborhood_lote(carpeta,pre_frame,pos_frame)
    directories = dir(carpeta);
    
    for kdir=3:length(directories)
        if directories(kdir).isdir
            gauss2dfitSTA_neighborhood([directories(kdir).folder '/'],directories(kdir).name(1:end-7),pre_frame,pos_frame)
        end
    end