function gauss2fitSecondPeak(carpeta,nombre_cell,STAtype)
    folder = [carpeta,nombre_cell,'_lineal/'];
    load([folder,'stavisual_lin_array_',nombre_cell,'.mat']);
    load([folder,'fit_var','.mat']);

    if STAtype=='ON'    %ON
        frame_ajuste = find(vector_amp == min(vector_amp));
        STA_ajuste = (STAarray_lin(:,:,frame_ajuste) - 255)*(-1); 
    else %ON
        frame_ajuste = find(vector_amp == max(vector_amp));
        STA_ajuste = STAarray_lin(:,:,frame_ajuste);
    end
    [fitresult, ~, ~, ~, ~, ~, ~, ~] = fmgaussfit(abs(STA_ajuste-mean2(STA_ajuste)));
    
    figsecondpeak = figure();
    pcolor(STA_ajuste);caxis([0 255])
    ellipse(fitresult(3),fitresult(4),deg2rad(fitresult(2)),fitresult(5),fitresult(6),'r');

    print(figsecondpeak,'-dpdf',[folder,'rf_secondpeak_',num2str(fitresult(1)),'.pdf']);
    save([folder,'fit_var_secondpeak.mat'],'fitresult');
