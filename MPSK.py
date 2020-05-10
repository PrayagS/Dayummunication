#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import periodogram
from scipy.spatial import distance
from scipy.stats import norm
from sympy.combinatorics.graycode import GrayCode

# Carrier signal
f_c = 100.0
t_c = 1.0 / f_c

# Sampling rate
f_s = 10000.0
t_s = 1.0 / f_s

# MPSK Parameters
Tb = 0.01
Eb = 0.001


def bits_to_symbols(msg, k):
    bucket_of_buckets = []
    for i in range(k):
        bucket_of_buckets.append(msg[i::k])
    symbols = np.array(bucket_of_buckets)
    return symbols


def constellation_angles(M):
    return np.arange(0.0, 2.0 * np.pi, 2.0 * np.pi / M)


def graycode(k):
    return list(GrayCode(k).generate_gray())


def generate_constellation_table(constellation, gray_code):
    constellation_table = {}
    for i, code in enumerate(gray_code):
        constellation_table[code] = constellation[i]
    return constellation_table


def generate_theta_vector(symbols, constellation_table):
    theta = np.zeros(np.size(symbols, axis=1), dtype="float")
    for j in range(np.size(symbols, axis=1)):
        bits = []
        for i in range(np.size(symbols, axis=0)):
            bits.append(symbols[i, j])
        bits_str = ""
        for bit in bits:
            bits_str += str(bit)
        theta[j] = constellation_table[bits_str]
    return theta


def generate_I_Q_signals(theta):
    A = np.sqrt(Eb)
    I = A * np.cos(theta)  # in-phase component
    Q = A * np.sin(theta)  # quadrature component
    return I, Q


def plot_constellation_diagram(I, Q):
    plt.figure()
    # Makes it look like a circle instead of an ellipse
    plt.axes().set_aspect("equal", "datalim")

    # Time vector for sine and cosine
    t_csd = np.linspace(0.0, 2.0 * np.math.pi, 100)
    plt.plot(
        np.sqrt(Eb) * np.sin(t_csd), np.sqrt(Eb) * np.cos(t_csd)
    )  # sqrt(Eb)*sin and sqrt(Eb)*cos
    plt.plot(I, Q, "ro", markersize=12)
    plt.grid()

    plt.title("Constellation diagram for QPSK", fontsize=14)
    plt.tick_params(labelsize=12)
    plt.show()


def modulate_signal(symbols, I, Q):
    t = np.linspace(0.0, Tb, int(Tb * f_s))
    modulated_signal = np.empty(
        np.size(symbols, axis=1) * len(t), dtype="float")
    phi_1 = np.sqrt(2 / Tb) * np.cos(2.0 * np.math.pi * f_c * t)
    phi_2 = np.sqrt(2 / Tb) * np.sin(2.0 * np.math.pi * f_c * t)
    for k in range(np.size(symbols, axis=1)):
        # Calculates modulated signal for each symbol
        # Page 12, Lecture 16
        modulated_signal[k * len(t): (k + 1) * len(t)
                         ] = I[k] * phi_1 - Q[k] * phi_2
    return modulated_signal


def plot_modulated_signal(symbols, modulated_signal):
    # Time vector for symbols
    # t_sym = np.arange(0.0, np.size(symbols, axis=1)*2.0*t_c, t_s)
    t_sym = np.linspace(
        0, np.size(symbols, axis=1) *
        Tb, int(np.size(symbols, axis=1) * Tb * f_s)
    )

    plt.figure()

    plt.title("MPSK", fontsize=14)
    plt.xlabel("t", fontsize=14)
    plt.ylabel("Amplitude", fontsize=14)
    plt.tick_params(labelsize=12)

    plt.plot(t_sym, modulated_signal)
    plt.show()


def add_noise(modulated_signal):
    # Noise
    ns = len(modulated_signal)
    noise = np.random.normal(size=ns)

    f, psd = periodogram(noise, f_s)

    # Plot noise
    # fig, ax = plt.subplots(2,1)
    # ax[0].plot(noise)
    # ax[1].plot(f, psd)

    psd_av = np.mean(psd)
    N0 = 2 * psd_av
    # modulated_signal += noise
    return N0, modulated_signal


def generate_decoding_table(gray_code, constellation_table):
    decoding_table = {}
    for code in gray_code:
        amp = np.zeros(2, dtype="float")
        amp[0] = np.cos(constellation_table[code])
        amp[1] = np.sin(constellation_table[code])
        decoding_table[code] = amp
    return decoding_table


def demodulate_signal(modulated_signal, decoding_table, gray_code, k):
    t = np.linspace(0, Tb, int(Tb * f_s))
    phi_1 = np.sqrt(2 / Tb) * np.cos(2.0 * np.math.pi * f_c * t)
    phi_2 = np.sqrt(2 / Tb) * np.sin(2.0 * np.math.pi * f_c * t)
    N = len(modulated_signal) // len(t)
    split_modulated_signal = np.array_split(modulated_signal, N)

    decoded_symbols = [[] for i in range(k)]
    constellation_points = []
    for code in decoding_table:
        constellation_points.append(decoding_table[code])
    constellation_points = np.array(constellation_points)

    for i in split_modulated_signal:
        s_1 = i * phi_1
        s_2 = i * phi_2
        x = s_1.sum() / f_s
        y = s_2.sum() / f_s
        decoded_point = np.array([[x, y]])
        distances = distance.cdist(
            decoded_point, constellation_points, "euclidean")
        code = gray_code[np.argmin(distances[0])]
        for i, bit in enumerate(list(code)):
            decoded_symbols[i].append(int(bit))

    decoded_msg = []
    for i in range(len(decoded_symbols[0])):
        for j in range(len(decoded_symbols)):
            decoded_msg.append(decoded_symbols[j][i])

    return decoded_msg


def error_probabilities(msg, decoded_msg, N0, k, M):
    # Bit Error Probability Calculations
    # Pb = norm.sf(np.sqrt(2 * Eb / N0)) This is for BPSK/QPSK

    # Symbol Error Probability Calculations
    Pe = 2 * norm.sf(np.sqrt(2 * k * Eb / N0) * np.sin(np.math.pi / M))
    print("Theoretical Symbol Error Probability:", Pe)
    Pb = Pe / k
    print("Theoretical Bit Error Probability:", Pb)
    Pb_pr = np.count_nonzero(msg != decoded_msg) / len(msg)
    print("Practical Bit Error Probability:", Pb_pr)
    return Pe, Pb, Pb_pr


def modulate(msg, k, M):
    symbols = bits_to_symbols(msg, k)
    constellation = constellation_angles(M)
    gray_code = graycode(k)
    constellation_table = generate_constellation_table(
        constellation, gray_code)

    theta = generate_theta_vector(symbols, constellation_table)
    I, Q = generate_I_Q_signals(theta)

    return I, Q

    plot_constellation_diagram(I, Q)
    modulated_signal = modulate_signal(symbols, I, Q)
    # plot_modulated_signal(symbols, modulated_signal, Tb, f_s)
    N0, modulated_signal_with_noise = add_noise(modulated_signal)
    return gray_code, constellation_table, modulated_signal_with_noise, N0


def demodulate(msg, k, M, gray_code, constellation_table, modulated_signal, N0):
    decoding_table = generate_decoding_table(gray_code, constellation_table)
    decoded_msg = demodulate_signal(
        modulated_signal, decoding_table, gray_code, k)
    return decoded_msg


if __name__ == "__main__":
    # message to be transmitted
    msg = np.array(
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0]
    )  # 8PSK demo signal
    # msg = np.array([0, 1, 0, 0, 1, 1, 0, 1, 1, 0])  # QPSK demo signal
    # msg = np.random.randint(low=0, high=2, size=int(1e3))
    M = 8
    k = int(np.log2(M))
    gray_code, constellation_table, modulated_signal_with_noise, N0 = modulate(
        msg, k, M
    )
    decoded_msg = demodulate(
        msg, k, M, gray_code, constellation_table, modulated_signal_with_noise, N0
    )
    Pe, Pb, Pb_pr = error_probabilities(msg, decoded_msg, N0, k, M)
