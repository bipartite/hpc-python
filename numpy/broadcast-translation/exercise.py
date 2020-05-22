import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("points_circle.dat")
print(data, data.shape)


v = np.array([2.4, 1.5]).reshape(1,2)
print(v)
rot = data * v
print(rot, rot.shape)

plt.plot(data[:,0], data[:,1], 'o')
plt.plot(rot[:,0], rot[:,1], 'x')
plt.show()