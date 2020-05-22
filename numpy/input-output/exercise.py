import numpy as np

args = {
    'header': 'XY coordinates y+2.5',
    'fmt': '%7.3f',
    'delimiter': ','
}

data = np.loadtxt("xy-coordinates.dat")

print(data)

data[:,1] += 2.5 
print(data)

np.savetxt('output.dat', data, **args)