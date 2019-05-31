import pandapower as pp
import pandapower.networks as pn
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt
from pandapower.plotting.plotly import vlevel_plotly
import pandas as pd


net = pn.create_cigre_network_lv()
net
plot.simple_plot(net, show_plot=True)


vlevel_plotly(net)


#del net.bus_geodata
pp.convert_format(net)
pp.to_excel(net, "examplecigrelow.xlsx")

netcoords = net.bus_geodata
netcoords.to_excel('cigrecoords.xlsx')


netlv = pp.from_excel("final code/examplecigrelow.xlsx")
#lv.bus_geodata
#del netlv.bus_geodata
netlv
plot.simple_plot(netlv, show_plot=True)
vlevel_plotly(netlv)

#vlevel_plotly(net)
netlv
net
netlv.bus_geodata
