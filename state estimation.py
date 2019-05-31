from pandapower.estimation import estimate
import pandapower as pp
from pandapower.estimation import remove_bad_data
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt
from pf_res_est_plotly import pf_res_est_plotly
from pandapower.plotting.plotly import pf_res_plotly
import pandas as pd

net = pp.create_empty_network()

b1 = pp.create_bus(net, name="bus 1", vn_kv=1., index=1)
b2 = pp.create_bus(net, name="bus 2", vn_kv=1., index=2)
b3 = pp.create_bus(net, name="bus 3", vn_kv=1., index=3)

pp.create_ext_grid(net, 3)  # set the slack bus to bus 1

l1 = pp.create_line_from_parameters(net, 1, 2, 1, r_ohm_per_km=.01, x_ohm_per_km=.03, c_nf_per_km=0., max_i_ka=1)
l2 = pp.create_line_from_parameters(net, 1, 3, 1, r_ohm_per_km=.02, x_ohm_per_km=.05, c_nf_per_km=0., max_i_ka=1)
l3 = pp.create_line_from_parameters(net, 2, 3, 1, r_ohm_per_km=.03, x_ohm_per_km=.08, c_nf_per_km=0., max_i_ka=1)

net

pp.create_measurement(net, "v", "bus", 1.006, .004, element=b1)        # V at bus 1
pp.create_measurement(net, "v", "bus", 0.968, .004, element=b2)        # V at bus 2
pp.create_measurement(net, "p", "bus", -0.501, .0010, element=b2)         # P at bus 2
pp.create_measurement(net, "q", "bus", -0.286, .0010, element=b2)         # Q at bus 2
pp.create_measurement(net, "p", "line", 0.888, .008, element=l1, side=b1)    # Pline (bus 1 -> bus 2) at bus 1
pp.create_measurement(net, "p", "line", 1.173, .008, element=l2, side=b1)   # Pline (bus 1 -> bus 3) at bus 1
pp.create_measurement(net, "q", "line", 0.568, .008, element=l1, side=b1)    # Qline (bus 1 -> bus 2) at bus 1
pp.create_measurement(net, "q", "line", 0.663, .008, element=l2, side=b1)    # Qline (bus 1 -> bus 3) at bus 1
net.measurement


success = estimate(net, init='flat')
print(success)


pp.runpp(net, calculate_voltage_angles=True, init="dc")


plot.simple_plot(net, show_plot=True)
pf_res_est_plotly(net)
pf_res_plotly(net)
net
net.bus

net.res_bus = net.res_bus_est
net.res_bus
net.res_bus_est.set_index(pd.Index([1,2,3]))

net.line

net.res_line_est
net.res_line
net.res_line = net.res_line_est

net.measurement
net.res_ext_grid




net
import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot
from pandapower.plotting.plotly import simple_plotly
%matplotlib inline

cmap_list=[(20, "green"), (50, "yellow"), (60, "red")]
cmap, norm = plot.cmap_continous(cmap_list)
lc = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)
plot.draw_collections([lc], figsize=(8,6))
plot.simple_plot(net, show_plot=True, trafo_size = 1.5, plot_loads = True, plot_sgens = True)
simple_plotly(net,respect_switches=True )
