import numpy as np
from pynrl1.util.nr_prbs import nr_prbs
from pynrl1.util.nr_mapper import nr_mapper

def nrPBCHDMRS(ncellid, issb):
    assert ncellid >= 0 and ncellid <= 1007
    assert issb >= 0 and issb <= 7

    # Get DMRS sequence
    cinit = nr_pbch_dmrs_cinit(issb, ncellid)
    prbs = nr_prbs(cinit, 2*144)

    # Convert sequence to symbols and merge with indices
    return nr_mapper(prbs, 'qpsk')


def nr_pbch_dmrs_cinit(issb, ncellid):
    return 2**11 * (issb + 1) * (ncellid//4 + 1) + 2**6 * (issb + 1) + (ncellid % 4)