
import numpy as np

from pynrl1.util.nr_prbs import nr_prbs
from pynrl1.util.nr_mapper import nr_mapper


def nr_pbch_dmrs(ncellid, issb):

    assert ncellid >= 0 and ncellid <= 1007
    assert issb >= 0 and issb <= 7

    # Get DMRS sequence
    cinit = nr_pbch_dmrs_cinit(issb, ncellid)
    prbs = nr_prbs(cinit, 2*144)

    # Indices with window for SSS
    K = 240
    ind  = list(range(  K,        2*K, 4)) #l = 1, k =   0 ... 236
    ind += list(range(2*K,     2*K+48, 4)) #l = 2, k =   0 ...  44
    ind += list(range(2*K+192,    3*K, 4)) #l = 2, k = 192 ... 236
    ind += list(range(3*K,        4*K, 4)) #l = 3, k =   0 ... 236

    # DMRS indices shift by "v"
    ind = np.array(ind)+(ncellid % 4)

    # Convert sequence to symbols and merge with indices
    return [ind, nr_mapper(prbs, 'qpsk')]


def nr_pbch_dmrs_cinit(issb, ncellid):
    return 2**11 * (issb + 1) * (ncellid//4 + 1) + 2**6 * (issb + 1) + (ncellid % 4)