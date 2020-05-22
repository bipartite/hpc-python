from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
    void evolve(double *u, double *u_previous, int nx, int ny, double a, double dt, double dx2, double dy2);   // list all the function prototypes from the
                """)

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("_my_cheat",
"""
    #include "evolve.h"
""",
   sources = ['evolve.c'],
   library_dirs = [],
   libraries = []   # if mymath utilizes math library we need to include it
                       # here
)

ffibuilder.compile(verbose=True)
