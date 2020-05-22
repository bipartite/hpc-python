import numpy as np


dx = 0.001

x = np.arange(0, np.pi/2, dx)

x_middle = (x[1:] + x[:-1]) / 2

f = np.sin(x_middle)

S = np.sum(f*dx)

print('Riemann sum:', S)

print('Diff from 1:', np.abs(S-1))
