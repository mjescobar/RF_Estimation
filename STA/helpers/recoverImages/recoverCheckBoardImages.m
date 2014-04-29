

%
%  Usage recoverCheckBoardImages(originalSeed,nimag)
%
%        originalSeed: Seed loaded from .mat file. It must inserted the
%        field 's', e.g., seedCINV.s
%        nimag: Number of images to create
%

function [images,originalSeed]=recoverCheckBoardImages(originalSeed,nimag)

if nargin<1,
    originalSeed = rng;
else
    rng(originalSeed);
end

blocks = 19;
pxs = 20;

%images = zeros(blocks*pxs,blocks*pxs,3,10);

for i=1:nimag,
    noise =  randi(2,blocks,blocks)-1;
    noiseimg = Expand(cat(3,noise*0,noise*255,noise*255),pxs);
    %images(:,:,:,i) = noiseimg;
    imwrite(noiseimg,['checker_' sprintf('%06d',i) '.png'],'png');
end
