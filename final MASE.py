import pandapower as pp
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandas as pd
from pandapower.estimation import estimate


#read overall net from excel file
net = pp.from_excel("final code/circuits/net3.xlsx")
plot.simple_plot(net, show_plot=True, trafo_size = 1.25, plot_loads = True, plot_sgens = True)

####INDUSTRIAL FEEDER###########
ind_feeder = pp.from_excel("final code/circuits/ind_feeder.xlsx")
plot.simple_plot(ind_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)

####RESIDENTIAL FEEDER###########
res_feeder = pp.from_excel("final code/circuits/res_feeder.xlsx")
plot.simple_plot(res_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)

####COMMERCIAL FEEDER###########
comm_feeder = pp.from_excel("final code/circuits/comm_feeder.xlsx")
plot.simple_plot(comm_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)

####MIXED FEEDER###########
mixed_feeder = pp.from_excel("final code/circuits/mixed_feeder.xlsx")
plot.simple_plot(mixed_feeder, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)

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

#####RESIDENTIAL ESTIMATOR########
successr = estimate(res_feeder, init='flat')
print(successr)

#####COMMERCIAL ESTIMATOR#########
successc = estimate(comm_feeder, init='flat')
print(successc)

#####MIXED ESTIMATOR##############
successrc = estimate(mixed_feeder, init='flat')
print(successrc)

#################################################SET UP MEASUREMENTS FOR OVERALL FEEDER########################
j = 0
while j < 1:
    ##RESIDENTIAL
    i = 0
    while i < len(res_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', res_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+3)
        pp.create_measurement(net, 'p', 'bus', -res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
        pp.create_measurement(net, 'q', 'bus', res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
        i = i+ 1

    ##INDUSTRIAL
    i = 0
    while i < len(ind_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', ind_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+22)
        pp.create_measurement(net, 'p', 'bus', -ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
        pp.create_measurement(net, 'q', 'bus', ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
        i = i+ 1

    ##COMMERCIAL
    i = 0
    while i < len(comm_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', comm_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+26)
        pp.create_measurement(net, 'p', 'bus', -comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
        pp.create_measurement(net, 'q', 'bus', comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
        i = i+ 1

    ##MIXED
    i = 0
    while i < len(mixed_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', mixed_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+47)
        pp.create_measurement(net, 'p', 'bus', -mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
        pp.create_measurement(net, 'q', 'bus', mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
        i = i+ 1


    pp.create_measurement(net, 'v', 'bus', 1 , 0.0004, element = 0)
    pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 1)
    pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 21)

    for busi in [3, 22, 1, 47, 26]:
        pp.create_measurement(net, 'p', 'bus', 0, .001,  element = busi)

    k = 3
    while k < 64:
        if k not in [21, 25]:
            pp.create_measurement(net, 'q', 'bus', 0, .001,  element = k)
        k = k + 1
    j = j + 1

########################################################OVERALL ESTIMATOR########################################
success = estimate(net, init='flat')
print(success)
net.res_line_est
net.res_bus_est


########################################################ALLOCATE SOME FLEXIBILITY TO ALLEVIATE CONSTRAINTS#####
#INDUSTRIAL
pp.create_measurement(ind_feeder, 'p', 'bus', 0.75, .001,  element = 4)

#COMMERCIAL
pp.create_measurement(comm_feeder, 'p', 'bus', 0.35, .001,  element = 34)

#RESIDENTIAL
pp.create_measurement(res_feeder, 'p', 'bus', 0.02, .001,  element = 11)
pp.create_measurement(res_feeder, 'p', 'bus', 0.03, .001,  element = 17)

#MIXED
pp.create_measurement(mixed_feeder, 'p', 'bus', 0.45, .001,  element = 58)

#####INDUSTRIAL ESTIMATOR#########
successi = estimate(ind_feeder, init='flat')
print(successi)

#####RESIDENTIAL ESTIMATOR########
successr = estimate(res_feeder, init='flat')
print(successr)

#####COMMERCIAL ESTIMATOR#########
successc = estimate(comm_feeder, init='flat')
print(successc)

#####MIXED ESTIMATOR##############
successrc = estimate(mixed_feeder, init='flat')
print(successrc)


#################################################SET UP MEASUREMENTS FOR OVERALL FEEDER########################
j = 0
while j < 1:
    ##RESIDENTIAL
    i = 0
    while i < len(res_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', res_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+3)
        pp.create_measurement(net, 'p', 'bus', -res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
        pp.create_measurement(net, 'q', 'bus', res_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+3)
        i = i+ 1

    ##INDUSTRIAL
    i = 0
    while i < len(ind_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', ind_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+22)
        pp.create_measurement(net, 'p', 'bus', -ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
        pp.create_measurement(net, 'q', 'bus', ind_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+22)
        i = i+ 1

    ##COMMERCIAL
    i = 0
    while i < len(comm_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', comm_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+26)
        pp.create_measurement(net, 'p', 'bus', -comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
        pp.create_measurement(net, 'q', 'bus', comm_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+26)
        i = i+ 1

    ##MIXED
    i = 0
    while i < len(mixed_feeder.res_bus_est):
        pp.create_measurement(net, 'v', 'bus', mixed_feeder.res_bus_est.vm_pu[i] , 0.0004, element = i+47)
        pp.create_measurement(net, 'p', 'bus', -mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
        pp.create_measurement(net, 'q', 'bus', mixed_feeder.res_bus_est.p_mw[i] , 0.0010, element = i+47)
        i = i+ 1


    pp.create_measurement(net, 'v', 'bus', 1 , 0.0004, element = 0)
    pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 1)
    pp.create_measurement(net, 'v', 'bus', np.random.normal(1, 0.0004), .0004,  element = 21)

    for busi in [3, 22, 1, 47, 26]:
        pp.create_measurement(net, 'p', 'bus', 0, .001,  element = busi)

    k = 3
    while k < 64:
        if k not in [21, 25]:
            pp.create_measurement(net, 'q', 'bus', 0, .001,  element = k)
        k = k + 1
    j = j + 1

########################################################OVERALL ESTIMATOR########################################
success = estimate(net, init='flat')
print(success)
net.res_line_est
net.res_bus_est
