import matlab.engine
import os
import itertools
import numpy as np
import pytest

from pynrl1.downlink.nrPDSCHDMRS import nrPDSCHDMRS
from pynrl1.downlink.nrPDSCHDMRSIndices import nrPDSCHDMRSIndices
from pynrl1.util.nrPDSCHConfig import nrPDSCHConfig
from pynrl1.util.nrCarrierConfig import nrCarrierConfig

def run_nr_pdschdmrs(cfg, eng):
    carrier = nrCarrierConfig();
    carrier.subcarrier_spacing = 120;
    carrier.cyclic_prefix = 'normal';
    carrier.n_size_grid = 132;
    carrier.n_start_grid = 0;

    pdsch_cfg = nrPDSCHConfig();
    pdsch_cfg.n_size_bwp = cfg['n_size_bwp']
    pdsch_cfg.n_start_bwp = cfg['n_start_bwp']
    pdsch_cfg.mapping_type = cfg['MappingType']
    pdsch_cfg.dmrs_typeA_pos = cfg['DMRSTypeAPosition']
    pdsch_cfg.dmrs_len = cfg['DMRSLength']
    pdsch_cfg.dmrs_additional_pos = cfg['DMRSAdditionalPosition']
    pdsch_cfg.dmrs_conf_type = cfg['DMRSConfigurationType']
    pdsch_cfg.dmrs_NIDNSCID = cfg['NIDNSCID']
    pdsch_cfg.dmrs_NSCID = cfg['NSCID']
    pdsch_cfg.PRB_set = cfg['PRBSet']
    pdsch_cfg.symbol_allocation = cfg['SymbolAllocation']

    pdschdmrs_syms = nrPDSCHDMRS(pdsch_cfg, carrier)
    pdschdmrs_indices = nrPDSCHDMRSIndices(pdsch_cfg)

    [pdschdmrs_syms_ref, pdschdmrs_indices_ref] = eng.gen_pdschdmrs(cfg, nargout=2)
    pdschdmrs_syms_ref = np.array(list(itertools.chain(*pdschdmrs_syms_ref)))

    pdschdmrs_indices_ref = np.array(list(itertools.chain(*pdschdmrs_indices_ref)))
    pdschdmrs_indices_ref = pdschdmrs_indices_ref - 1

    pdschdmrs_syms = np.around(pdschdmrs_syms, 4)
    pdschdmrs_syms_ref = np.around(pdschdmrs_syms_ref, 4)

    assert np.array_equal(pdschdmrs_syms, pdschdmrs_syms_ref)
    assert np.array_equal(pdschdmrs_indices, pdschdmrs_indices_ref)


@pytest.mark.parametrize('typeA_pos', [2, 3])
@pytest.mark.parametrize('symb_alloc', [[2, 12]])
@pytest.mark.parametrize('dmrs_add_pos', [0, 1, 2, 3])
@pytest.mark.parametrize('PRBSet', [list(range(0, 132)), list(range(60, 132)), list(range(30, 60))])
@pytest.mark.parametrize('dmrs_cfg_type', [1, 2])
def test_nr_pdschdmrs(symb_alloc, dmrs_add_pos, typeA_pos, PRBSet, dmrs_cfg_type):
    eng = matlab.engine.connect_matlab()
    eng.cd(os.path.dirname(__file__))

    cfg = {}
    cfg['n_size_bwp'] = 132
    cfg['n_start_bwp'] = 0
    cfg['MappingType'] = "A"
    cfg['DMRSTypeAPosition'] = typeA_pos
    cfg['DMRSLength'] = 1
    cfg['DMRSAdditionalPosition'] = dmrs_add_pos
    cfg['PRBSet'] = PRBSet
    cfg['SymbolAllocation'] = symb_alloc
    cfg['DMRSConfigurationType'] = dmrs_cfg_type
    cfg['NIDNSCID'] = 1
    cfg['NSCID'] = 0

    try:
        run_nr_pdschdmrs(cfg, eng)
    finally:
        eng.quit()

if __name__ == '__main__':
    test_nr_pdschdmrs([2, 12], 1, 2, list(range(2, 130)), 2)
