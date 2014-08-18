%% sta inspector
%% This function gives back the SNR value for every unit 
function sta_inspector (unit_file, sta_folder, inicio, limite)
% datos = '001';

units = textread(unit_file,'%s','delimiter','\t');

%charac = load(['characterization_',datos,'.txt']);
charac = ones(length(units),1);

snr_inspector = zeros(length(units),1);
unit_name_inspector= cell(length(units),1);


classfolder = 'sta_inspector';
mkdir([sta_folder,'/',classfolder]);

dimensiones = 5;
nclusters = 6;

% inicio = 1;
% limite = 95; %23+5; %length(charac); 

doplot = 1;
numframes = 20;
spikeframe = 18;
contadorunit = 1;

dotemp = 1;

for kunit = inicio:limite
if (charac(kunit)>0)
    indexvector(contadorunit) = kunit;
%%
% FOLDER NAME OF THE CELL

charunit = char(units(kunit));
display(charunit);
carpeta = [sta_folder,'\',charunit,'_lineal\'];

nombre_cell_grupo = char(charunit);

load([carpeta,'stavisual_lin_array_',nombre_cell_grupo,'.mat']);
load([carpeta,'sta_array_',nombre_cell_grupo,'.mat']);
% STAarray_lin(:,:,:) = stavisual_lin(:,:,3,:);
% STA_array(:,:,:) = STA(:,:,3,:);
% STA_array(:,:,:) = STA(:,:,3,:);

% clear stavisual_lin
% clear STA

% img_total=STAarray_lin(:);
img_total= STA_array(:);

ima_total=max(img_total(:));

disp ('max');
disp (ima_total);

imi_total=min(img_total(:));

disp ('min');
disp(imi_total);

primer_frame=STA_array(:,:,1);
disp(size(primer_frame(:)));
ims_total=std(primer_frame(:));
disp('size imgtotal');
disp(size(ims_total));

disp ('std_deviation');
disp(ims_total);

snr_total=20*log10(abs(ima_total-imi_total)./ims_total);

disp('SNR');
disp(snr_total);

unit_name_inspector{kunit}=nombre_cell_grupo; 
snr_inspector(kunit) = snr_total;
% snr = 10.147 % which fulfills the rose criterion...

%%
%--------------------------------------------------------------------------
if doplot
    fig1=figure('Visible','off');
    for k=1:spikeframe; 
        subplot(3,6,k); 
        imshow(uint8(STAarray_lin(:,:,k))); 
        
%         img=STAarray_lin(:,:,k);
%         ima=max(img(:));
%         imi=min(img(:));
%         ims=std(img(:));
%         snr=20*log10((ima-imi)./ims);
%         title(['SNR ',num2str(snr)]);
    end; 
    title(['SNR total ',num2str(snr_total)]);
    colormap('jet');
    %save([carpeta,'time_curves_',nombre_cell_grupo,'.mat'],'temporalcurve1','tvector','spline_curve','frame_ajuste','fc');
    print(fig1,'-dpng',[sta_folder,'/',classfolder,'/',charunit,'.png']);
end
%--------------------------------------------------------------------------

if dotemp
 %% normalize STA matrix for plot purposes
STA_promedio = mean(STAarray_lin,3);

STA = STAarray_lin(:,end:-1:1,:);

[n_filas,n_columnas] = size(STA_promedio);

promedio = mean(STA_promedio(:));

[min_sta,frame_min] = min(min(min(STA)));
[max_sta,frame_max] = max(max(max(STA)));
amp_min = promedio - min_sta;
amp_max = max_sta - promedio;

if amp_min >= amp_max
    frame_ajuste = frame_min;
%     STA_ajuste = (STA(:,:,frame_ajuste) - 255)*(-1); 
    ss = STAarray_lin(:,:,frame_ajuste);
    [fila,col]=find(ss==min(min(ss)));
else
    frame_ajuste = frame_max;
%     STA_ajuste = STA(:,:,frame_ajuste);
    ss = STAarray_lin(:,:,frame_ajuste);
    [fila,col]=find(ss==max(max(ss)));
end

% fc = [fila(1),col(1)];
fc = [round(mean(fila)),round(mean(col))];

% temporalcurve = STAarray_lin(fc(1),fc(2),:);
% tempcurve = temporalcurve(:);

temporalcurve1 = STA_array(fc(1),fc(2),:);
temporalcurve2 = STAarray_lin(fc(1),fc(2),:);
tempcurve = temporalcurve1(:)/sum(abs(temporalcurve1));

tvector = ((1:numframes)-spikeframe)/60*1000;

pp = csaps(tvector,tempcurve);
spline_curve = fnplt(pp);
% spline_curve = points;

alltempcurves(:,contadorunit) = tempcurve;
alltempcurvesinterpolated(:,:,contadorunit) = spline_curve;
contadorunit = contadorunit+1;

save([carpeta,'time_curves_',nombre_cell_grupo,'.mat'],'temporalcurve1','tvector','spline_curve','frame_ajuste','fc');

%%
% if doplot
%     figure;
%     imshow(uint8(sta(:,:,frame_ajuste))); 
%     colormap('gray'); 
%     colorbar;
%     hold on, 
%     line([0 400],[fc(2) fc(2)],'Color','r')
%     line([fc(1) fc(1)],[0 400],'Color','r')
% end

%%
% if doplot
%     tvector = ((1:18)-13)/60*1000;
%     figure, 
%     plot(tvector,tempcurve,'LineWidth',2);
%     hold on
%     line([0 0],[0 255],'Color','r','LineWidth',2);
%     grid
%     xlabel('Time ms');
%     ylabel('Amplitude');
%     xlim([-200 50]);
%     ylim([-2 256]);
% end
end
disp(['k unit ',num2str(kunit)])
end
end

%%
% normalize each curve
if dotemp
donorm = 0;
if donorm
for k=1:size(alltempcurves,2) %size(list_dir,1)
    alltempcurves2(:,k) = alltempcurves(:,k) - alltempcurves(spikeframe,k);
end
else 
    alltempcurves2 = alltempcurves;
end
end

%%
if dotemp
tvector = ((1:numframes)-spikeframe)/60*1000;
h1=figure;
plot(tvector,alltempcurves2,'Color','b','LineWidth',1);
hold on
line([0 0],[-100 50],'Color','r','LineWidth',2);
grid
xlabel('Time ms');
ylabel('Amplitude');
title('Temporal Profiles');
xlim([-300 40]);
ylim([-0.35 0.35]);

%%
h1_1=figure;
xcurve(1:size(alltempcurvesinterpolated,2),1:size(alltempcurvesinterpolated,3)) = alltempcurvesinterpolated(1,:,:);
ycurve(1:size(alltempcurvesinterpolated,2),1:size(alltempcurvesinterpolated,3)) = alltempcurvesinterpolated(2,:,:);

plot(xcurve,ycurve,'Color','b','LineWidth',1);
hold on
line([0 0],[-100 50],'Color','r','LineWidth',2);
grid
xlabel('Time ms');
ylabel('Amplitude');
title('Temporal Profiles');
xlim([-300 40]);
ylim([-0.35 0.35]);

%%
X = alltempcurves2';
[COEFF,SCORE,latent] = princomp(X);

%%
h2=figure;
plot3(SCORE(:,1),SCORE(:,2),SCORE(:,3),'b.');
grid;
xlabel('PC1');
ylabel('PC2');
zlabel('PC3');
title('Feature space PCA');

%%
opts = statset('Display','final');

X2 = SCORE(:,1:dimensiones);
[idx,ctrs] = kmeans(X2,nclusters,'Distance','sqEuclidean','Replicates',10,'Options',opts,'start','cluster');

%%
h3=figure;
plot(X2(idx==1,1),X2(idx==1,2),'r.','MarkerSize',12)
hold on
plot(X2(idx==2,1),X2(idx==2,2),'b.','MarkerSize',12)
plot(X2(idx==3,1),X2(idx==3,2),'g.','MarkerSize',12)
plot(X2(idx==4,1),X2(idx==4,2),'m.','MarkerSize',12)
plot(X2(idx==5,1),X2(idx==5,2),'c.','MarkerSize',12)
plot(X2(idx==6,1),X2(idx==6,2),'y.','MarkerSize',12)
plot(ctrs(:,1),ctrs(:,2),'kx','MarkerSize',12,'LineWidth',2)
plot(ctrs(:,1),ctrs(:,2),'ko','MarkerSize',12,'LineWidth',2)
grid
xlabel('PC1');
ylabel('PC2');
title('Features space PCA');

%%
h3_3=figure;
plot3(SCORE(idx==1,1),SCORE(idx==1,2),SCORE(idx==1,3),'r.'); hold on
plot3(SCORE(idx==2,1),SCORE(idx==2,2),SCORE(idx==2,3),'b.');
plot3(SCORE(idx==3,1),SCORE(idx==3,2),SCORE(idx==3,3),'g.');
plot3(SCORE(idx==4,1),SCORE(idx==4,2),SCORE(idx==4,3),'m.');
plot3(SCORE(idx==5,1),SCORE(idx==5,2),SCORE(idx==5,3),'c.');
plot3(SCORE(idx==6,1),SCORE(idx==6,2),SCORE(idx==6,3),'y.');
grid;
xlabel('PC1');
ylabel('PC2');
zlabel('PC3');
title('Feature space PCA');

%%
meancurve1=mean(alltempcurves2(:,idx==1),2);
meancurve2=mean(alltempcurves2(:,idx==2),2);
meancurve3=mean(alltempcurves2(:,idx==3),2);
meancurve4=mean(alltempcurves2(:,idx==4),2);
meancurve5=mean(alltempcurves2(:,idx==5),2);
meancurve6=mean(alltempcurves2(:,idx==6),2);

tvector = ((1:numframes)-spikeframe)/60*1000;

h4=figure;
plot(tvector,alltempcurves2(:,idx==1),'Color','r','LineWidth',1); hold on
plot(tvector,alltempcurves2(:,idx==2),'Color','b','LineWidth',1);
plot(tvector,alltempcurves2(:,idx==3),'Color','g','LineWidth',1);
plot(tvector,alltempcurves2(:,idx==4),'Color','m','LineWidth',1);
plot(tvector,alltempcurves2(:,idx==5),'Color','c','LineWidth',1);
plot(tvector,alltempcurves2(:,idx==6),'Color','y','LineWidth',1);
plot(tvector,meancurve1,'k--','LineWidth',3);
plot(tvector,meancurve2,'k--','LineWidth',3);
plot(tvector,meancurve3,'k--','LineWidth',3);
plot(tvector,meancurve4,'k--','LineWidth',3);
plot(tvector,meancurve5,'k--','LineWidth',3);
plot(tvector,meancurve6,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid
xlabel('Time ms');
ylabel('Amplitude');
title('Temporal Profile');
xlim([-300 40]);
ylim([-0.35 0.35]);



%% subplots of each cluster
% tvector = ((1:numframes)-spikeframe)/60*1000;

h5=figure;
subplot(2,3,1); 
plot(tvector,alltempcurves2(:,idx==1),'Color','r','LineWidth',1); hold on
plot(tvector,meancurve1,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster1');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,2); 
plot(tvector,alltempcurves2(:,idx==2),'Color','b','LineWidth',1); hold on
plot(tvector,meancurve2,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster2');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,3); 
plot(tvector,alltempcurves2(:,idx==3),'Color','g','LineWidth',1); hold on
plot(tvector,meancurve3,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster3');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,4); 
plot(tvector,alltempcurves2(:,idx==4),'Color','m','LineWidth',1); hold on
plot(tvector,meancurve4,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster4');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,5); 
plot(tvector,alltempcurves2(:,idx==5),'Color','c','LineWidth',1); hold on
plot(tvector,meancurve5,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster5');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,6); 
plot(tvector,alltempcurves2(:,idx==6),'Color','y','LineWidth',1); hold on
plot(tvector,meancurve6,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster5');
xlim([-300 40]);
ylim([-0.35 0.35]);

%%
h4_1=figure;
%plot(xcurve,ycurve,'Color','b','LineWidth',1);

mc1=mean(ycurve(:,idx==1),2);
mc2=mean(ycurve(:,idx==2),2);
mc3=mean(ycurve(:,idx==3),2);
mc4=mean(ycurve(:,idx==4),2);
mc5=mean(ycurve(:,idx==5),2);
mc6=mean(ycurve(:,idx==6),2);

plot(xcurve(:,1),ycurve(:,idx==1),'Color','r','LineWidth',1); hold on
plot(xcurve(:,1),ycurve(:,idx==2),'Color','b','LineWidth',1);
plot(xcurve(:,1),ycurve(:,idx==3),'Color','g','LineWidth',1);
plot(xcurve(:,1),ycurve(:,idx==4),'Color','m','LineWidth',1);
plot(xcurve(:,1),ycurve(:,idx==5),'Color','c','LineWidth',1);
plot(xcurve(:,1),ycurve(:,idx==6),'Color','y','LineWidth',1);
plot(xcurve(:,1),mc1,'k--','LineWidth',3);
plot(xcurve(:,1),mc2,'k--','LineWidth',3);
plot(xcurve(:,1),mc3,'k--','LineWidth',3);
plot(xcurve(:,1),mc4,'k--','LineWidth',3);
plot(xcurve(:,1),mc5,'k--','LineWidth',3);
plot(xcurve(:,1),mc6,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid
xlabel('Time ms');
ylabel('Amplitude');
title('Temporal Profile');
xlim([-300 40]);
ylim([-0.35 0.35]);

%%
%tvector = ((1:numframes)-spikeframe)/60*1000;
%plot(xcurve,ycurve,'Color','b','LineWidth',1);
h5_1=figure;

subplot(2,3,1); 
plot(xcurve(:,1),ycurve(:,idx==1),'Color','r','LineWidth',1); hold on
plot(xcurve(:,1),mc1,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster1');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,2); 
plot(xcurve(:,1),ycurve(:,idx==2),'Color','b','LineWidth',1); hold on
plot(xcurve(:,1),mc2,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster2');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,3); 
plot(xcurve(:,1),ycurve(:,idx==3),'Color','g','LineWidth',1); hold on
plot(xcurve(:,1),mc3,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster3');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,4); 
plot(xcurve(:,1),ycurve(:,idx==4),'Color','m','LineWidth',1); hold on
plot(xcurve(:,1),mc4,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster4');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,5); 
plot(xcurve(:,1),ycurve(:,idx==5),'Color','c','LineWidth',1); hold on
plot(xcurve(:,1),mc5,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster5');
xlim([-300 40]);
ylim([-0.35 0.35]);

subplot(2,3,6); 
plot(xcurve(:,1),ycurve(:,idx==6),'Color','y','LineWidth',1); hold on
plot(xcurve(:,1),mc6,'k--','LineWidth',3);
line([0 0],[-255 255],'Color','r','LineWidth',2);
grid; xlabel('Time ms'); ylabel('Amplitude'); title('Temporal Profile Cluster5');
xlim([-300 40]);
ylim([-0.35 0.35]);

%% save images


print(h1,'-dpdf',[sta_folder,'/',classfolder,'/h1_temp_prof.pdf']);
print(h2,'-dpdf',[sta_folder,'/',classfolder,'/h2_pca.pdf']);
print(h3,'-dpdf',[sta_folder,'/',classfolder,'/h3_pca_kmeans.pdf']);
print(h3_3,'-dpdf',[sta_folder,'/',classfolder,'/h3_3_pca_kmeans.pdf']);
print(h4,'-dpdf',[sta_folder,'/',classfolder,'/h4_temp_clustered.pdf']);
print(h5,'-dpdf',[sta_folder,'/',classfolder,'/h5_tp_clusters.pdf']);

print(h1_1,'-dpdf',[sta_folder,'/',classfolder,'/h1_spline_temp_prof.pdf']);
print(h4_1,'-dpdf',[sta_folder,'/',classfolder,'/h4_spline_temp_clustered.pdf']);
print(h5_1,'-dpdf',[sta_folder,'/',classfolder,'/h5_spline_tp_clusters.pdf']);

% PNGS
print(h1,'-dpng',[sta_folder,'/',classfolder,'/h1_temp_prof.png']);
print(h2,'-dpng',[sta_folder,'/',classfolder,'/h2_pca.png']);
print(h3,'-dpng',[sta_folder,'/',classfolder,'/h3_pca_kmeans.png']);
print(h3_3,'-dpng',[sta_folder,'/',classfolder,'/h3_3_pca_kmeans.png']);
print(h4,'-dpng',[sta_folder,'/',classfolder,'/h4_temp_clustered.png']);
print(h5,'-dpng',[sta_folder,'/',classfolder,'/h5_tp_clusters.png']);

print(h1_1,'-dpng',[sta_folder,'/',classfolder,'/h1_spline_temp_prof.png']);
print(h4_1,'-dpng',[sta_folder,'/',classfolder,'/h4_spline_temp_clustered.png']);
print(h5_1,'-dpng',[sta_folder,'/',classfolder,'/h5_spline_tp_clusters.png']);

%% get the labels of each unit
% units_line = list_dir(3:end);
% units = {};
% for k =1:size(units_line,1)
%     u = char(units_line(k));
%     units{k} = [u(1:end-7)];
% end
% 
% table_id = [units(1:limite)];
% 
% for k=1:size(table_id,2)
%     table_id{2,k} = (idx(k));
% end
% 
% save([path,'_table_id.mat'],'table_id');
cont =1;
for k=indexvector;
    table_id{1,k}=units(k);
    table_id{2,k}=charac(k);
    table_id{3,k}=idx(cont);
    
    table_id_mini{1,cont}=units(k);
    table_id_mini{2,cont}=charac(k);
    table_id_mini{3,cont}=idx(cont);
    cont=cont+1;
end
save([sta_folder,'/',classfolder,'/classification.mat'],'table_id','table_id_mini');
%% IMPROVE THE TEMPORAL PROFILE PLOTS:

save([sta_folder,'/',classfolder,'/all_temp_curves.mat'],'units','charac','idx','tvector','alltempcurves','alltempcurvesinterpolated','SCORE','COEFF','xcurve','ycurve');

end

% snr_inspector
save([sta_folder,'/',classfolder,'/snr_inspector.mat'],'snr_inspector');
save([sta_folder,'/',classfolder,'/unit_name_inspector.mat'],'unit_name_inspector');