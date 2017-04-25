(1) plotProbeVars.py plots all the probe variables and saves as .png

(2)To run it, do:
python plotProbeVars.py

(3) (Above command) It plots in linear(creates and saves plots in plotsLinear<runperiod>) and log scale(creates and saves plots in plotsLog<runperiod>). 
plotProbeVars.py also creates to root files:
histoData_<runperiod>.root and histoMC_<runperiod>.root
These two root files can be useful incase someone wants to do style changes to the plots.

(4) To plot the plots on the same canvas from data and MC using the above two root file, 
do:
root -l -b -q plot.C
This command will store all the plots in plots directory - make sure you have this directory 
--- will add later a command that plot.C automatically creates plots directory


