function [raster]=createRaster(spklist,nframes,dt)

raster=zeros(nframes,1);

for i=1:length(spklist)
    frameId = ceil(spklist(i)/dt) + 1;
    if(frameId < nframes)
        raster(frameId) = raster(frameId) + 1;
    end
end



