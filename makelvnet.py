import pandapower as pp
import pandapower.networks as pn
import numpy as np
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandas as pd
from pandapower.plotting.plotly import vlevel_plotly

net = pp.create_empty_network()

##BUSES##

pp.create_bus(net, name='Bus 0', vn_kv=11, type='b', zone = 'CIGRE_LV')
##RESIDENTIAL FEEDER##
pp.create_bus(net, name='Bus R0', vn_kv=11, type='b', zone = 'CIGRE_LV')
for i in range(1, 19):
    pp.create_bus(net, name='Bus R%s' % i, vn_kv=0.4, type='m', zone = 'CIGRE_LV')
##INDUSTRIAL FEEDER##
pp.create_bus(net, name='Bus I0', vn_kv=11, type='b', zone = 'CIGRE_LV')
for i in range(1, 3):
    pp.create_bus(net, name='Bus I%s' % i, vn_kv=0.4, type='m', zone = 'CIGRE_LV')
##COMMERCIAL FEEDER##
pp.create_bus(net, name='Bus C0', vn_kv=11, type='b', zone = 'CIGRE_LV')
for i in range(1, 21):
    pp.create_bus(net, name='Bus C%s' % i, vn_kv=0.4, type='m', zone = 'CIGRE_LV')
##MIXED FEEDER##
pp.create_bus(net, name='Bus RC0', vn_kv=11, type='b', zone = 'CIGRE_LV')
for i in range(1, 21):
    pp.create_bus(net, name='Bus RC%s' % i, vn_kv=0.4, type='m', zone = 'CIGRE_LV')
net.bus


##LINES##
lv_lines = pd.read_excel('final code/examplecigrelow.xlsx', sheet_name ='line', index_col = 0)
lv_lines
net.line = lv_lines
net.line


##TRANSFORMERS##
lv_trans = pd.read_excel('final code/examplecigrelow.xlsx', sheet_name ='line', index_col = 0)
lv_lines
net.line = lv_lines
net.line
