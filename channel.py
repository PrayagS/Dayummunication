import numpy as np


def generate_noise(signal, N0, f_s):
    N0_unit_power = 0.0004
    ns = len(signal)
    noise = np.random.normal(size=ns)
    noise *= np.sqrt(N0/N0_unit_power)
    # f, psd = periodogram(noise, f_s)
    # psd_av = np.mean(psd)
    # N0 = 2*psd_av
    return noise
    # signal_with_noise = signal + noise
    # return signal_with_noise
