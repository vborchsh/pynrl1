import matlab.engine
import numpy as np
import pytest

from pynrl1.util.nr_mapper import nr_mapper

def map_bits(databits, modtype):
    pass

def run_nr_mapper(modtype, databits):
    ref_data = map_bits(databits, modtype)
    data = nr_mapper(databits, modtype)

    assert (ref_data == data).all()

@pytest.mark.parametrize("modtype", ['bpsk', 'qpsk', 'qam16', 'qam64', 'qam256'])
def test_nr_pbch(modtype):

    try:
        run_nr_mapper(modtype)
    finally:
        eng.quit()
