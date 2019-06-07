import pandapower as pp
#import pandapower.networks as pn
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandas as pd
from pandapower.plotting.plotly import simple_plotly
from pandapower.estimation import estimate


#read overall net from excel file
net = pp.from_excel("final code/circuits/net3.xlsx")
#net
#make some network plots
plot.simple_plot(net, show_plot=True, trafo_size = 1.25, plot_loads = True, plot_sgens = True)
simple_plotly(net,respect_switches=True )


####INDUSTRIAL FEEDER###########
ind_feeder = pp.from_excel("final code/circuits/ind_feeder.xlsx")
#ind_feeder
#make some network plots
plot.simple_plot(ind_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(ind_feeder)


####RESIDENTIAL FEEDER###########
res_feeder = pp.from_excel("final code/circuits/res_feeder.xlsx")
#res_feeder
#make some network plots
#plot.simple_plot(res_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(res_feeder)


####COMMERCIAL FEEDER###########
comm_feeder = pp.from_excel("final code/circuits/comm_feeder.xlsx")
#comm_feeder
#make some network plots
#plot.simple_plot(comm_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
#simple_plotly(comm_feeder)


####MIXED FEEDER###########
mixed_feeder = pp.from_excel("final code/circuits/mixed_feeder.xlsx")
#mixed_feeder
#make some network plots
#plot.simple_plot(mixed_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
#simple_plotly(mixed_feeder)


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
ind_feeder.measurement = pd.read_excel('final code/measurements/ind_feeder_m.xlsx')
successi = estimate(ind_feeder, init='flat')
print(successi)
#ind_feeder.measurement
#ind_feeder.res_line_est
ind_feeder.res_bus_est



#####RESIDENTIAL ESTIMATOR########
success = estimate(res_feeder, init='flat')
print(success)
#res_feeder.res_line_est
#res_feeder.res_bus_est

#####COMMERCIAL ESTIMATOR#########
#comm_feeder.measurement = pd.read_excel('final code/measurements/comm_feeder_m.xlsx')
successc = estimate(comm_feeder, init='flat')
print(successc)
#comm_feeder.res_line_est
#comm_feeder.res_bus_est

#####MIXED ESTIMATOR##############
successrc = estimate(mixed_feeder, init='flat')
print(successrc)
mixed_feeder.res_line_est
mixed_feeder.res_bus_est

#################################################SET UP MEASUREMENTS FOR OVERALL FEEDER########################

##############################BUS MEASUREMENTS#####################################
net = pp.from_excel("final code/circuits/net3.xlsx")
##RESIDENTIAL
i = 0
while i < len(res_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', res_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+3)
    pp.create_measurement(net, 'p', 'bus', -res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
    #pp.create_measurement(net, 'q', 'bus', res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
    i = i+ 1

##INDUSTRIAL
i = 0
while i < len(ind_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', ind_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+22)
    pp.create_measurement(net, 'p', 'bus', -ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
    #pp.create_measurement(net, 'q', 'bus', ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
    i = i+ 1

##COMMERCIAL
i = 0
while i < len(comm_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', comm_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+26)
    pp.create_measurement(net, 'p', 'bus', -comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
    #pp.create_measurement(net, 'q', 'bus', comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
    i = i+ 1

##MIXED
i = 0
while i < len(mixed_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', mixed_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+47)
    pp.create_measurement(net, 'p', 'bus', -mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
    #pp.create_measurement(net, 'q', 'bus', mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
    i = i+ 1


pp.create_measurement(net, 'v', 'bus', 1 , 0.0004, element = 0)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 1)
pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 1)
#pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 2)
pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 21)
#pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 25)
#pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 46)


#pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 26)
#pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 47)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 22)
pp.create_measurement(net, 'p', 'bus', -8, .001,  element = 23)
#pp.create_measurement(net, 'q', 'bus', -1, .001,  element = 24)
pp.create_measurement(net, 'q', 'bus', 0, .001,  element = 22)
pp.create_measurement(net, 'q', 'bus', 0, .001,  element = 24)
pp.create_measurement(net, 'q', 'bus', .52, .001,  element = 46)
pp.create_measurement(net, 'q', 'bus', 0, .001,  element = 4)
pp.create_measurement(net, 'q', 'bus', 0, .001,  element = 3)
pp.create_measurement(net, 'q', 'bus', 0, .001,  element = 47)
pp.create_measurement(net, 'q', 'bus', 0, .001,  element = 48)
net.measurement[30:40]

#net.measurement.to_excel('final code/measurements/allmeasev.xlsx')
########################################################OVERALL ESTIMATOR########################################

succes = estimate(net, init='flat')
print(succes)
net.res_line_est
net.res_bus_est
net.res_line_est.to_excel('final code/result/line_ev.xlsx')
net.res_bus_est.to_excel('final code/result/bus_ev.xlsx')

########################################################CHECK CONSTRAINTS#######################################
#net.res_line_est.loading_percent>75


########################################################ALLOCATE SOME FLEXIBILITY TO ALLEVIATE CONSTRAINTS#####

#####WHAT ARE THE OPTIONS FOR EACH FEEDER########
#DISPLAY OPTIONS AND CALCULATE CHEAPEST

#CHOOSE AND ALLEVIATE
#INDUSTRIAL
pp.create_measurement(net, 'p', 'bus', 3, .001,  element = 24)

pp.create_measurement(net, 'p', 'bus', 5, .001,  element = 23)
#COMMERCIAL
#pp.create_measurement(net, 'p', 'bus', 1.2, .001,  element = 33)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 35)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 45)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 46)
#RESIDENTIAL
#pp.create_measurement(net, 'p', 'bus', 0.5, .001,  element = 12)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 10)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 19)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 18)
#MIXED
#pp.create_measurement(net, 'p', 'bus', 0.1, .001,  element = 63)
#pp.create_measurement(net, 'p', 'bus', 2, .001,  element = 24)

#RECALCULATE STATE TO CONFIRM
successfinal = estimate(net, init='flat')
print(successfinal)
net.res_line_est
net.res_bus_est.to_excel('final code/result/bus_final.xlsx')
net.res_line_est.to_excel('final code/result/line_final.xlsx')
