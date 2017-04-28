import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sp
from scipy.integrate import quadrature as integrate
from scipy.integrate import ode
import time

import numpy.polynomial as legpoly

from warnings import filterwarnings

filterwarnings("ignore")


# x = hv/kT

def getMuGrid(mu_size):
    muVals, weightVals = legpoly.legendre.leggauss(mu_size)
    return muVals
    # if mu_size == 2:
    #     return np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
    # elif mu_size == 4:
    #     return np.array([-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116])
    # elif mu_size == 8:
    #     return np.array([-0.960289856497536, -0.796666477413627, -0.525532409916329, -0.183434642495650, 0.183434642495650, 0.525532409916329, 0.796666477413627, 0.960289856497536])
    # elif mu_size == 16:
    #     return np.array([-0.989400934991650, -0.944575023073233, -0.865631202387832, -0.755404408355003, -0.617876244402644, -0.458016777657227, -0.281603550779259, -0.095012509837637, 0.095012509837637, 0.281603550779259, 0.458016777657227, 0.617876244402644, 0.755404408355003, 0.865631202387832, 0.944575023073233, 0.989400934991650])
    # else:
    #     print("Mu Size not available")
    #     exit(1)

zSize = 100
xSize = 10
muSize = 8

x0 = -1

z0 = -1
zMax = 1

zGrid = np.linspace(z0, zMax, zSize)
muGrid = getMuGrid(muSize)

I = np.zeros((zSize, xSize, muSize))

Xi = 0
# Theta_0 = 0
omega = 0.6
tau = 5
# flip = 1 # Turn Compton on and off

delZ = zGrid[1]-zGrid[0]

def getI(i, j, k):
    if i > zSize - 1:
        if muGrid[k] < 0:
            return 0
        else:
            print("Shouldn't be called")
            exit(1)
    if i < 0:
        if muGrid[k] > 0:
            return 0
        else:
            print("Shouldn't be called")
            exit(1)
    return I[i][j][k]



def alpha(mu, mu_p):
    return 3*(mu*mu_p)**2-mu**2-mu_p**2+3

def beta(mu, mu_p):
    return 5*(mu*mu_p+(mu*mu_p)**3)-3*(mu**3*mu_p-mu*mu_p**3)

def epsilon(mu, mu_p):
    return -3*alpha(mu, mu_p)+8+2*beta(mu, mu_p)-8*mu*mu_p

def n_e(z):
    return (1-z**2)**3

def Temp(z):
    return (1-z**2)

def eta(z, x):
    # T = Temp(z)
    # res = n_e(z)**2/np.sqrt(T)*np.exp(-np.power(10, x)/T)
    res = (1-z**2)**(5.5)*np.exp(-np.power(10, x)/(1-z**2))
    return np.nan_to_num(res)

def weight(mu):
    muVals, weightVals = legpoly.legendre.leggauss(muSize)
    return weightVals

def G(z, x, mu):
    return -tau*n_e(z)/mu

def A(z, x, mu, mu_p):
    return tau*n_e(z)/mu*(3./16.)*(alpha(mu, mu_p))

def F(z, x, mu):
    return eta(z, x)/mu


