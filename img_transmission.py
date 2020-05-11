import numpy as np
from PIL import Image
import channel
import Coding
import QFSK

if __name__ == "__main__":
    img = Image.open("lena256color.tiff")
    img_matrix = np.array(img)
    img_array = np.reshape(img_matrix, np.prod(img_matrix.shape))
    binary_img_array = np.unpackbits(img_array)
    binary_img_array = Coding.encodebits(binary_img_array)
    # M = 8
    # k = int(np.log2(M))
    # gray_code, constellation_table, modulated_signal_with_noise, N0 = modulate(
    #     encoded_msg, k, M)
    # demodulated_msg = demodulate(
    #     encoded_msg, k, M, gray_code, constellation_table, modulated_signal_with_noise, N0)
    # decoded_msg = decode(np.array(demodulated_msg))
    # Pe, Pb, Pb_pr = error_probabilities(
    # binary_img_array, decoded_msg, N0, k, M)
    # 0.08960278828938802

    modulated_array = QFSK.modulate(binary_img_array, 0.001, 0.01, 100, 10000)
    noise = channel.generate_noise(modulated_array, 0.0004, 10000)
    signal_plus_noise = modulated_array + noise
    demodulated_array = QFSK.demodulate(signal_plus_noise ,0.01, 100, 10000)
    demodulated_array = Coding.decodebits(demodulated_array)
    demodulated_img_array = np.reshape(
        np.packbits(np.array(demodulated_array)), img_matrix.shape)
    decoded_img = Image.fromarray(demodulated_img_array)
    decoded_img.save("encoded_lena256color_decoded_QFSK.tiff", format="TIFF")
    Pe, Pb, Pb_pr = QFSK.error_probabilities(
        binary_img_array, demodulated_array, 0.001, 0.0004)
    print(Pb, Pb_pr)
