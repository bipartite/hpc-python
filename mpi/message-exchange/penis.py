from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = {'myrank': rank}

if rank == 0:
    comm.send(data, dest=1)
    msg = comm.recv(source=1)  
elif rank == 1:
    msg = comm.recv(source=0)
    comm.send(data, dest=0)
print(f'Rank {rank} received data {msg}')
    

## Array

n = 100000
data = np.full(n, rank, int)
buff = np.empty(n, int)

if rank == 0:
    comm.Send([data, 10000, MPI.INT], dest=1)
    comm.Recv([buff, 10000, MPI.INT], source=1)
elif rank == 1:
    comm.Recv([buff, 10000, MPI.INT], source=0)
    comm.Send([data, 10000, MPI.INT], dest=0)

print("Rank %d received an array filled with %ds." % (rank, buff[0]))
