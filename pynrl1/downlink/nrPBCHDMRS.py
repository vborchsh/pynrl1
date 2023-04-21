import numpy as np
from pynrl1.util.nrPRBS import nrPRBS
from pynrl1.util.nrSymbolModulate import nrSymbolModulate

def nrPBCHDMRS(ncellid, issb):
    assert ncellid >= 0 and ncellid <= 1007
    assert issb >= 0 and issb <= 7

    # Get DMRS sequence
    cinit = nr_pbch_dmrs_cinit(issb, ncellid)
    prbs = nrPRBS(cinit, 2*144)

    # Convert sequence to symbols and merge with indices
    return nrSymbolModulate(prbs, 'qpsk')


def nr_pbch_dmrs_cinit(issb, ncellid):
    return 2**11 * (issb + 1) * (ncellid//4 + 1) + 2**6 * (issb + 1) + (ncellid % 4)