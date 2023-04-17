
# 38.211

import numpy as np

# from pynrl1.util.nr_prbs import nr_prbs
# from pynrl1.util.nr_mapper import nr_mapper
from pynrl1.util.configurations import nrPDSCH_config

def nr_pdschdmrs_indices(cfg: nrPDSCH_config):
    frame_begin = cfg.n_rb_size * min(cfg.PRB_set)
    frame_end = cfg.n_rb_size * (max(cfg.PRB_set)+1)
    frame_size = cfg.n_rb_size * cfg.n_size_bwp
    # print(frame_begin, frame_end, frame_size)

    # Single frame DMRS positions
    dmrs_full_range = np.array(list(range(frame_begin, frame_end)))

    # Calculate DMRS positions in every occupied symbol. Frequency position
    if cfg.dmrs_conf_type == 1:
        # Takes every 2nd symbol
        occupied_res = dmrs_full_range[::2]
    elif cfg.dmrs_conf_type == 2:
        # Takes every 4th couple of symbols
        occupied_res = dmrs_full_range.reshape(-1, 2)[::3].ravel()
    # print(occupied_res)

    # Calculates occupied symbols numbers. Time positions
    l1 = 11

    occupied_syms = np.array([])
    occupied_syms = np.append(occupied_syms, cfg.dmrs_typeA_pos)

    # print(cfg.symbol_allocation[1], cfg.dmrs_additional_pos)

    # LUT for the reset symbols positions
    if cfg.symbol_allocation[1] in [8, 9]:
        occupied_syms = np.append(occupied_syms, 7)
    elif cfg.symbol_allocation[1] in [10, 11]:
        if cfg.dmrs_additional_pos == 1:
            occupied_syms = np.append(occupied_syms, 9)
        if cfg.dmrs_additional_pos == 2 or cfg.dmrs_additional_pos == 3:
            occupied_syms = np.append(occupied_syms, [6, 9])
    elif cfg.symbol_allocation[1] == 12:
        if cfg.dmrs_additional_pos == 1:
            occupied_syms = np.append(occupied_syms, 11)
        elif cfg.dmrs_additional_pos == 2:
            occupied_syms = np.append(occupied_syms, [7, 11])
        elif cfg.dmrs_additional_pos == 3:
            occupied_syms = np.append(occupied_syms, [5, 8, 11])
    elif cfg.symbol_allocation[1] in [13, 14]:
        if cfg.dmrs_additional_pos == 1:
            occupied_syms = np.append(occupied_syms, l1)
        elif cfg.dmrs_additional_pos == 2:
            occupied_syms = np.append(occupied_syms, [7, 11])
        elif cfg.dmrs_additional_pos == 3:
            occupied_syms = np.append(occupied_syms, [5, 8, 11])
    print(occupied_syms)

    dmrs_indices = np.array([])
    for idx, sym in enumerate(occupied_syms):
        sym_offset = sym*frame_size
        dmrs_indices = np.append(dmrs_indices, (occupied_res + sym_offset))
    # print(dmrs_indices)

    return dmrs_indices
