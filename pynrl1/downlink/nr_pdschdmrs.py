
# 38.211

import numpy as np

from pynrl1.util.nr_prbs import nr_prbs
from pynrl1.util.nr_mapper import nr_mapper
from pynrl1.util.configurations import nrPDSCH_config
from pynrl1.util.configurations import nrCarrier_config

def nr_pdschdmrs(cfg: nrPDSCH_config, carrier: nrCarrier_config):
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
        dmrs_prbs = nr_prbs(cinit_dmrs, dmrs_size )

        # Cut PRBS sequency
        dmrs_prbs = dmrs_prbs[dmrs_begin:dmrs_end]
        dmrs_syms = np.append(dmrs_syms, nr_mapper(dmrs_prbs, "QPSK"))

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
        if add_pos == 2 or add_pos == 3:
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
    return (1 << 17) * (sps * n_slot + n_symb + 1) * ((NIDSCID << 1) + 1) + ((NIDSCID << 1) + n_scid)