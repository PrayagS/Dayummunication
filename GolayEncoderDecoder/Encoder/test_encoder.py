import unittest
from Encoder.encoder import *


class TestParser(unittest.TestCase):

    def test_encode_extended_Golay(self):
        self.assertEqual(encode_extended_Golay('101010101010'), '101010101010010010111100')

    def test_encode_Golay(self):
        self.assertEqual(encode_Golay('010101010101'), '01010101010110110100001')


if __name__ == '__main__':
    unittest.main()
