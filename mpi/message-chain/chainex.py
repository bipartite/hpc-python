from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

ntasks = comm.Get_size()

n=100
data = np.full(n, rank, int)
buffer = np.empty(data.shape, dtype=data.dtype)

tgt = rank + 1
src = rank - 1

if rank == 0:
    comm.Send(data, dest=tgt)
    print("  Rank %d: sent %d elements to rank %d." % (rank, len(data), tgt))
elif rank == ntasks -1:
    comm.Recv(buffer, source=src)
    print("  Rank %d: received a message from rank %d." % (rank, src))
    print("  Rank %d: received an array filled with %ds." % (rank, buffer[0]))
else:
    comm.Sendrecv(data, dest=tgt, recvbuf=buffer, source=src)
    print("  Rank %d: sent %d elements to rank %d." % (rank, len(data), tgt))
    print("  Rank %d: received a message from rank %d." % (rank, src))
    print("  Rank %d: received an array filled with %ds." % (rank, buffer[0]))


    
