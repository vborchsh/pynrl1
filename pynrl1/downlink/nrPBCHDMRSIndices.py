import numpy as np

def nrPBCHDMRSIndices(ncellid):
    assert ncellid >= 0 and ncellid <= 1007

    # Indices with window for SSS
    K = 240
    ind  = list(range(  K,        2*K, 4)) #l = 1, k =   0 ... 236
    ind += list(range(2*K,     2*K+48, 4)) #l = 2, k =   0 ...  44
    ind += list(range(2*K+192,    3*K, 4)) #l = 2, k = 192 ... 236
    ind += list(range(3*K,        4*K, 4)) #l = 3, k =   0 ... 236

    # DMRS indices shift by "v"
    ind = np.array(ind)+(ncellid % 4)

    return ind
