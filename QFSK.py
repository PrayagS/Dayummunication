import numpy as np
from math import ceil


def modulate(msg, Eb, Tb, f_c1, f_s):
    f_c2 = ceil(f_c1 + 1 / Tb)
    f_c3 = ceil(f_c1 + 2 / Tb)
    f_c4 = ceil(f_c1 + 3 / Tb)
    symbols = np.array([msg[0::2], msg[1::2]])
    signal = []
    t = np.linspace(0.0, Tb, int(Tb * f_s))
    for k in range(np.size(symbols, axis=1)):
        b_0 = symbols[0, k]
        b_1 = symbols[1, k]
        if b_0 == 0 and b_1 == 0:
            s = np.sqrt(2 * Eb / Tb) * np.cos(2 * np.pi * f_c1 * t)
        elif b_0 == 1 and b_1 == 0:
            s = np.sqrt(2 * Eb / Tb) * np.cos(2 * np.pi * f_c2 * t)
        elif b_0 == 0 and b_1 == 1:
            s = np.sqrt(2 * Eb / Tb) * np.cos(2 * np.pi * f_c3 * t)
        elif b_0 == 1 and b_1 == 0:
            s = np.sqrt(2 * Eb / Tb) * np.cos(2 * np.pi * f_c4 * t)

        signal.extend(s)
        return np.array(signal)


def demodulate(signal, Tb, f_c1, f_s):
    t = np.linspace(0.0, Tb, int(Tb * f_s))
    f_c2 = ceil(f_c1 + 1 / Tb)
    f_c3 = ceil(f_c1 + 2 / Tb)
    f_c4 = ceil(f_c1 + 3 / Tb)
    Ts = int(Tb * f_s)  # no of samples of carrier for 1 bit
    e1 = np.cos(2 * np.pi * f_c1 * t)  # cosomega1t
    e2 = np.sin(2 * np.pi * f_c1 * t)  # sinomega1t
    e3 = np.cos(2 * np.pi * f_c2 * t)  # cosomega2t
    e4 = np.sin(2 * np.pi * f_c2 * t)  # sinomega2t
    e5 = np.cos(2 * np.pi * f_c3 * t)  # cosomega1t
    e6 = np.sin(2 * np.pi * f_c3 * t)  # sinomega1t
    e7 = np.cos(2 * np.pi * f_c4 * t)  # cosomega2t
    e8 = np.sin(2 * np.pi * f_c4 * t)  # sinomega2t

    decmsg = []
    for x in range(int(len(signal) / Ts)):
        samplearr = signal[x * Ts:(x + 1) * Ts]
        e9 = (samplearr * e1).sum() / len(samplearr)
        e10 = (samplearr * e2).sum() / len(samplearr)
        e11 = (samplearr * e3).sum() / len(samplearr)
        e12 = (samplearr * e4).sum() / len(samplearr)
        e13 = (samplearr * e5).sum() / len(samplearr)
        e14 = (samplearr * e6).sum() / len(samplearr)
        e15 = (samplearr * e7).sum() / len(samplearr)
        e16 = (samplearr * e8).sum() / len(samplearr)

        e17 = e9 + e10
        e18 = e11 + e12
        e19 = e13 + e14
        e20 = e15 + e16

        if e17 > e18 and e17 > e19 and e17 > e20:
            decmsg.append(0)
            decmsg.append(0)
        elif e18 > e17 and e18 > e19 and e18 > e20:
            decmsg.append(1)
            decmsg.append(0)
        elif e19 > e18 and e19 > e17 and e19 > e20:
            decmsg.append(0)
            decmsg.append(1)
        elif e20 > e17 and e20 > e18 and e20 > e19:
            decmsg.append(1)
            decmsg.append(1)


def error_probabilities(msg, decoded_msg, Eb, N0):
    Pe = (3 / 2) * np.exp(-Eb / (2 * N0))
    Pb = 2 * Pe / 3
    Pb_pr = np.count_nonzero(msg != decoded_msg) / len(msg)
    return Pe, Pb, Pb_pr
