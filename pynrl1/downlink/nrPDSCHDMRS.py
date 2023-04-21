
# 38.211

import numpy as np

from pynrl1.util.nrPRBS import nrPRBS
from pynrl1.util.nrSymbolModulate import nrSymbolModulate
from pynrl1.util.nrPDSCHConfig import nrPDSCHConfig
from pynrl1.util.nrCarrierConfig import nrCarrierConfig

def nrPDSCHDMRS(cfg: nrPDSCHConfig, carrier: nrCarrierConfig):
    if cfg.dmrs_conf_type == 1:
        n_dmrs_per_re = 6
    else:
        n_dmrs_per_re = 4
    n_dmrs_bits_re = 2*n_dmrs_per_re

    dmrs_begin = n_dmrs_bits_re * min(cfg.PRB_set)
    dmrs_end = n_dmrs_bits_re * (max(cfg.PRB_set)+1)
    dmrs_size = n_dmrs_bits_re * cfg.n_size_bwp

    n_scid = 0

    occupied_syms = pdschdmrs_occ_symbols(cfg.dmrs_typeA_pos, cfg.symbol_allocation[1], cfg.dmrs_additional_pos)

    # Start generation for every symbol
    dmrs_syms = np.array([])
    for n_symb in occupied_syms:
        cinit_dmrs = nr_pdschdmrs_cinit(carrier.symbols_per_slot, carrier.n_slot, n_symb, cfg.dmrs_NIDNSCID, n_scid)
        dmrs_prbs = nrPRBS(cinit_dmrs, dmrs_size)

        # Cut PRBS sequency
        dmrs_prbs = dmrs_prbs[dmrs_begin:dmrs_end]
        dmrs_syms = np.append(dmrs_syms, nrSymbolModulate(dmrs_prbs, "QPSK"))

    return dmrs_syms

# LUT for DMRS occupied symbols positions
def pdschdmrs_occ_symbols(typeA_pos, sym_alloc, add_pos):
    l1 = 11

    occupied_syms = np.array([], dtype=int)
    occupied_syms = np.append(occupied_syms, typeA_pos)

    if sym_alloc in [8, 9]:
        occupied_syms = np.append(occupied_syms, 7)
    elif sym_alloc in [10, 11]:
        if add_pos == 1:
            occupied_syms = np.append(occupied_syms, 9)
        elif add_pos == 2 or add_pos == 3:
            occupied_syms = np.append(occupied_syms, [6, 9])
    elif sym_alloc == 12:
        if add_pos == 1:
            occupied_syms = np.append(occupied_syms, 11)
        elif add_pos == 2:
            occupied_syms = np.append(occupied_syms, [7, 11])
        elif add_pos == 3:
            occupied_syms = np.append(occupied_syms, [5, 8, 11])
    elif sym_alloc in [13, 14]:
        if add_pos == 1:
            occupied_syms = np.append(occupied_syms, l1)
        elif add_pos == 2:
            occupied_syms = np.append(occupied_syms, [7, 11])
        elif add_pos == 3:
            occupied_syms = np.append(occupied_syms, [5, 8, 11])
    return occupied_syms

def nr_pdschdmrs_cinit(sps, n_slot, n_symb, NIDSCID, n_scid):
    return 2**17 * (sps * n_slot + n_symb + 1) * (2*NIDSCID + 1) + 2*NIDSCID + n_scid