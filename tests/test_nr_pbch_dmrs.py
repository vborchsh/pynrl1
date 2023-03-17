import matlab.engine
import itertools
import numpy as np
import pytest

from pynrl1.downlink.nr_pbch_dmrs import nr_pbch_dmrs

def run_nr_pbch_dmrs(ncellid, issb, eng):
    ref_data = eng.nrPBCHDMRS(matlab.double(ncellid), matlab.double(issb))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    ref_ind = eng.nrPBCHDMRSIndices(matlab.double(ncellid))
    ref_ind = np.array(list(itertools.chain(*ref_ind)))
    ref_ind = np.array(ref_ind - 1)

    [indices, data] = nr_pbch_dmrs(ncellid, issb)

    ref_data = np.around(ref_data, 4)
    data = np.around(data, 4)

    assert (ref_data == data).all()
    assert (ref_ind == indices).all()

@pytest.mark.parametrize("ncellid", [0, 500, 1007])
@pytest.mark.parametrize("issb", list(range(8)))
def test_nr_pbch_dmrs(ncellid, issb):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_pbch_dmrs(ncellid, issb, eng)
    finally:
        eng.quit()
