import unittest
from decoder import *


class TestParser(unittest.TestCase):

    def test_find_weight(self):
        self.assertEqual(find_weight([1, 1]), 2)

    def test_decode_extended_Golay(self):
        self.assertEqual(decode_extended_Golay('101010101010010010111100'), '101010101010')
        # the following test cases are from p80-80, 'Coding Theory and Cryptography: The Essentials'
        # by Hoffman, Lindner, Wall ISBN: 0-8247-0465-7.
        self.assertEqual(decode_extended_Golay('101111101111010010010010'), '001111101110')
        self.assertEqual(decode_extended_Golay('001001001101101000101000'), '001001011111')
        self.assertEqual(decode_extended_Golay('000111000111011011010000'), '000011000111')
        # print(decode_extended_Golay('111000000000011011011011'))
        # print(decode_extended_Golay('111111000000100011100111'))
        # print(decode_extended_Golay('111111000000101011100111'))
        # print(decode_extended_Golay('111111000000111000111000'))
        # print(decode_extended_Golay('111000000000110111001101'))
        # print(decode_extended_Golay('110111001101111000000000'))
        self.assertEqual(decode_extended_Golay('000111000111101000101101'), '000111000111')
        # print(decode_extended_Golay('110000000000101100100000'))
        # print(decode_extended_Golay('110101011101111000000000'))

    def test_decode_Golay(self):
        self.assertEqual(decode_Golay('00100100100111111110000'), '001001000000')


if __name__ == '__main__':
    unittest.main()
