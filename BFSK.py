from math import ceil

import numpy as np


def modulate(msg, Eb, Tb, f_c1, f_s):
    f_c2 = ceil(f_c1 + 1 / Tb)
    signal = []
    t = np.linspace(0, Tb, int(Tb * f_s))
    for i in msg:
        s = np.sqrt(2 * Eb / Tb) * np.cos(2 * np.pi * f_c1 * t)
        s1 = np.sqrt(2 * Eb / Tb) * np.cos(2 * np.pi * f_c2 * t)
        if i == 0:
            s = s1
        signal.extend(s)
    t = np.linspace(0, len(msg) * Tb, int(len(msg) * Tb * f_s))
    return np.array(signal)


def demodulate(signal, Tb, f_c1, f_s):
    f_c2 = ceil(f_c1 + 1 / Tb)
    t = np.linspace(0, Tb, int(Tb * f_s))
    Ts = int(Tb * f_s)  # no of samples of carrier for 1 bit
    e1 = np.cos(2 * np.pi * f_c1 * t)  # cosomega1t
    e2 = np.sin(2 * np.pi * f_c1 * t)  # sinomega1t
    e3 = np.cos(2 * np.pi * f_c2 * t)  # cosomega2t
    e4 = np.sin(2 * np.pi * f_c2 * t)  # sinomega2t
    received_msg = []
    for x in range(int(len(signal) / Ts)):
        samplearr = signal[x * Ts: (x + 1) * Ts]
        e5 = (samplearr * e1).sum() / len(samplearr)
        e6 = (samplearr * e2).sum() / len(samplearr)
        e7 = (samplearr * e3).sum() / len(samplearr)
        e8 = (samplearr * e4).sum() / len(samplearr)

        e9 = e5 + e6
        e10 = e7 + e8
        if e9 < e10:
            received_msg.append(0)
        else:
            received_msg.append(1)
    return received_msg


def error_probabilities(msg, decoded_msg, Eb, N0):
    Pb = (1 / 2) * np.exp(-Eb / N0)
    Pb_pr = np.count_nonzero(msg != decoded_msg) / len(msg)
    return Pb, Pb_pr
