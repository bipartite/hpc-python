
from mpi4py import MPI
import numpy as np
from sys import stdout

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

aloc = np.empty(16)
# a = np.zeros(16)

if rank == 0:
    a = np.arange(16)

a = comm.bcast(a, root=0)

comm.Alltoall(a, aloc)
if rank == 0:
    print(f'{rank} aloc {aloc}')