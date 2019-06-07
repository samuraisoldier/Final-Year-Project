import pandas as pd
import numpy as np
import cmath
from ast import literal_eval
from numpy.linalg import inv
from scipy.sparse.linalg import spsolve


def errcov(m):
    errcov = []
    for i in range(len(m)):
        row = []
        for j in range(8):
                if i == j:
                    row.append(m[i] * m[i])
                else:
                    row.append(0)
        errcov.append(row)
    errcov = np.array(errcov)
    return errcov


def front_substitution(L: np.ndarray, tk: np.ndarray) -> np.ndarray:
    n = tk.size
    u = np.zeros_like(tk)

    for i in range(0,n,1):
        u[i] = tk[i]
        for j in range(0, i, 1):
            u[i] -= L[i, j]*u[j]
        u[i] /= L[i,i]

    return u

def back_substitution(L: np.ndarray, u: np.ndarray) -> np.ndarray:
    n = u.size
    x = np.zeros_like(u)

    for i in range(n-1, -1, -1):
        x[i] = u[i]
        for j in range(n-1, i, -1):
           x[i] -= L[i, j]*x[j]
        x[i] /= L[i,i]

    return x


def meas_jaco(meas, no_buses, x_state, lines, ad_mat, no_meas):
    h_jaco = []
    for k in range(len(meas)):
        if meas['measurement_type'][k] == 'p':
            if meas['element_type'][k] == 'line':
                row = []
                buses = literal_eval(meas['buses_tf'][k])
                for i in range(no_buses):
                    #do angles, skip 0 - reference angle
                    if i == 0:
                        row.append(0)# do nothing
                    elif i+1 in buses:
                        ind1 = buses[0]
                        ind2 = buses[1]
                        vi=x_state[ind1+1]
                        vj=x_state[ind2+1]
                        gij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['R'][0]
                        if ind1 == 1:
                            thetai = 0
                        else:
                            thetai= x_state[ind1-2]
                        thetaj=x_state[ind2-2]
                        thetaij=thetai-thetaj
                        bij=lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] ==ind2].reset_index(drop = True)['X'][0]
                        ans = 1000 * vi * vj * (gij*np.sin(np.radians(thetaij)) - bij*np.cos(np.radians(thetaij)))
                        row.append(ans)
                    else:
                        row.append(0)
                #do voltages
                ind1 = buses[0]
                ind2 = buses[1]
                vi=x_state[ind1+1]
                vj=x_state[ind2+1]
                gij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['R'][0]
                if ind1 == 1:
                    thetai = 0
                else:
                    thetai= x_state[ind1-2]
                thetaj=x_state[ind2-2]
                thetaij=thetai-thetaj
                bij=lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['X'][0]
                ans1 = 1000 * (-1*vj * (gij*np.cos(np.radians(thetaij)) - bij*np.sin(np.radians(thetaij))) + 2 * gij * vi)
                ans2 = 1000 * (-1*vi * (gij*np.cos(np.radians(thetaij)) - bij*np.sin(np.radians(thetaij))))
                ansrow = [0]*3
                ansrow[ind1-1] = round(ans1,2)
                ansrow[ind2-1] = round(ans2,2)
                row = row + ansrow
                del row[0]
                h_jaco.append(row)

            elif meas['element_type'][k] == 'bus':
                row = [0]*5
                #first do angles
                #need to grab from admittance Matrix
                bus = meas['element'][k]
                vi=x_state[bus+1]
                ans = 0
                ad_row = ad_mat[bus-1]
                for j in range(no_buses):
                    vj=x_state[j+1]
                    Gij=ad_row[j].real
                    if j == 0:
                        thetaj = 0
                    else:
                        thetaj= x_state[j-2]
                    thetai=x_state[bus-2]
                    thetaij=thetai-thetaj
                    Bij=ad_row[j].imag
                    ans = ans + (vi * vj * (-Gij*np.sin(np.radians(thetaij)) + Bij*np.cos(np.radians(thetaij))))
                row[0]=round(ans-vi * ad_row[1].imag,2)
                thetaij = x_state[1]-x_state[0]
                Gij=ad_row[2].real
                Bij=ad_row[2].imag
                row[1] = round(vi * x_state[4]*(Gij*np.sin(np.radians(thetaij))-Bij*np.cos(np.radians(thetaij))),2)

                #time for voltages
                for i in range(no_buses):
                    if i == 1:
                        ans = 0
                        vi = x_state[3]
                        for j in range(no_buses):
                            vj=x_state[j+2]
                            Gij=ad_row[j].real
                            if j == 0:
                                thetaj = 0
                            else:
                                thetaj= x_state[j-1]
                            thetai=x_state[0]
                            thetaij=thetai-thetaj
                            Bij=ad_row[j].imag
                            ans = ans + (vj * (-Gij*np.sin(np.radians(thetaij)) + Bij*np.cos(np.radians(thetaij))))
                        row[3] = round(ans + vi*ad_row[i].real,2)
                    else:
                        if i == 0:
                            thetaj = 0
                        else:
                            thetaj = x_state[i-1]
                        thetaij = x_state[0]-thetaj
                        vi =  x_state[bus+1]
                        Gij=ad_row[i].real
                        Bij=ad_row[i].imag
                        row[i+2] = round(vi * (Gij*np.cos(np.radians(thetaij))+Bij*np.sin(np.radians(thetaij))),2)


                h_jaco.append(row)
        elif meas['measurement_type'][k] == 'q':
            if meas['element_type'][k] == 'line':
                row = []
                buses = literal_eval(meas['buses_tf'][k])
                for i in range(no_buses):
                    #do angles, skip 0 - reference angle
                    if i == 0:
                        row.append(0)# do nothing
                    elif i+1 in buses:
                        ind1 = buses[0]
                        ind2 = buses[1]
                        vi=x_state[ind1+1]
                        vj=x_state[ind2+1]
                        gij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['R'][0]
                        if ind1 == 1:
                            thetai = 0
                        else:
                            thetai= x_state[ind1-2]
                        thetaj=x_state[ind2-2]
                        thetaij=thetai-thetaj
                        bij=lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] ==ind2].reset_index(drop = True)['X'][0]
                        ans =1000* vi * vj * (gij*np.cos(np.radians(thetaij)) + bij*np.sin(np.radians(thetaij)))
                        row.append(round(ans,2))
                    else:
                        row.append(0)
                #do voltages
                ind1 = buses[0]
                ind2 = buses[1]
                vi=x_state[ind1+1]
                vj=x_state[ind2+1]
                gij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['R'][0]
                if ind1 == 1:
                    thetai = 0
                else:
                    thetai= x_state[ind1-2]
                thetaj=x_state[ind2-2]
                thetaij=thetai-thetaj
                bij=lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['X'][0]
                ans1 = 1000 * (-vj * (gij*np.sin(np.radians(thetaij)) - bij*np.cos(np.radians(thetaij))) - 2 * bij * vi)
                ans2 = 1000 * (-vi * (gij*np.sin(np.radians(thetaij)) - bij*np.cos(np.radians(thetaij))))
                ansrow = [0]*3
                ansrow[ind1-1] = round(ans1,2)
                ansrow[ind2-1] = round(ans2,2)
                row = row + ansrow
                del row[0]
                h_jaco.append(row)

            elif meas['element_type'][k] == 'bus':
                row = [0]*5
                #first do angles
                #need to grab from admittance Matrix
                bus = meas['element'][k]
                vi=x_state[bus+1]
                ans = 0
                ad_row = ad_mat[bus-1]
                for j in range(no_buses):
                    vj=x_state[j+2]
                    Gij=ad_row[j].real
                    if j == 0:
                        thetaj = 0
                    else:
                        thetaj= x_state[j-1]
                    thetai=x_state[bus-2]
                    thetaij=thetai-thetaj
                    Bij=ad_row[j].imag
                    ans = ans + (vi * vj * (Gij*np.cos(np.radians(thetaij)) + Bij*np.sin(np.radians(thetaij))))
                row[0]=round(ans-vi *vi* ad_row[1].real,2)
                thetaij = x_state[1]-x_state[0]
                Gij=ad_row[2].real
                Bij=ad_row[2].imag
                row[1] = round(vi * x_state[4]*(-Gij*np.cos(np.radians(thetaij))-Bij*np.sin(np.radians(thetaij))),2)

                #time for voltages
                for i in range(no_buses):
                    if i == 1:
                        ans = 0
                        vi = x_state[3]
                        for j in range(no_buses):
                            vj=x_state[j+2]
                            Gij=ad_row[j].real
                            if j == 0:
                                thetaj = 0
                            else:
                                thetaj= x_state[j-1]
                            thetai=x_state[0]
                            thetaij=thetai-thetaj
                            Bij=ad_row[j].imag
                            ans = ans + (vj * (Gij*np.sin(np.radians(thetaij)) - Bij*np.cos(np.radians(thetaij))))
                        row[3] = round(ans - vi*ad_row[i].imag,2)
                    else:
                        if i == 0:
                            thetaj = 0
                        else:
                            thetaj = x_state[i-1]
                        thetaij = x_state[0]-thetaj
                        vi =  x_state[bus+1]
                        Gij=ad_row[i].real
                        Bij=ad_row[i].imag
                        row[i+2] = round(vi * (Gij*np.sin(np.radians(thetaij))-Bij*np.cos(np.radians(thetaij))),2)
                h_jaco.append(row)

        elif meas['measurement_type'][k] == 'v':
            bus = meas['element'][k]
            row = [0]*5
            row[bus+1] = 1.0
            h_jaco.append(row)
            #by default voltage is just bus
    return h_jaco


def small_h(meas, no_meas, x_state, lines, ad_mat, no_buses):
    h_meas = [0]*no_meas

    for k in range(no_meas):
        if meas['measurement_type'][k] == 'p':
            if meas['element_type'][k] == 'line':
                buses = literal_eval(meas['buses_tf'][k])
                ind1 = buses[0]
                ind2 = buses[1]
                vi=x_state[ind1+1]
                vj=x_state[ind2+1]
                gij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['R'][0]
                bij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['X'][0]
                if ind1 == 1:
                    thetai = 0
                else:
                    thetai= x_state[ind1-2]
                thetaj=x_state[ind2-2]
                thetaij=thetai-thetaj
                h_meas[k] =  round(vi**2 * gij - (vi * vj * (gij*np.cos(np.radians(thetaij)) + bij*np.sin(np.radians(thetaij)))),4)

            elif meas['element_type'][k] == 'bus':
                bus = meas['element'][k]
                vi=x_state[bus+1]
                thetai=x_state[bus-2]
                ans = 0
                ad_row = ad_mat[bus-1]
                for j in range(no_buses):
                    if j == bus -1:
                        h_meas[k] = h_meas[k] + 0
                    else:
                        vj=x_state[j+1]
                        Gij=ad_row[j].real
                        Bij=ad_row[j].imag
                        if j == 0:
                            thetaj = 0
                        else:
                            thetaj= x_state[j-1]
                        thetaij=thetai-thetaj
                        h_meas[k] += (vj * (Gij*np.cos(np.radians(thetaij)) + Bij*np.sin(np.radians(thetaij))))
                h_meas[k] = round(vi*h_meas[k],4)
        elif meas['measurement_type'][k] == 'q':
            if meas['element_type'][k] == 'line':
                buses = literal_eval(meas['buses_tf'][k])
                ind1 = buses[0]
                ind2 = buses[1]
                vi=x_state[ind1+1]
                vj=x_state[ind2+1]
                gij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['R'][0]
                bij= lines.loc[lines['from_bus'] == ind1].reset_index(drop = True).loc[lines['to_bus'] == ind2].reset_index(drop = True)['X'][0]
                if ind1 == 1:
                    thetai = 0
                else:
                    thetai= x_state[ind1-2]
                thetaj=x_state[ind2-2]
                thetaij=thetai-thetaj
                h_meas[k] =  round(-vi**2 * bij - (vi * vj * (gij*np.sin(np.radians(thetaij)) - bij*np.cos(np.radians(thetaij)))),4)
            elif meas['element_type'][k] == 'bus':
                bus = meas['element'][k]
                vi=x_state[bus+1]
                thetai=x_state[bus-2]
                ad_row = ad_mat[bus-1]
                for j in range(no_buses):
                    if j == bus -1:
                        h_meas[k] = h_meas[k] + 0
                    else:
                        vj=x_state[j+1]
                        Gij=ad_row[j].real
                        Bij=ad_row[j].imag
                        if j == 0:
                            thetaj = 0
                        else:
                            thetaj= x_state[j-1]
                        thetaij=thetai-thetaj
                        h_meas[k]  += (vj * (Gij*np.sin(np.radians(thetaij)) - Bij*np.cos(np.radians(thetaij))))
                h_meas[k] = round(vi*h_meas[k],4)


        elif meas['measurement_type'][k] == 'v':
            h_meas[k] = round(1,4)

    return h_meas

def admit_matrix(no_buses, lines):
    ad_mat = []
    for i in range(no_buses):
        lines_sub = lines.loc[lines['from_bus'] == (i+1)].reset_index(drop = True)
        yvals = []
        for j in range(no_buses):
            if i == j:
                yvals.append(0)
            else:
                this_line = lines_sub.loc[lines_sub['to_bus'] == (j+1)].reset_index(drop = True)
                r_val = this_line['R']
                x_val = this_line['X']
                if ((r_val[0] + x_val[0])==0):
                    yvals.append(0)
                else:
                    val = -1/(complex(r_val[0], x_val[0]))
                    yvals.append(complex(round(val.real,2),round(val.imag,2)))
        ad_mat.append(yvals)
        rowsum = -sum(ad_mat[i])
        ad_mat[i][i] = complex(round(rowsum.real,2),round(rowsum.imag,2))
    return ad_mat
