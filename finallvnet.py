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
#plot.simple_plot(ind_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
#simple_plotly(ind_feeder)


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
#plot.simple_plot(comm_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
#simple_plotly(comm_feeder)


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
#ind_feeder.measurement
#ind_feeder.res_line_est
#ind_feeder.res_bus_est



#####RESIDENTIAL ESTIMATOR########
success = estimate(res_feeder, init='flat')
print(success)
#res_feeder.res_line_est
#res_feeder.res_bus_est



#####COMMERCIAL ESTIMATOR#########
successc = estimate(comm_feeder, init='flat')
print(successc)
#comm_feeder.res_line_est
#comm_feeder.res_bus_est



#####MIXED ESTIMATOR##############
successrc = estimate(mixed_feeder, init='flat')
print(successrc)
#mixed_feeder.res_line_est
#mixed_feeder.res_bus_est



#################################################SET UP MEASUREMENTS FOR OVERALL FEEDER########################

##############################BUS MEASUREMENTS#####################################

##RESIDENTIAL
i = 0
while i < len(res_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', res_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+3)
    pp.create_measurement(net, 'p', 'bus', res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
    i = i+ 1

##INDUSTRIAL
i = 0
while i < len(ind_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', ind_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+22)
    pp.create_measurement(net, 'p', 'bus', ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
    i = i+ 1

##COMMERCIAL
i = 0
while i < len(comm_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', comm_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+26)
    pp.create_measurement(net, 'p', 'bus', comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
    i = i+ 1

##MIXED
i = 0
while i < len(mixed_feeder.res_bus_est):
    pp.create_measurement(net, 'v', 'bus', mixed_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+47)
    pp.create_measurement(net, 'p', 'bus', mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
    i = i+ 1


pp.create_measurement(net, 'v', 'bus', 1 , 0.0004, element = 0)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 1)
pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 1)
#pp.create_measurement(net, 'v', 'bus', 1, .0004,  element = 2)
#pp.create_measurement(net, 'v', 'bus', 1, .0004,  element = 21)
#pp.create_measurement(net, 'v', 'bus', 1, .0004,  element = 46)

pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 26)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 47)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 22)
pp.create_measurement(net, 'p', 'bus', 0, .001,  element = 3)


#net.measurement

#net.measurement.to_excel('final code/measurements/allmeas1.xlsx')
########################################################OVERALL ESTIMATOR########################################

succes = estimate(net, init='flat')
print(succes)
net.res_line_est
net.res_bus_est.to_excel('final code/result/bus_init.xlsx')
net.res_line_est.to_excel('final code/result/line_init.xlsx')

n
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


















##############################LINE MEASUREMENTS#####################################

##RESIDENTIAL
datares = pd.DataFrame({'name':[None]*len(res_feeder.res_line_est.i_ka),
                        'measurement_type':['i']*len(res_feeder.res_line_est.i_ka),
                        'element_type':['line']*len(res_feeder.res_line_est.i_ka),
                        'element':list(range(1,18)),
                        'value':list(res_feeder.res_line_est.i_ka.values*1000),
                        'std_dev':[0.001]*len(res_feeder.res_line_est.i_ka),
                        'side':list(net.line.from_bus.loc[1:17].values)})



##COMMERCIAL
datacomm = pd.DataFrame({'name':[None]*len(comm_feeder.res_line_est.i_ka),
                        'measurement_type':['i']*len(comm_feeder.res_line_est.i_ka),
                        'element_type':['line']*len(comm_feeder.res_line_est.i_ka),
                        'element':list(range(23,42)),
                        'value':list(comm_feeder.res_line_est.i_ka.values*1000),
                        'std_dev':[0.001]*len(comm_feeder.res_line_est.i_ka),
                        'side':list(net.line.from_bus.loc[23:41].values)})


##INDUSTRIAL
dataind = pd.DataFrame({'name':[None]*len(ind_feeder.res_line_est.i_ka),
                        'measurement_type':['i']*len(ind_feeder.res_line_est.i_ka),
                        'element_type':['line']*len(ind_feeder.res_line_est.i_ka),
                        'element':list(range(19,22)),
                        'value':list(ind_feeder.res_line_est.i_ka.values*1000),
                        'std_dev':[0.001]*len(ind_feeder.res_line_est.i_ka),
                        'side':list(net.line.from_bus.loc[19:21].values)})


##MIXED
datamixed = pd.DataFrame({'name':[None]*len(mixed_feeder.res_line_est.i_ka),
                        'measurement_type':['i']*len(mixed_feeder.res_line_est.i_ka),
                        'element_type':['line']*len(mixed_feeder.res_line_est.i_ka),
                        'element':list(range(42,61)),
                        'value':list(mixed_feeder.res_line_est.i_ka.values*1000),
                        'std_dev':[0.001]*len(mixed_feeder.res_line_est.i_ka),
                        'side':list(net.line.from_bus.loc[42:60].values)})
