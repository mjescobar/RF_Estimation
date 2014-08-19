function [ stim, originalSeed] = get_stim_from_seed_sta( seed_file,first_file,nimag,blocks,outputname ,do_v7 );
% get stimuli ensemble from seed file and save to a mat file
% INPUTS:
%   seed_file: File with the seed to generates the random values
%   first_file: File with the first generated frames as reference
%   nimag: Number of images to generate
%   blocks: Number of pixel blocks of one side of the squared frame.
%           This number must be knowed from previous information.
%   outputname: string for the output file name with the stimuli matrix.
%   do_v73: define if save the stimuli matrix with the v7.3 option (for
%   large matrix)
% 
% OUTPUTS:
%   stim: stimuli matrix, contain all the frames
%   originalSeed: original used seed for generate random values
% 
% USAGE
% >> seed_file = 'Exp__2014_05_08-16.01.01/Seed_2.mat';
% >> first_file = 'Exp__2014_05_08-16.01.01/FirstImages_2.mat';
% >> nimag = 58000;
% >> blocks = 16;
% >> outputname = '2014_05_08-16.01.01-58k';
% >> do_v73=0;
% >> [ stim, originalSeed] = get_stim_from_seed_sta(seed_file,first_file,nimag,blocks,outputname,do_v7 );
% 
% ALAND ASTUDILLO JUNIO 2014
% MJE 2014
% Other references 2014

% seed_file = 'Exp__2014_05_08-16.01.01/Seed_2.mat';
% first_file = 'Exp__2014_05_08-16.01.01/FirstImages_2.mat';
% nimag = 58000;
% blocks = 16;
% outputname = '2014_05_08-16.01.01-58k';
% do_v73=0;

seed = load(seed_file);
first_images = load(first_file);

oi = first_images.fi;
oi1 = oi(:,:,:,1);
% figure, imshow(oi1); title('original image');
%% generates

pxs = 1;
[stim , originalSeed] = recoverCheckBoardImages1( seed.s , nimag ,blocks,pxs);
%% Save the stimuli matrix
if do_v7
save(['stim_mini_',outputname,'.mat'],'stim','-v7');
else 
save(['stim_mini_',outputname,'.mat'],'stim','-v7.3');
end
%% validates

im1 = stim(:,:,:,1);
% figure, imshow(im1); axis image; title('result image');

oi1_resized = imresize(oi1,1/size(oi1,1)*blocks,'box');
% figure, imshow(oi1_resized); axis image; title('resized original image');

end

function [images,originalSeed]=recoverCheckBoardImages1(originalSeed,nimag,blocks,pxs)
%  Usage recoverCheckBoardImages(originalSeed,nimag)
%
%        originalSeed: Seed loaded from .mat file. It must inserted the
%        field 's', e.g., seedCINV.s
%        nimag: Number of images to create
% MJE 2014
if nargin<1,
    originalSeed = rng;
else
    rng(originalSeed);
end
% blocks = 19;
% pxs = 20;
%images = zeros(blocks*pxs,blocks*pxs,3,10);
for i=1:nimag,
    noise =  randi(2,blocks,blocks)-1;
    noiseimg = Expand1(cat(3,noise*0,noise*255,noise*255),pxs);
    images(:,:,:,i) = noiseimg;
    %imwrite(noiseimg,['checker_' sprintf('%06d',i) '.png'],'png');
end
end

function B=Expand1(A,horizontalFactor,verticalFactor)
% B=Expand(A,horizontalFactor,[verticalFactor])
%
% Expands the ND matrix A by cell replication, and returns the result.
% If the vertical scale factor is omitted, it is assumed to be 
% the same as the horizontal. Note that the horizontal-before-vertical
% ordering of arguments is consistent with image processing, but contrary 
% to Matlab's rows-before-columns convention.
%
% We use "Tony's Trick" to replicate a vector, as explained
% in MathWorks Matlab Technote 1109, section 4.
%
% Also see ScaleRect.m

% Denis Pelli 5/27/96, 6/14/96, 7/6/96
% 7/24/02 dgp Support an arbitrary number of dimensions.
% 13/06/12 DN Redid internals for significant speedup.

if nargin<2 || nargin>3
	error('Usage: A=Expand(A,horizontalFactor,[verticalFactor])');
end
if nargin==2
	verticalFactor=horizontalFactor;
end

psychassert1(round(verticalFactor)  ==verticalFactor   && verticalFactor>=1 && ... 
            round(horizontalFactor)==horizontalFactor && horizontalFactor>=1, ...
        	'Expand only supports positive integer factors.');
psychassert1(~isempty(A),'Can''t expand an empty matrix');


% Generate row copying instructions index.
inds                            = 1:size(A,1);
rowCopyingInstructionsIndex     = inds(ones(verticalFactor,1),:);
rowCopyingInstructionsIndex     = rowCopyingInstructionsIndex(:);

% Generate column copying instructions index.
inds                            = 1:size(A,2);
columnCopyingInstructionsIndex  = inds(ones(horizontalFactor,1),:);
columnCopyingInstructionsIndex  = columnCopyingInstructionsIndex(:)';

% The following code uses Matlab's matrix indexing quirks to magnify the
% matrix.  It is easier to understand how it works by looking at a specific
% example:
% 
% >> n = [1 2; 3 4] % Matlab, please give me a matrix with four elements.
%
% n =
% 
%      1     2
%      3     4
% 
% >> % Matlab, please generate a new matrix by using the provided copying
% >> % instructions index.  My copying instructions index says that you
% >> % should print the first column twice, then print the second column
% >> % twice.  Thanks.
% >> m = n(:, [1 1 2 2])
% 
% m =
% 
%      1     1     2     2
%      3     3     4     4
%
% >> % Matlab, please generate a new matrix by using the provided copying
% >> % instructions index.  My copying instructions index says that you
% >> % should print the first row twice, then print the second row
% >> % twice.  Thanks.
% >> m = n([1 1 2 2], :)
% 
% m =
% 
%      1     2
%      1     2
%      3     4
%      3     4
%
if ndims(A)>3
    colon = {':'};
    B = A(rowCopyingInstructionsIndex, columnCopyingInstructionsIndex, colon{ones(1,ndims(A)-2)});
else
    B = A(rowCopyingInstructionsIndex, columnCopyingInstructionsIndex,:);
end
end

function psychassert1(varargin)
% psychassert(expression, ...) - Replacement for Matlab 7 builtin assert().
% This is hopefully useful for older Matlab installations and
% for the Octave port:
%
% If the assert-function is supported as builtin function on
% your Matlab installation, this function will call the builtin
% "real" assert function. Read the "help assert" for usage info.
%
% If your Matlab lacks a assert-function, this function
% will try to emulate the real assert function. The only known limitation
% of our own assert wrt. Matlabs assert is that it can't handle the MSG_ID
% parameter as 2nd argument. Passing only message strings or message
% formatting strings + variable number of arguments should work.
%

% History:
% 01/06/09 mk Wrote it. Based on the specification of assert in Matlab 7.3.

if exist('assert', 'builtin')==5
  % Call builtin implementation:
  builtin('assert', varargin{:});
else
  % Use our fallback-implementation:
  if nargin < 1
      error('Not enough input arguments.');
  else
      expression = varargin{1};
      if ~isscalar(expression) || ~islogical(expression)
          error('The condition input argument must be a scalar logical.');
      end
      
      % Expression true?
      if ~expression
          % Assertion failed:
          if nargin < 2
              error('Assertion failed.');
          else
              if nargin < 3
                  emsg = sprintf('%s\n', varargin{2});
                  error(emsg); %#ok<SPERR>
              else
                  emsg = sprintf(varargin{2}, varargin{3:end});
                  error(emsg); %#ok<SPERR>                  
              end
          end
      end
  end
end

return;
end
