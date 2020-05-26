from mpi4py import MPI
from numpy import arange, zeros
from sys import stdout

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = arange(10, dtype=float) * (rank + 1)
buffer = zeros(size * 10, float)

n = comm.gather(rank, root=0)     # returns the value
comm.Gather(data, buffer, root=0) # in-place modification

print(f'Rank {rank}: send     data {data}')
print(f'Rank {rank}: received data {buffer} and n {n}')
# print(f'{buffer.shape}')

stdout.flush()
comm.barrier()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = arange(10 * size, dtype=float) * (rank + 1)
buffer = zeros(size * 10, float)

n = comm.reduce(rank, op=MPI.SUM, root=0) # returns the value

comm.Reduce(data, buffer, op=MPI.SUM, root=0) # in-place modification

print(f'Rank {rank}: send     data {data[1]}')
print(f'Rank {rank}: received sum {buffer} and n {n}')
print(f'{buffer.shape}')