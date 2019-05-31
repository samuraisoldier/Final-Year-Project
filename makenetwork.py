#make  networks


import pandapower as pp
import pandapower.networks as pn
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt

net = pn.create_cigre_network_mv(with_der = 'all')
net
net.line

plot.simple_plot(net, show_plot=True)

#pp.to_excel(netmv, "examplecigre5.xlsx")


netmv = pn.create_cigre_network_lv()
netmv.line


net3 = pp.from_excel("lvtestnet.xlsx")
plot.simple_plot(net3, show_plot=True)

from pandapower.plotting.plotly import vlevel_plotly
vlevel_plotly(net3)

netmv = pn.mv_oberrhein()

pp.runpp(net3)
cmap_list=[(20, "green"), (50, "yellow"), (60, "red")]
cmap, norm = plot.cmap_continous(cmap_list)
lc = plot.create_line_collection(netmv, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)
plot.draw_collections([lc], figsize=(8,6))
cmap_list=[(0.975, "blue"), (1.0, "green"), (1.03, "red")]
cmap, norm = plot.cmap_continous(cmap_list)
bc = plot.create_bus_collection(netmv, net.bus.index, size=80, zorder=2, cmap=cmap, norm=norm)
plot.draw_collections([lc, bc], figsize=(8,6))
