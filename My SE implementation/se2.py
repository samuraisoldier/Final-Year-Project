import pandas as pd
import numpy as np
import cmath
from ast import literal_eval
from numpy.linalg import inv
from scipy.sparse.linalg import spsolve
#import sefn
from sefn import admit_matrix, small_h, meas_jaco, errcov, front_substitution,back_substitution

net_file = 'sample_net2.xlsx'
lines_sheet = 'lines'
buses_sheet = 'meas'

lines = pd.read_excel(net_file, lines_sheet)
meas = pd.read_excel(net_file, buses_sheet)

no_buses = 3
no_meas = len(meas)


#make a complex bus admittance matrix
ad_mat = admit_matrix(no_buses, lines)
ad_mat

x_state = [0]*(no_buses-1) + [1]*no_buses
x_state
iter = 0
tol = 5
z_meas = list(meas['value'])
z_meas


x_states = {}
dxs = {}

#while tol > 0.0001:
while iter < 2:
    print(iter)
    h_meas = np.array(small_h(meas, no_meas, x_state, lines, ad_mat, no_buses))

    #h_meas

    #work out measurement Jacobian
    h_mat = np.array(meas_jaco(meas, no_buses,x_state, lines, ad_mat, no_meas))
    h_mat_t = h_mat.T
    #h_mat


    #need to build R
    R = errcov(meas['std_dev'])
    #R



    gainmat = np.dot(np.dot(h_mat_t, inv(R)), h_mat)
    gainmat107 = np.around(gainmat/(10**7), 4)
    #gainmat107
    #np.linalg.eigvals(gainmat)/10**7

    L_mat = np.around(np.linalg.cholesky(gainmat), 4)
    #L_mat/10**3
    L_mat_t = L_mat.T


    #make r
    r = [round(a-b,4) for a, b in zip(z_meas,h_meas)]
    #r


    #tk = h_mat_t*inv(R)*r
    tk = np.dot(np.dot(h_mat_t, inv(R)), r)
    #tk

    u_mat = front_substitution(L_mat, tk)
    #u_mat
    dx = back_substitution(L_mat_t,u_mat)
    #dx

    dxs[iter] = dx
    x_states[iter] = x_state

    x_state = x_state + dx

    print(abs(max(dx)))

    iter = iter + 1
    tol = abs(max(dx))


x_state
iter

x_states[1]
dxs[1]

L_mat

tk
