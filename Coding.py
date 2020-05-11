import numpy as np
from scipy.special import comb

from golay import decode, encode


def encodebits(msg):
    msgsize = len(msg)
    addnzeros = np.zeros((12 - msgsize % 12, 1))
    dappendarray = np.zeros((12, 1))
    dappendarray[msgsize % 12] = 1
    msg = np.append(np.append(msg, addnzeros), dappendarray)
    return encode(msg)


def decodebits(demodmsg):
    decodedmsg = decode(demodmsg)
    last12bits = decodedmsg[-12:]
    bitstoignore = 12 if (np.argmax(last12bits) ==
                          0) else np.argmax(last12bits)
    bitstoignore = 12 if (np.argmax(last12bits) == 0) else (12 - bitstoignore)
    bitstoignore += 12
    decodedmsg = decodedmsg[:-(bitstoignore)]
    return decodedmsg


def error_probabilities(msg, decoded_msg, Eb, N0, pc):
    # pc is the theoretical bit error probability without encoding - depends on the method used and hence needs to be passed to this function
    t = 3
    n = 24
    Pb = 0
    for i in range(t + 1, n + 1):
        Pb += i * comb(n, i, exact=True) * pc ** i * (1 - pc) ** (n - i)
    Pb /= n
    Pb_pr = 0
    count = 0
    for i in range(len(decoded_msg)):
        if int(msg[i]) != int(decoded_msg[i]):
            Pb_pr += 1
        count += 1
    Pb_pr = Pb_pr/count
    return Pb, Pb_pr


if __name__ == "__main__":
    msg = np.random.randint(
        low=0, high=2, size=np.random.randint(low=0, high=500, size=1)[0]
    )
    # msg = np.random.randint(
    #     low=0, high=2, size=192)
    encoded_data = encodebits(msg)
    decoded_data = decodebits(encoded_data)
    print(msg.shape)
    print(decoded_data.shape)
