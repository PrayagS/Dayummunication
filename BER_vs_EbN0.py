import numpy as np
from numpy import sqrt
from numpy.random import rand, randn
import matplotlib.pyplot as plt
import channel
import Coding
import BPSK, QPSK, BFSK, QFSK, MPSK

if __name__ == "__main__":
    N = 1e3
    EbNodB_range = range(0,50)
    ber = []

    for n in range(len(EbNodB_range)): 
    
        EbNodB = EbNodB_range[n]   
        EbNo=10.0**(EbNodB/10.0)
        noise_std = 1/sqrt(2*EbNo)
        msg = np.random.randint(low=0, high=2, size=int(N))
        msg = Coding.encodebits(msg)

        mmsg = BPSK.modulate(msg, EbNo*0.0004, 0.01, 100, 10000)
        mmsg += channel.generate_noise(mmsg, noise_std, 10000)

        dmsg = BPSK.demodulate(mmsg, 0.01, 100, 10000)
        dsmg = Coding.decodebits(dmsg)

        Pb, Pb_pr = BPSK.error_probabilities(msg, dmsg, EbNo*0.0004, noise_std)
        ber.append(Pb_pr)
    
    plt.plot(EbNodB_range, ber, "o-", label="BPSK Practical BER")
    plt.xscale('linear')
    plt.xlabel("SNR (dB)")
    plt.ylabel("BER")
    plt.yscale('log')
    plt.legend()
    plt.savefig("BPSK_PER.png")
    plt.show()