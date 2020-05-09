#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
# from scipy.signal import periodogram
from scipy.stats import norm

# Carrier signal
f_c = 100.0
t_c = 1.0 / f_c

# Sampling rate
f_s = 10000.0
t_s = 1.0 / f_s

# BPSK Parameters
Tb = 0.01
Eb = 0.001

def modulate(msg):
    modulated_signal = []
    t = np.linspace(0, Tb, Tb*f_s)
    for i in msg:
        s = np.sqrt(2*Eb/Tb)*np.sin(2*np.pi*f_c*t)
        if i == 0:
            s = -s
        modulated_signal.extend(s)
    t = np.linspace(0, len(msg)*Tb, len(msg)*Tb*f_s)
    modulated_signal = np.array(modulated_signal)
    return modulated_signal    

# def add_noise(signal, N0):
#     N0_unit_power = 0.0004
#     ns = len(signal)
#     noise = np.random.normal(size=ns)
#     noise *= np.sqrt(N0/N0_unit_power)
#     f, psd = periodogram(noise, f_s)
#     psd_av = np.mean(psd)
#     # N0 = 2*psd_av
#     signal_with_noise = signal + noise
#     return signal_with_noise

def demodulate(signal):
    t = np.linspace(0, Tb, Tb*f_s)
    phi = np.sqrt(2/Tb)*np.sin(2*np.pi*f_c*t)
    N = len(signal) // len(t)
    signal = np.array_split(signal, N)
    received_msg = []
    for i in signal:
        x = i*phi
        sm = x.sum()/f_s
        if sm > 0:
            received_msg.append(1)
        else:
            received_msg.append(0)
    return received_msg

def error_probabilities(msg, decoded_msg, N0):
    Pb = norm.sf(np.sqrt(2*Eb/N0))
    # print('Theoretical Bit Error Probability:', Pb)
    Pb_pr = np.count_nonzero(msg != decoded_msg) / len(msg)
    # print('Practical Bit Error Probability:', Pb_pr)
    return Pb, Pb_pr