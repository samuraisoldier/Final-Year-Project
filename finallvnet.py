import pandapower as pp
#import pandapower.networks as pn
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandas as pd
from pandapower.plotting.plotly import simple_plotly


#read overall net from excel file
net = pp.from_excel("final code/circuits/net2.xlsx")
#net
#make some network plots
plot.simple_plot(net, show_plot=True, trafo_size = 1.25, plot_loads = True, plot_sgens = True)
simple_plotly(net,respect_switches=True )


####REDUCED NET###########
red_net = pp.from_excel("final code/circuits/red_net2.xlsx")
#red_net
#make some network plots
#plot.simple_plot(red_net, show_plot=True, trafo_size = 1.5)
simple_plotly(red_net)
#pp.to_excel(red_net, 'red_net2.xlsx', include_empty_tables = False)

####INDUSTRIAL FEEDER###########
ind_feeder = pp.from_excel("final code/circuits/ind_feeder.xlsx")
ind_feeder
#make some network plots
#plot.simple_plot(ind_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(ind_feeder)


####RESIDENTIAL FEEDER###########
res_feeder = pp.from_excel("final code/circuits/res_feeder.xlsx")
#res_feeder
#make some network plots
plot.simple_plot(res_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(res_feeder)


####COMMERCIAL FEEDER###########
comm_feeder = pp.from_excel("final code/circuits/comm_feeder.xlsx")
#comm_feeder
#make some network plots
plot.simple_plot(comm_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(comm_feeder)


####MIXED FEEDER###########
mixed_feeder = pp.from_excel("final code/circuits/mixed_feeder.xlsx")
#mixed_feeder
#make some network plots
plot.simple_plot(mixed_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(mixed_feeder)






#########################################################MEASUREMENTS#########################################

#####INDUSTRIAL MEASUREMENTS#########
ind_feeder.measurement = pd.read_excel('final code/measurements/ind_feeder_m.xlsx')

#####RESIDENTIAL MEASUREMENTS########
res_feeder.measurement = pd.read_excel('final code/measurements/res_feeder_m.xlsx')

#####COMMERCIAL MEASUREMENTS#########
comm_feeder.measurement = pd.read_excel('final code/measurements/comm_feeder_m.xlsx')

#####MIXED MEASUREMENTS##############
mixed_feeder.measurement = pd.read_excel('final code/measurements/mixed_feeder_m.xlsx')



########################################################RUN ESTIMATORS########################################

#####INDUSTRIAL ESTIMATOR#########
successi = estimate(ind_feeder, init='flat')
print(successi)
ind_feeder.res_line_est
ind_feeder.res_bus_est



#####RESIDENTIAL ESTIMATOR########
successr = estimate(res_feeder, init='flat')
print(successr)
res_feeder.res_line_est
res_feeder.res_bus_est



#####COMMERCIAL ESTIMATOR#########
successc = estimate(comm_feeder, init='flat')
print(successc)
comm_feeder.res_line_est
comm_feeder.res_bus_est



#####MIXED ESTIMATOR##############
successrc = estimate(mixed_feeder, init='flat')
print(successrc)
mixed_feeder.res_line_est
mixed_feeder.res_bus_est



#################################################SET UP MEASUREMENTS FOR OVERALL FEEDER########################








########################################################OVERALL ESTIMATOR########################################








########################################################CHECK CONSTRAINTS#######################################
###############################OVERALL NET


########################INDIVIDUAL FEEDERS
#INDUSTRIAL


#RESIDENTIAL


#COMMERCIAL


#MIXED



########################################################ALLOCATE SOME FLEXIBILITY TO ALLEVIATE CONSTRAINTS#####

#####WHAT ARE THE OPTIONS FOR EACH FEEDER########
#DISPLAY OPTIONS AND CALCULATE CHEAPEST
#CHOOSE AND ALLEVIATE
#RECALCULATE STATE TO CONFIRM
