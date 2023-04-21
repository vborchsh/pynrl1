
# 38.211 7.4.3 SS/PBCH block

import numpy as np

def nrPBCHIndices(ncellid):
    assert ncellid <= 1007 and ncellid >= 0

    # Indices with windows for SSB
    K = 240
    ind  = list(range(  K,        2*K, 4)) #l = 1, k =   0 ... 236
    ind += list(range(2*K,     2*K+48, 4)) #l = 2, k =   0 ...  44
    ind += list(range(2*K+192,    3*K, 4)) #l = 2, k = 192 ... 236
    ind += list(range(3*K,        4*K, 4)) #l = 3, k =   0 ... 236

    # 3 indices for PBCH within groups of 4, depending on DMRS shift
    v_indices = ncellid % 4
    if v_indices == 0:
        dmrs_ind = [1, 2, 3]
    elif v_indices == 1:
        dmrs_ind = [0, 2, 3]
    elif v_indices == 2:
        dmrs_ind = [0, 1, 3]
    elif v_indices == 3:
        dmrs_ind = [0, 1, 2]

    # Compile DMRS+PBCH indices
    res_ind = [j for x in ind for j in [x+dmrs_ind[0], x+dmrs_ind[1], x+dmrs_ind[2]]]

    return np.array(res_ind)
