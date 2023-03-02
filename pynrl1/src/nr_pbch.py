
# 38.211 7.4.3 SS/PBCH block

import numpy as np

from pynrl1.util.nr_prbs import nr_prbs
from pynrl1.util.nr_mapper import nr_mapper

def nr_pbch(ncellid, v, databits):

    assert ncellid <= 1007 and ncellid >= 0
    assert v >= 0 and v <= 7

    n = len(databits)

    # Scrambling, Section 7.3.3.1, TS 38.211
    prbs_bits = nr_prbs(ncellid, v*n+n)
    prbs_bits = prbs_bits[-n:]
    scrambled_bits = np.bitwise_xor(databits, prbs_bits)

    # Modulation, Section 7.3.3.2, TS 38.211
    return nr_mapper(scrambled_bits, 'QPSK')
