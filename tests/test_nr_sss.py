import matlab.engine
import itertools
import numpy as np
import pytest

from pynrl1.downlink.nr_sss import nr_sss

def run_nr_sss(ncellid, eng):
    ref_data = eng.nrSSS(matlab.double(ncellid))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    ref_ind = eng.nrSSSIndices()
    ref_ind = np.array(list(itertools.chain(*ref_ind)))
    ref_ind = np.array(ref_ind - 1)

    [indices, data] = nr_sss(ncellid)
    data = [(x*2)-1 for x in data]

    assert (ref_data == data).all()
    assert (indices == ref_ind).all()

@pytest.mark.parametrize("ncellid", [0, 600, 1007])
def test_nr_sss(ncellid):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_sss(ncellid, eng)
    finally:
        eng.quit()

