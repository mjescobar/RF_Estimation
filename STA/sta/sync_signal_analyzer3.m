% Synchrony signal ANALIZER 3

% AASTUDILLO 17 OCTOBER 2013
% Modificado por Ricardo Villarroel 2 Diciembre 2013

% % %% for mcd file case
% % 
% % % open mcd lib files 
% % 
% % [nsresult] = ns_SetLibrary( 'nsMCDlibrary64.dll' )
% % % ns_SetDLL   Opens a Neuroshare Shared Library (.DLL or .so) in prepearation for other work
% % % for linux you must change this line to
% % % [nsresult] = ns_SetLibrary( 'nsMCDlibrary64.so' )
% % 
% % [nsresult,info] = ns_GetLibraryInfo()
% % 
% % %% open mcd data container file
% % pathname = '';
% % %filename1 = 'datos0001.mcd';
% % %filename = '../datos0001.mcd';
% % filename1 = 'datos0003.mcd';
% % filename = '../datos0003.mcd';
% % 
% % [nsresult, hfile] = ns_OpenFile([pathname filename])
% % [nsresult,info_file] = ns_GetFileInfo(hfile)
% % 
% % EntityCount = info_file.EntityCount; % total number of entities in the file
% % TimeStampRes = info_file.TimeStampResolution; % time between samples in seconds
% % TimeSpan = info_file.TimeSpan; % total time in seconds
% % 
% % %% open label of entities from mcd data file
% % 
% % % get all entities labels:
% % for k = 1:info_file.EntityCount;
% %     [nsresult,entity] = ns_GetEntityInfo(hfile,k);
% %     EntityLabels{k} = entity.EntityLabel;
% % end
% % 
% % EntityNumber = 253; % analog data A1
% % 
% % [nsresult,entity] = ns_GetEntityInfo(hfile,EntityNumber)
% % 
% % % [ns_RESULT, ContCount, Data] = ns_GetAnalogData(hFile, EntityID, StartIndex, IndexCount);
% % [nsresult,count,data] = ns_GetAnalogData(hfile,EntityNumber,1,entity.ItemCount); % Digital data

%% complete synchrony signal analysis : 
% OPTIONAL SIMPLE ANALYSIS

% 1) cada frame tiene una barra roja al final de su presentacion (en la base)
% 2) para cada barra roja la senal de sincronizacion muestra un pulso (app
% 1ms) de min 16 puntos sobre cierto umbral
% 3) el final de cada pulso representa el final de la presentacion de cada
% frame
% 4) en algunos casos cada frame es presentado dos veces (30 hz de
% presentacion) por lo que un frame en verdad es determinado por dos pulsos
% 5) la distancia  entre un pulso y otro determina el tiempo (en puntos) en
% que un frame fue mostrado.
% 6) el canto de bajada de un pulso de frame determina el final de un frame
% dado
% 7) el punto de inicio de cada frame debe ser estimado a partir de la
% distancia entre frames (en puntos) y el final de cada pulso

datosname = 'datos0005';

load(['syn_signal1_',datosname]);

%%

data= datos; %(1:24000000);

x = data;
umbral_volts = 0.151111112; %0.1511 ; % umbral en volts, determina criticamente el performance de la deteccion de frames
puntos_pulso = 50; %24*2; 24; % puntos maximos requeridos para considerar como un pulso de frame

duracion_min = length(data)/20000/60; % duracion en minutos de la senal
k_keep = 1;
contador_bajadas = 0;
posicion_bajada = [ ];

for k = puntos_pulso+1:length(x)-2
    if x(k) > umbral_volts
        if (x(k-1)>umbral_volts) && (x(k-puntos_pulso)< umbral_volts) && (x(k+1)<umbral_volts) && (x(k+1)<umbral_volts)
            posicion_bajada(k_keep) = k;
            contador_bajadas = contador_bajadas+1;
            k_keep = k_keep + 1;
        end
    end
end

distancias = posicion_bajada(2:end)-posicion_bajada(1:end-1);

duracion_min2 = length(posicion_bajada)*334/20000/60; % duracion de frames encontrados

brecha = duracion_min - duracion_min2;

lost_frames = find(distancias>334*2)

if isempty(lost_frames)
    %pos_bajada_val = posicion_bajada(1:(lost_frames(1)-1));
    pos_bajada_val = posicion_bajada;

    distancias2 = pos_bajada_val(2:end)-pos_bajada_val(1:end-1);

    duracion_min3 = length(pos_bajada_val)*334/20000/60; % duracion de frames encontrados y validos

    promedio_std_distancias = [ mean(distancias2), std(distancias2)] % debe ser cercano a 334
    %std_distancias = std(distancias2) % std debe ser no mayor que 2
end
%% see result

%inicio = 2212416-10000;
%20636000 - 20000+1; %final de la presentacion
%inicio =150000-20000; % inicio de presentacion datos_0003
inicio = 200000-20000;
%2545471-10000; %546000; %100000; %30000; %354000;

bloque = 10000*2;

xplot = data(inicio:inicio+bloque-1);
posiciones = find((posicion_bajada>inicio) & (posicion_bajada<inicio+bloque) );
m = posicion_bajada(posiciones)-inicio;

FIGURA = figure;
plot(xplot); 
hold on;
plot(xplot,'b.'); 
line([0 bloque],[umbral_volts umbral_volts],'Color','r');
plot( m , xplot(m),'r*');
for j=1:length(posiciones)
    %c = char(colorcitos(findex2(posiciones(j))));
    c = 'r';
    line( [m(j)-334 m(j)], [xplot(m(j))  xplot(m(j))],'Color',c,'LineWidth',2);
end
for j=1:length(posiciones)
    %c = char(colorcitos(findex2(posiciones(j))));
    c = 'g';
    line( [m(j)-334 m(j)], [0.2  0.2],'Color',c,'LineWidth',8);
end
hold off;
grid;
title('Syncronization signal analysis example'); xlabel('Time points'); ylabel('Amplitude V');

print(FIGURA,'-dpdf',['Figure_Sync_',datosname,'.pdf']);

%% output and save:
posicion_bajada_frame = pos_bajada_val(2:1:end);
frameduracion = round(mean(distancias2))*1; % debido a que cada frame se presenta dos veces: 2x334 puntos

fin_frame = posicion_bajada_frame; %valores medidos
inicio_frame = fin_frame - distancias2(1: length(fin_frame)); %valores estimados
inicio_fin_frame = [inicio_frame', fin_frame'];
%save('sync_analysis_output.mat','s','s2','cantobajada2','frameduracion');
save(['inicio_fin_frame_',datosname,'.txt' ],'inicio_fin_frame', '-ASCII' ,'-DOUBLE');

% inicio de frames corresponde a : cantobajada2(1)-frameduracion
% posici�n inicial de cada frame (i) corresponde al vector : s2(:,1)-frameduracion

%% -------------------------- aditional help -----------------------
% For convertion of time points (or seconds or miliseconds) to frame index:
% if a spike position is spk =  4346+30000 (for example frame block 10, frame index 5)
% so the steps to get the frame index are:

%spkstamp = 4346+30000; 

%framepoints = 334*2; % proviene de framepoints



% ------------------------------------------------
% % estaS lineaS estaN incorrectaS:
% traslatedindex = spkstamp - (posicion_bajada_frame(1) - framepoints) % marca inicio de frames : LINEA INCORRECTA
% 
% newindex = floor(traslatedindex/framepoints)+1
% 
% sincmatrix(newindex,:) %%all the data of the frame
% 
% % another option is 
% p = find(sincmatrix(:,1)>spkstamp & sincmatrix(:,1)<spkstamp+2*framepoints )
% % where the first p is the position of the frame in sincmatrix