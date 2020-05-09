import numpy as np
from math import ceil

def modulate(msg, Eb, Tb, f_c1, f_s):
    f_c2 = ceil(f_c1 + 1/Tb)
    signal = []
    t = np.linspace(0, Tb, int(Tb*f_s))
    for i in msg:
        s = np.sqrt(2*Eb/Tb)*np.cos(2*np.pi*f_c1*t)
        s1=np.sqrt(2*Eb/Tb)*np.cos(2*np.pi*f_c2*t)
        if i == 0:
            s = s1
        signal.extend(s)
    t = np.linspace(0, len(msg)*Tb, int(len(msg)*Tb*f_s))
    return np.array(signal)

def demodulate(signal, Tb, f_c1, f_s):
    t = np.linspace(0, Tb, Tb*f_s)
    phi = np.sqrt(2/Tb)*np.sin(2*np.pi*f_c1*t)
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