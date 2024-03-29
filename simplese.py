import pandapower as pp
#import pandapower.networks as pn
import pandas as pd
from pandapower.estimation import estimate


%%time
net = pp.from_excel("final code/circuits/net3.xlsx")

net.measurement = pd.read_excel('final code/measurements/net_m.xlsx')


succes = estimate(net, init='flat')
print(succes)
net.res_line_est
net.res_bus_est
net.res_line_est.to_excel('final code/result/line_simp.xlsx')
net.res_bus_est.to_excel('final code/result/bus_simp.xlsx')
