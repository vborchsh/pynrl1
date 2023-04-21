
# 38.211

import numpy as np

from pynrl1.downlink.nrPDSCHDMRS import pdschdmrs_occ_symbols
from pynrl1.util.nrPDSCHConfig import nrPDSCHConfig

def nrPDSCHDMRSIndices(cfg: nrPDSCHConfig):
    frame_begin = cfg.n_rb_size * min(cfg.PRB_set)
    frame_end = cfg.n_rb_size * (max(cfg.PRB_set)+1)
    frame_size = cfg.n_rb_size * cfg.n_size_bwp

    # Single frame DMRS positions
    dmrs_full_range = np.array(list(range(frame_begin, frame_end)))

    # Calculate DMRS positions in every occupied symbol. Frequency position
    if cfg.dmrs_conf_type == 1:
        # Takes every 2nd symbol
        occupied_res = dmrs_full_range[::2]
    elif cfg.dmrs_conf_type == 2:
        # Takes every 4th couple of symbols
        occupied_res = dmrs_full_range.reshape(-1, 2)[::3].ravel()

    # Calculates occupied symbols numbers. Time positions
    occupied_syms = pdschdmrs_occ_symbols(cfg.dmrs_typeA_pos, cfg.symbol_allocation[1], cfg.dmrs_additional_pos)

    dmrs_indices = np.array([])
    for idx, sym in enumerate(occupied_syms):
        sym_offset = sym*frame_size
        dmrs_indices = np.append(dmrs_indices, (occupied_res + sym_offset))

    return dmrs_indices
