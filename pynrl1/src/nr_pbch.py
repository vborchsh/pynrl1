
# 38.211 7.4.3 SS/PBCH block

import numpy as np

from pynrl1.util.nr_prbs import nr_prbs
from pynrl1.util.nr_mapper import nr_mapper

def nr_pbch(ncellid, v, databits):

    n = len(databits)

    assert ncellid <= 1007 and ncellid >= 0
    assert v >= 0 and v <= 7
    assert n > 0

    # Scrambling, Section 7.3.3.1, TS 38.211
    prbs_bits = nr_prbs(ncellid, v*n+n)
    prbs_bits = prbs_bits[-n:]
    scrambled_bits = np.bitwise_xor(databits, prbs_bits)

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

    # Modulation, Section 7.3.3.2, TS 38.211
    res_sym = nr_mapper(scrambled_bits, 'QPSK')

    return np.array(res_ind), np.array(res_sym)
