from golay import encode, decode
import numpy as np


def encodebits(msg):
    msgsize = len(msg)
    addnzeros = np.zeros((12-msgsize % 12, 1))
    dappendarray = np.zeros((12, 1))
    dappendarray[msgsize % 12] = 1
    msg = np.append(np.append(msg, addnzeros), dappendarray)
    return encode(msg)


def decodebits(demodmsg):
    decodedmsg = decode(demodmsg)
    last12bits = decodedmsg[-12:]
    bitstoignore = 12 if (np.argmax(last12bits) ==
                          0) else np.argmax(last12bits)
    bitstoignore = 12 if (np.argmax(last12bits) ==
                          0) else (12-bitstoignore)
    bitstoignore += 12
    decodedmsg = decodedmsg[:-(bitstoignore)]
    return decodedmsg


def error_probabilities(msg, decoded_msg, Eb, N0):
    Pb_pr = np.count_nonzero(msg != decoded_msg) / len(msg)
    return Pb_pr


if __name__ == "__main__":
    msg = np.random.randint(
        low=0, high=2, size=np.random.randint(
            low=0, high=500, size=1)[0])
    encoded_data = encodebits(msg)
    decoded_data = decodebits(encoded_data)
    print(msg.shape)
    print(decoded_data.shape)
