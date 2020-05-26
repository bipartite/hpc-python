from __future__ import print_function
import numpy as np
import time
from mpi4py import MPI

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from evolve import evolve

# Set the colormap
plt.rcParams['image.cmap'] = 'BrBG'

# Basic parameters
a = 0.5                # Diffusion constant
timesteps = 200        # Number of time-steps to evolve system
image_interval = 4000  # Write frequency for png files

# Grid spacings
dx = 0.01
dy = 0.01
dx2 = dx**2
dy2 = dy**2

# For stability, this is the largest interval possible
# for the size of the time-step:
dt = dx2*dy2 / ( 2*a*(dx2+dy2) )

# MPI globals
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Up/down neighbouring MPI ranks
up = rank - 1
down = rank + 1
# if at the edge of the grid, use MPI.PROC_NULL
if up < 0:
    up = MPI.PROC_NULL
if down > size - 1:
    down = MPI.PROC_NULL


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

def exchange(field):
    # select border rows from the field and add MPI calls to
    # exchange them with the neighbouring tasks
    # send down, receive from up
    sbuf = field[-2,:]  # last row of real data
    rbuf = field[0,:]  # ghost row
    comm.Sendrecv(sbuf, dest=down, recvbuf=rbuf, source=up)
    # send up, receive from down
    sbuf = field[1,:]  # first row of real data
    rbuf = field[-1,:]  # ghost row
    comm.Sendrecv(sbuf, dest=up, recvbuf=rbuf, source=down)

def iterate(field, local_field, local_field0, timesteps, image_interval):
    for m in range(1, timesteps+1):
        exchange(local_field0)
        evolve(local_field, local_field0, a, dt, dx2, dy2)
        if m % image_interval == 0:
            # gather partial fields to reconstruct the full field
            comm.Gather(local_field[1:-1,:], field, root=0)
            if rank == 0:
                write_field(field, m)


def main():
    # Read and scatter the initial temperature field
    if rank == 0:
        field, field0 = init_fields('bottle_large.dat')
        shape = field.shape
        dtype = field.dtype
        # send the shape and dtype to everyone else
        comm.bcast(shape, 0)
        comm.bcast(dtype, 0)
    else:
        field = None
        # receive the shape and dtype
        shape = comm.bcast(None, 0)
        dtype = comm.bcast(None, 0)
    if shape[0] % size:
        raise ValueError('Number of rows in the temperature field (' \
                + str(shape[0]) + ') needs to be divisible by the number ' \
                + 'of MPI tasks (' + str(size) + ').')
    n = int(shape[0] / size)  # number of rows for each MPI task
    m = shape[1]         # number of columns in the field

    # scatter a portion of the field to each MPI task
    buff = np.zeros((n, m), dtype=dtype) # receive buffer for (n,m) elements of dtype
    comm.Scatter(field, buff, 0)

    # construct local field based on the received data
    # Note: remember to add two ghost rows (one on each side)
    local_field = np.zeros((n+2, m), dtype=dtype)
    local_field[1:-1,:] = buff

    local_field0 = np.zeros_like(local_field)  # array for previous time step
    # Fix outer boundary ghost layers to account for aperiodicity?
    if True:
        if rank == 0:
            local_field[0,:] = local_field[1,:]
        if rank == size - 1:
            local_field[-1,:] = local_field[-2,:]
    local_field0[:] = local_field[:]

    # Plot/save initial field
    if rank == 0:
        write_field(field, 0)
    # Iterate
    t0 = time.time()
    iterate(field, local_field, local_field0, timesteps, image_interval)
    t1 = time.time()
    # Plot/save final field
    # gather partial fields to reconstruct the full field
    comm.Gather(local_field[1:-1,:], field, root=0)
    if rank == 0:
        write_field(field, timesteps)
        print("Running time: {0}".format(t1-t0))

if __name__ == '__main__':
    main()
