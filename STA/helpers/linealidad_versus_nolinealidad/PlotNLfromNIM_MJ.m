function PlotNLfromNIM_MJ(nim,name,savepath,sep)
% Plots nonlinearities from nim outputs

figfold = [savepath,sep,'NL_'];
mkdir(figfold);
%mkdir(figfold);

fig=figure(1);
scatter(nim{1}.bin_centers,nim{1}.nonpar/nim{1}.stim_params.dt);hold on
plot(nim{1}.bin_centers,nim{1}.pred/nim{1}.stim_params.dt,'r-');hold on
yl = ylim();
%plot(nim{1}.x,nim{1}.n/max(nim{1}.n)*yl(2),'k')                
xlim(nim{1}.bin_edges([1 end]));               
title(['Unit ',name],'fontsize',6);                
set(gca,'fontsize',6);
saveas(gcf,[figfold,sep,name,'.png'],'png');
%close(fig);


