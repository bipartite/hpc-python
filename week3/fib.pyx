def fibonacci1(x):
    if x < 2:
        return x
    else:
        return fibonacci1(x-1) + fibonacci1(x-2)



def fibonacci2(int x):
    if x < 2:
        return x
    else:
        return fibonacci2(x-1) + fibonacci2(x-2)


cpdef int fibonacci3(int x):
    if x < 2:
        return x
    else:
        return fibonacci3(x-1) + fibonacci3(x-2)