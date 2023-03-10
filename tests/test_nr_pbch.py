import matlab.engine
import itertools
import numpy as np
import pytest

from pynrl1.src.nr_pbch import nr_pbch

def run_nr_pbch(ncellid, databits, v, eng):
    ref_data = eng.nrPBCH(databits, matlab.double(ncellid), matlab.double(v), nargout=1)
    ref_data = np.array(list(itertools.chain(*ref_data)))

    data = nr_pbch(ncellid, v, np.array(list(itertools.chain(*databits)), dtype=(int)))

    ref_data = np.around(ref_data, 4)
    data = np.around(data, 4)

    assert (ref_data == data).all()

@pytest.mark.parametrize("ncellid", [1, 500, 1007])
@pytest.mark.parametrize("v", list(range(8)))
def test_nr_pbch(ncellid, v):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_pbch(ncellid, eng.randi(matlab.double([0, 1]),864,1), v, eng)
    finally:
        eng.quit()
