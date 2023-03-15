
# 38.211 5.2.1 Pseudo-random sequence generation

import numpy as np

def nr_prbs(cinit, n):

    assert n > 0

    # 9 = [1 0 0 1], 15 = [1 1 1 1] (both arranged msb->lsb)
    poly = [9, 15]

    # Register initialization
    reg = [1, cinit]

    # Pre-computed output masks for 1600 shift initialization
    masks = [35263098, 10031374]

    # Memory to store shift register value across the sequence
    seqpair = np.zeros((n, 2), dtype=(int))
    ts = np.zeros((n, 2), dtype=(int))

    feedback = [0, 0]

    # Parity table
    Parity15 = [x*(2**(31-1))
                for x in [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]]

    # Run the shift registers
    for i in range(n):
        # Store the masked register values
        seqpair[i][0] = reg[0] & masks[0]
        seqpair[i][1] = reg[1] & masks[1]
        # print(seqpair)

        # Top bit of 32 bit shift register
        and_regpoly = np.bitwise_and(reg, poly)
        # print(and_regpoly)

        feedback[0] = Parity15[int(and_regpoly[0])]
        feedback[1] = Parity15[int(and_regpoly[1])]

        # Shift registers down to the right
        reg[0] = reg[0] >> 1
        reg[1] = reg[1] >> 1

        # Then shift in top bit
        reg[0] = np.bitwise_xor(reg[0], feedback[0])
        reg[1] = np.bitwise_xor(reg[1], feedback[1])

    # Parity table for output masking
    Parity = np.array([
        0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
        1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
        1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
        0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
        1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
        0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
        0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
        1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0
    ])

    # Output masking to implement the shift
    pseq = np.zeros((n, 2), dtype=(int))
    # Shift down 16 and combine
    for i in range(n):
        ts[i][0] = np.bitwise_xor(seqpair[i][0], seqpair[i][0] >> 16)
        ts[i][1] = np.bitwise_xor(seqpair[i][1], seqpair[i][1] >> 16)

        # Shift down 8 and combine
        ts[i][0] = np.bitwise_xor(ts[i][0], ts[i][0] >> 8)
        ts[i][1] = np.bitwise_xor(ts[i][1], ts[i][1] >> 8)

        # Mask lower 8 bits
        ts[i][0] = np.bitwise_and(ts[i][0], 255)
        ts[i][1] = np.bitwise_and(ts[i][1], 255)

        # Look up parity value for these 8 bits
        pseq[i][0] = Parity[ts[i][0]]
        pseq[i][1] = Parity[ts[i][1]]

    # Combine (xor) together the two PN sequences
    return np.array([np.bitwise_xor(a, b) for (a, b) in pseq])
