% ------------------------------------------------------------
% STA GAUSSIAN FIT STAGE
% PLOT STA RESULTS, RECEPTIVE FIELDS CALCULATED FROM STA_SSPY
% ------------------------------------------------------------
% This script plot the STA results from the receptive fields
% obtained from STA_PPY code (VERSION).
% The STA results are used for characterize retinal ganglion 
% cells. The founded receptive field are then fitted using 
% 2d gaussian MODEL, resulting in the STA estimation.
% The STA_SSPY output are matlab files that contains the 
% 3d matrix STA.
% This script contains this stages:
% (1) graph all the frames of the resulting SSPY STA
% (2) choose the max peak frame and fit a 2d gaussian model
%     and show a 3d graph profile.
% (3) show the 2d profile with its fitting of the max peak 
%     frame.
% (4) obtain a temporal profile of the max peak point in the
%     STA ensemble.
% (4) (optional) do the fit for all the frames.
%
% AASTUDILLO 2014
% ------------------------------------------------------------

% FOLDER NAME OF THE CELL (unit)
nombre_cell_grupo = 'H8a';

carpeta = ['STA_datos0003_2/',nombre_cell_grupo,'_lineal/'];

spiketimestamps_file = ['TS_datos0003_2/',nombre_cell_grupo,'.txt'];

%load([carpeta,'MEANSTA_line_',nombre_cell_grupo,'.mat']);
%load([carpeta,'stavisual_lin_array_e_',nombre_cell_grupo,'.mat']);
load([carpeta,'stavisual_lin_array_',nombre_cell_grupo,'.mat']);

spikestimes = load(spiketimestamps_file);

%% ISI BRIEF ANALYSIS
% diferencia = spikestimes(2:end)-spikestimes(1:end-1);
% figure, hist(diferencia,100)

%% normalize STA matrix for plot purposes

% correct the color scale for plot
STA_VISUAL = STAarray_lin + abs( min(STAarray_lin(:)) );
STA_VISUAL2 = STA_VISUAL*255/abs(max(STA_VISUAL(:)));

% correct the axis positions according to the MEA map position
STA_VISUAL2 = STA_VISUAL2(:,end:-1:1,:);

%%
fig1 = figure;

for k = 1:18
    subplot(3,6,k);
    
    I = STA_VISUAL2(:,:,k);
    J2 = imresize(I, 2, 'bilinear');
    
    imagesc(J2, [0 255] ); 
    title(['f ',num2str(k),' t ',num2str(k - 1 -12)]);
    axis off
    axis square  
end

colormap= 'jet';

v = 1;
print(fig1,'-dpdf',[carpeta,'rf_',num2str(v),'.pdf']);

%% 
% [maximo1 sel1] = max(max(max(abs(STA_VISUAL2))));
% [minimo1 sel2] = min(min(min(abs(STA_VISUAL2))));
% 
% STA_ajuste = STA_VISUAL2(:,:,11);

%% FIT 2D GAUSSIAN

STA_promedio = mean(STAarray_lin,3);

STA = STAarray_lin(:,end:-1:1,:);

%[n_filas,n_columnas] = size(STA_promedio);
aux =[];

promedio = mean(STA_promedio(:));

[min_sta,frame_min] = min(min(min(STA)));
[max_sta,frame_max] = max(max(max(STA)));
amp_min = promedio - min_sta;
amp_max = max_sta - promedio;

if amp_min >= amp_max
    frame_ajuste = frame_min;
    STA_ajuste = (STA(:,:,frame_ajuste) - 255)*(-1); 
else
    frame_ajuste = frame_max;
    STA_ajuste = STA(:,:,frame_ajuste);
end

tic;
[fitresult, zfit, xData2D, yData2D, fiterr, zerr, resnorm, rr] = fmgaussfit(STA_ajuste);
tempofit = toc

save([carpeta,'fit_var.mat'],'fitresult', 'zfit', 'xData2D', 'yData2D', 'fiterr', 'zerr', 'resnorm', 'rr');

%% figures: 3d profile of one  STA frame and its fit.
[n_filas,n_columnas] = size(STA_ajuste);

[Xpixel2D,Ypixel2D] = meshgrid(1:n_columnas,1:n_filas);

vent_str = num2str(frame_ajuste-1);

fig2 = figure;

subplot(2,2,1)
if amp_min >= amp_max
    mesh(Xpixel2D, Ypixel2D, double(255-STA_ajuste));
else
    mesh(Xpixel2D, Ypixel2D, double(STA_ajuste));
end
titulo_im_frame = strcat('Frame ',vent_str,' 3D Profile');
title(titulo_im_frame)
xlabel('X')
ylabel('Y')
axis([0 n_columnas+20 0 n_filas+20 -50 300])
    
subplot(2,2,2)
if amp_min >= amp_max
    meshc(xData2D, yData2D,255-zfit);
else
    meshc(xData2D, yData2D,zfit);
end
titulo_im_ajuste_frame = strcat('2D Gauss fit frame',vent_str);
title(titulo_im_ajuste_frame)
xlabel('X');
ylabel('Y');
    
subplot(2,2,3)
if amp_min >= amp_max
   plot(xData2D(1,:), 255-zfit(round(fitresult(6)),:),'LineWidth',2);
else
    plot(xData2D(1,:), zfit(round(fitresult(6)),:),'LineWidth',2);
end
grid;
title('Profile X axis'); xlabel('X'); ylabel('Z');
axis([0 n_columnas+20 -50 300])
    
subplot(2,2,4)
if amp_min >= amp_max
   plot(yData2D(:,1), 255-zfit(:,round(fitresult(5))),'LineWidth',2);
else
    plot(yData2D(:,1), zfit(:,round(fitresult(5))),'LineWidth',2);
end
grid;
title('Profile Y axis'); xlabel('Y'); ylabel('Z')
axis([0 n_filas+20 -50 300])

print(fig2,'-dpdf',[carpeta,'rf_fit',num2str(frame_ajuste),'.pdf']);

%% figure 2d profile of receptive field
fig3 = figure;

subplot(2,2,1)
if (amp_min >= amp_max)
   %mesh(Xpixel2D, Ypixel2D, double(255-STA_ajuste));
   imagesc(double(255-STA_ajuste), [0 255] ); 
else
   %mesh(Xpixel2D, Ypixel2D, double(STA_ajuste));
   imagesc(double(STA_ajuste), [0 255] ); 
end
titulo_im_frame = strcat('Frame ',vent_str,' 2D Profile');
title(titulo_im_frame)
%axis([0 n_columnas+20 0 n_filas+20 -50 300])

subplot(2,2,2)
if amp_min >= amp_max
   %mesh(xData2D, yData2D,255-zfit);
   imagesc(255-zfit, [0 255] );
else
   %mesh(xData2D, yData2D,zfit);
   imagesc(zfit, [0 255] );
end
titulo_im_ajuste_frame = strcat('2D Gauss fit frame',vent_str);
title(titulo_im_ajuste_frame);
%axis([0 n_columnas+20 0 n_filas+20 -50 300]);

%fitresult=[amp,     sx,    sxy,    sy,     xo,        yo,        zo]
%fitresult= 1        2      3       4       5x_pos_col 6y_pos_row 7z_pos
%fitresult= 177.3832 0.0000 39.8483 37.4116 76.1594    347.9796   74.7677

subplot(2,2,4)
[C,h] = contourf(flipud(zfit),1);
title('Contour of fit');
%axis off

subplot(2,2,2); 
x_lim =get(gca,'xlim'); 
y_lim =get(gca,'ylim');

subplot(2,2,3);
plot(fitresult(5),fitresult(6),'ro','MarkerSize',fitresult(4)/2,'LineWidth',2);
axis([x_lim(1) x_lim(2) y_lim(1) y_lim(2)]);
axis ij
title('Circle position');

print(fig3,'-dpdf',[carpeta,'rf_fit2d_',num2str(frame_ajuste),'.pdf']);

%% FIT TEMPORAL CURVE
Resultad = [frame_ajuste-1, fitresult];    
disp('N_frame     amplitud   angulo    sigma_x   sigma_y	  xo	   yo        z0');
%       10.0000  134.3579   95.4074   34.2291   29.3493   93.6269  116.2744  113.8308
disp(Resultad)

Resultad=Resultad';
save([carpeta,'resultado.txt'],'Resultad','-ascii');

resultadoex = num2cell(Resultad);
xlswrite([carpeta,'resultadoex.xls'],Resultad,1,'B1');

vent_ini = 0; %frame inicial para el perfil temporal(contando desde el frame 0)
vent_fin = 17;%frame final para el perfil temporal 

% get ampliutdes
vector_amp = [];
for frame = vent_ini+1:vent_fin+1, 
    vector_amp_nuevo = [vector_amp; STA(round(Resultad(7)),round(Resultad(6)),frame)]; 
    vector_amp = vector_amp_nuevo;
end

% plot
fig33 = figure;
plot(vent_ini:vent_fin,vector_amp,'LineWidth',2);
title('Max Amplitude Temporal Evolution')
xlabel('N Frame STA')
ylabel('Pixel value')
axis([vent_ini vent_fin 0 255])
grid;
print(fig33,'-dpdf',[carpeta,'rf_temp_',num2str(frame_ajuste),'.pdf']);

%% fit 2D GAUSSIAN for all the frames

doforallframes = 0;

if doforallframes 

stafit = zeros(380,380,18);
promedio = mean(STA_promedio(:));
[min_sta,frame_min] = min(min(min(STA)));
[max_sta,frame_max] = max(max(max(STA)));
amp_min = promedio - min_sta;
amp_max = max_sta - promedio;
for k = 1:18
    frame_ajuste = k;
    k
    min_delframe = min(min(STA(:,:,frame_ajuste)));
    max_delframe = max(max(STA(:,:,frame_ajuste)));
    if (promedio-min_delframe) >= (max_delframe - promedio)
        STA_ajuste = (STA(:,:,frame_ajuste) - promedio)*(-1); 
    else
        STA_ajuste = STA(:,:,frame_ajuste);
    end
%     if amp_min >= amp_max
%         %frame_ajuste = frame_min;
%         STA_ajuste = (STA(:,:,frame_ajuste) - 255)*(-1); 
%     else
%         %frame_ajuste = frame_max;
%         STA_ajuste = STA(:,:,frame_ajuste);
%     end
%     STA_ajuste = STA(:,:,frame_ajuste);
    
    [fitresult, zfit, xData2D, yData2D, fiterr, zerr, resnorm, rr] = fmgaussfit2(STA_ajuste);
    stafit(:,:,k) = zfit;
end

%%
fig4 = figure;

for k = 1:18
    subplot(3,6,k);
    
    %I = stafit(:,:,k);
    %J2 = imresize(I, 2, 'bilinear');
    J2 = stafit(:,:,k);
    min_delframe = min(min(J2));
    max_delframe = max(max(J2));
    if (promedio-min_delframe) >= (max_delframe - promedio)
        J2 = (J2 - promedio)*(-1); 
    end
    
    imagesc(J2, [0 255] ); 
    title(['f ',num2str(k),' t ',num2str(k - 1 -12)]);
    axis off
    axis square  
end

colormap= 'jet';

v = 1;
print(fig4,'-dpdf',[carpeta,'rf_fit_',num2str(v),'.pdf']);

end