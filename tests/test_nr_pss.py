import matlab.engine
import itertools
import numpy as np
import pytest

from pynrl1.src.nr_pss import nr_pss

def run_nr_pss(ncellid, eng):
    ref_data = eng.nrPSS(matlab.double(ncellid))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    ref_ind = eng.nrPSSIndices()
    ref_ind = np.array(list(itertools.chain(*ref_ind)))
    ref_ind = np.array(ref_ind - 1)

    [indices, data] = nr_pss(ncellid)
    data = [(x*2)-1 for x in data]

    assert (ref_data == data).all()
    assert (indices == ref_ind).all()

@pytest.mark.parametrize("ncellid", [1, 500, 1007])
def test_nr_pss(ncellid):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_pss(ncellid, eng)
    finally:
        eng.quit()