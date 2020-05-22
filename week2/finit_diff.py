import numpy as np

dx = 0.1

x = np.arange(0, np.pi/2, dx)
print(x)

f =  np.sin(x)


df = (f[2:] - f[:-2]) / (2*dx)

print('df', df)

print('cosx', np.cos(x))

print('diff', np.abs(df - np.cos(x[1:-1])))