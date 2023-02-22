
import numpy as np

def nr_mapper(databits, modtype):
    int_modtype = modtype.lower()

    assert int_modtype in ['bpsk', 'qpsk', 'qam16', 'qam64', 'qam256'], "modulation type is incorrect"
    assert len(databits) > 0, "length of databits must be greater 0"
    assert max(databits) < 2, "databits must be list of 0s and 1s"
    assert min(databits) >= 0, "databits must be list of 0s and 1s"

    if int_modtype == 'bpsk':
        res_arr = np.zeros(len(databits), dtype=(complex))
        for idx, sample in enumerate(databits):
            res_arr[idx] = (2*sample-1) + 1j*0

    elif int_modtype == 'qpsk':
        assert not (len(databits) % 2), "length of databits must be multiple of 2"
        databits = (2*databits-1) * (-1/np.sqrt(2))
        res_arr = np.zeros((len(databits)//2), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//2)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = sample[0] + 1j*sample[1]

    elif int_modtype == 'qam16':
        assert not (len(databits) % 4), "length of databits must be multiple of 4"
        databits = (2*databits-1) * (-1/np.sqrt(2))
        res_arr = np.zeros((len(databits)//4), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//4)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = (sample[0] + sample[3]//2) + 1j*(sample[2] + sample[4]//2)

    elif int_modtype == 'qam64':
        assert not (len(databits) % 6), "length of databits must be multiple of 6"
        databits = (2*databits-1) * (-1/np.sqrt(2))
        res_arr = np.zeros((len(databits)//6), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//6)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = (sample[0] + sample[3]//2 + sample[5]//4) + 1j*(sample[2] + sample[4]//2 + sample[6]//4);

    elif int_modtype == 'qam256':
        assert not (len(databits) % 8), "length of databits must be multiple of 8"
        pass

    return np.around(res_arr, 4)
