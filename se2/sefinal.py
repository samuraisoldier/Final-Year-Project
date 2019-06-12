import pandas as pd
import numpy as np
import cmath
from ast import literal_eval
from numpy.linalg import inv
from scipy.sparse.linalg import spsolve
from sefn import admit_matrix, small_h, meas_jaco, errcov, front_substitution,back_substitution

 xnet_file = 'sample_net2.xlsx'
lines_sheet = 'lines'
buses_sheet = 'meas'

lines = pd.read_excel(net_file, lines_sheet)
meas = pd.read_excel(net_file, buses_sheet)

no_buses = 3
no_meas = len(meas)
z_meas = list(meas['value'])

#make a complex bus admittance matrix
ad_mat = admit_matrix(no_buses, lines)


x_state = [0.0000]*(no_buses-1) + [1.0000]*no_buses
iter = 0
tol = 5
x_states = {}
x_states[iter] = x_state
dxs = {}
Js = {}
rs = {}
hmats={}
smallhs={}


while tol > 0.01:
    iter = iter + 1
    print(iter)

    #need to build R
    R = np.array(errcov(meas['std_dev']))
    #R

    h_mat = np.array(meas_jaco(meas, no_buses, x_state, lines, ad_mat, no_meas))
    h_mat_t = h_mat.T
    gainmat = np.dot(np.dot(h_mat_t, inv(R)), h_mat)

    L_mat = np.linalg.cholesky(gainmat)
    L_mat_t = L_mat.T

    #tk = h_mat_t*inv(R)*r
    h_meas = np.array(small_h(meas, no_meas, x_state, lines, ad_mat, no_buses))
    #h_meas
    r = np.subtract(z_meas, h_meas)
    #r
    tk = np.dot(np.dot(h_mat_t, inv(R)), r)
    #tk

    u_mat = front_substitution(L_mat, tk)
    #u_mat
    dx = back_substitution(L_mat_t,u_mat)
    #dx = spsolve(gainmat, tk)
    #dx

    x_state = x_state + dx

    J = np.dot(np.dot(r.T, inv(R)), r)

    Js[iter] = J
    hmats[iter] = h_mat
    x_states[iter] = x_state
    dxs[iter] = dx
    smallhs[iter] = h_meas
    rs[iter] = r
    print(abs(max(dx)))

    tol = abs(max(dx))

results = {}
results['Bus'] = [1,2,3]
results['Voltages (pu)'] = [x_state[2], x_state[3], x_state[4]]
results['Angles (degrees)'] = [0] + [np.degrees(x_state[0]), np.degrees(x_state[1])]
res= pd.DataFrame(results).set_index('Bus')
res

#vm_pu	va_degree	p_mw	q_mvar
#0	1.005994	0.000000	-2.240295	-1.766743
#1	0.968006	-1.237732	0.634443	0.700324
#2	0.941750	-2.708246	1.538518	0.887710


x_states
Js
dxs

rs
smallhs


h_jaco = [[-30, 0, 10 ,-10, 0],
        [0,-17.2,6.9, 0, -6.9 ],
        [40.9, -10.9, -10, 14.1, -4.1],
        [10, 0, 30, -30, 0],
        [0, 6.9, 17.2, 0, -17.2],
        [-14.1, 4.1, -30, 40.9, -10.9],
        [0, 0, 1, 0 , 0],
        [0,0,0,1,0]
        ]


r = np.subtract[z_meas, h_meas]
