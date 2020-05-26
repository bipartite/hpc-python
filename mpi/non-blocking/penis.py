from mpi4py import MPI
import numpy
from sys import stdout

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Send and receive buffers
n = 100000
data = numpy.full(n, rank, int)
buff = numpy.zeros(n, int)

tgt = rank + 1
src = rank - 1
send_tag = tgt
if rank == 0:
    src = MPI.PROC_NULL
if rank == size - 1:
    tgt = MPI.PROC_NULL
    send_tag = 0


req = []
req.append(comm.Isend(data, dest=tgt, tag=send_tag))
req.append(comm.Irecv(buff, source=src, tag=rank))

MPI.Request.waitall(req)

print("Rank %d: sent %d elements to rank %d." % (rank, len(data), tgt))