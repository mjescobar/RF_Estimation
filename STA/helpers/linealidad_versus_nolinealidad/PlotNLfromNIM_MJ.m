function PlotNLfromNIM_MJ(nim,name,savepath,sep)
% Plots nonlinearities from nim outputs

figfold = [savepath,sep,'NL_'];


fig=figure(1);
scatter(nim.bin_centers,nim.nonpar*nim.stim_params.dt);hold on
plot(nim.bin_centers,nim.pred*nim.stim_params.dt,'r-');hold on
xlim(nim.bin_edges([1 end]));               
title(['Unit ',name],'fontsize',6);                
set(gca,'fontsize',6);
saveas(gcf,[figfold,sep,name,'.png'],'png');
close(fig);


