from mpi4py import MPI
import numpy as np
from sys import stdout

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

assert size == 4, 'Number of MPI tasks has to be 4.'

if rank == 0:
    print('First collective:')

# create data vector at task 0 and send it to everyone else
#       using collective communication
if rank == 0:
    data = np.arange(8, dtype=int)
else:
    data = np.empty(8, int)

comm.Bcast(data, root=0)
print('  Task {0}: {1}'.format(rank, data))


# Prepare data vectors ..
start = rank * 8
end = start + 8
data = np.arange(start, end, step=1, dtype=int)
# .. and receive buffers
buff = np.full(8, -1, int)

# ... wait for every rank to finish ...
stdout.flush()
comm.barrier()
if rank == 0:
    print('')
    print('-' * 32)
    print('')
    print('Data vectors:')
print('  Task {0}: {1}'.format(rank, data))
stdout.flush()
comm.barrier()
if rank == 0:
    print('')
    print('c)')

# how to get the desired receive buffer using a single collective
#       communication routine?
comm.Scatter(data, buff[:2], root=0)

print('  Task {0}: {1}'.format(rank, buff))

# ... wait for every rank to finish ...
buff[:] = -1
stdout.flush()
comm.barrier()
if rank == 0:
    print('')
    print('d)')

# how to get the desired receive buffer using a single collective
#       communication routine?

comm.Gather(data[:2], buff, root=1)
print('  Task {0}: {1}'.format(rank, buff))

# ... wait for every rank to finish ...
buff[:] = -1
stdout.flush()
comm.barrier()
if rank == 0:
    print('')
    print('e)')

# TODO: how to get the desired receive buffer using a single collective
#       communication routine?

color = rank // 2

local_comm = comm.Split(color)
local_rank = local_comm.Get_rank()
print("Global rank: %d Local rank: %d" % (rank, local_rank))

local_comm.Reduce(data, buff, op=MPI.SUM, root=0)
# comm.Reduce(data[], buff, op=MPI.SUM, root=0)

print('  Task {0}: {1}'.format(rank, buff))

