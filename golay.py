from GolayEncoderDecoder.Encoder.encoder import *
from GolayEncoderDecoder.Decoder.decoder import *
import numpy as np

def encode(data):
    n = 12
    # If number of bits are not a multiple of 12, append trailing zeros
    if len(data)%12 != 0:
        # data = np.array([data, np.zeros(len(data) - len(data)%12, dtype=np.int)])
        data = np.append(data, np.zeros(n - len(data)%n, dtype=np.int))
    # Split data into chunks of 12
    split_data = data.reshape(len(data)//n, n)
    # split_data = [data[i:i+n] for i in range(0, len(data), n)]
    # split_data = np.array(split_data)
    encoded_data = []
    for i in range(len(split_data)):
        # Encode chunk and append
        encoded_data.extend(encode_extended_Golay(split_data[i].tolist()))
    return np.array(encoded_data)
    # print(type(encoded_data))
    # print(encoded_data)

def decode(data):
    n = 24
    # Split data into chunks of 24
    split_data = data.reshape(len(data)//n, n)
    decoded_data = []
    for i in range(len(split_data)):
        # Decode and append
        decoded_data.extend(decode_extended_Golay(split_data[i].tolist()))
    return np.array(decoded_data)

if __name__ == '__main__':
    encoded_data = encode(np.array([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]))
    print(encoded_data)
    decoded_data = decode(encoded_data)
    print(decoded_data)