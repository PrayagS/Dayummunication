import numpy as np
from PIL import Image
from MPSK import modulate, demodulate, error_probabilities
from QPSK import modulate as QPSK_modulate
# from golay import encode, decode

if __name__ == "__main__":
    img = Image.open("img_resized.jpg")
    img_matrix = np.array(img)
    img_array = np.reshape(img_matrix, np.prod(img_matrix.shape))
    binary_img_array = np.unpackbits(img_array)

    # M = 8
    # k = int(np.log2(M))
    # gray_code, constellation_table, modulated_signal_with_noise, N0 = modulate(
    #     encoded_msg, k, M)
    # demodulated_msg = demodulate(
    #     encoded_msg, k, M, gray_code, constellation_table, modulated_signal_with_noise, N0)
    # decoded_msg = decode(np.array(demodulated_msg))
    # Pe, Pb, Pb_pr = error_probabilities(
    # binary_img_array, decoded_msg, N0, k, M)

    demodulated_msg, N0 = QPSK_modulate(binary_img_array)
    demodulated_img = np.reshape(
        np.packbits(np.array(demodulated_msg)), img_matrix.shape)
    decoded_img = Image.fromarray(demodulated_img)
    decoded_img.save("decoded_img.jpg", format="JPEG")
    Pe, Pb, Pb_pr = error_probabilities(
        binary_img_array, demodulated_msg, N0, 2, 4)
