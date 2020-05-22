import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cython
cimport numpy as cnp # Import for NumPY C-API

# Set the colormap
plt.rcParams['image.cmap'] = 'BrBG'

@cython.boundscheck(False)
@cython.wraparound(False)
cdef evolve(u, u_previous, double a, double dt, double dx2, double dy2):
    """Explicit time evolution.
       u:            new temperature field
       u_previous:   previous field
       a:            diffusion constant
       dt:           time step. """

    cdef int n, m
    n, m = u.shape

    cdef cnp.ndarray[cnp.double_t, ndim=2] cnp_u, cnp_u_previous
    #cnp_u = np.empty((n, m), dtype=double)
    cnp_u = u

    #cnp_u_previous = np.empty((n, m), dtype=float)
    cnp_u_previous = u_previous

    cdef int i, j

    for i in range(1, n-1):
        for j in range(1, m-1):
            cnp_u[i, j] = cnp_u_previous[i, j] + a * dt * ( \
             (cnp_u_previous[i+1, j] - 2*cnp_u_previous[i, j] + \
              cnp_u_previous[i-1, j]) / dx2 + \
             (cnp_u_previous[i, j+1] - 2*cnp_u_previous[i, j] + \
                 cnp_u_previous[i, j-1]) / dy2 )
    cnp_u_previous[:] = cnp_u[:]



def iterate1(field, field0, a, dx, dy, timesteps, image_interval):
    """Run fixed number of time steps of heat equation"""

    dx2 = dx**2
    dy2 = dy**2

    # For stability, this is the largest interval possible
    # for the size of the time-step:
    dt = dx2*dy2 / ( 2*a*(dx2+dy2) )    

    for m in range(1, timesteps+1):
        evolve(field, field0, a, dt, dx2, dy2)
        if m % image_interval == 0:
            write_field(field, m)

def init_fields(filename):
    # Read the initial temperature field from file
    field = np.loadtxt(filename)
    field0 = field.copy() # Array for field of previous time step
    return field, field0

def write_field(field, step):
    plt.gca().clear()
    plt.imshow(field)
    plt.axis('off')
    plt.savefig('heat_{0:03d}.png'.format(step))


