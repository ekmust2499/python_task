import unittest
import os
from encode import *
from decode import *

path = os.path.join(os.path.dirname(__file__), 'For_tests', 'picture.bmp')


class TestLinksExtractor(unittest.TestCase):

    def test_bmp_header(self):
        with open(path, "rb") as bmp_f:
            bmp = bytearray(bmp_f.read())
            bf_type, bf_off_bit = bmp_header(bmp)
            self.assertEqual(("BM", 138), (bf_type, bf_off_bit))

    def test_main_enc(self):
        value = 127
        for i in range(2, 9):
            encoded, num = main_encoding(value, 0, i, 8 - 1)
            self.assertEqual(encoded, 2 ** (i - 1) - 1)

    def test_enc_multi_sym(self):
        with open(path, "rb") as bmp_f:
            bmp = bytearray(bmp_f.read())
            x = encoding_multiple_characters(b'code', bmp, 1, 8)
            self.assertEqual(x, None)

    def test_write_in_file(self):
        path = os.path.join(os.path.dirname(__file__),
                            'For_tests', 'hello.txt')
        text = bytes("Привет".encode("utf-8"))
        write_in_file(path, text)
        with open(path, 'rb') as f:
            f = f.read()
            self.assertEqual(f, text)

    def test_encode(self):
        bmp = str(encoding(path, b'I love python', 4))
        with open(os.path.join(os.path.dirname(__file__),
                  'For_tests', 'primer.txt'), 'r') as f:
            f = f.read()
            self.assertEqual(bmp, f)

    def test_error_one(self):
        with open(os.path.join(os.path.dirname(__file__),
                  'For_tests', 'text.txt'), "rb") as file_f:
            file = bytearray(file_f.read())
            result = encoding(path, file, 2)
            self.assertEqual(result, False)

    def test_error_two(self):
        path = os.path.join(os.path.dirname(__file__), 'For_tests', 'doc.tiff')
        tiff = encoding(path, b'Hello', 5)
        self.assertEqual(tiff, False)

    def test_main_dec(self):
        value = 127
        res_data = {1: bytearray(b'\x00\x01\x01\x01\x01\x01\x01\x01'),
                    2: bytearray(b'\x01\x03\x03\x03\x00\x00\x00\x00'),
                    3: bytearray(b'\x03\x07\x06\x00\x00\x00\x00\x00'),
                    4: bytearray(b'\x07\x0f\x00\x00\x00\x00\x00\x00'),
                    5: bytearray(b'\x0f\x1c\x00\x00\x00\x00\x00\x00'),
                    6: bytearray(b'\x1f\x30\x00\x00\x00\x00\x00\x00'),
                    7: bytearray(b'\x3f\x40\x00\x00\x00\x00\x00\x00'),
                    8: bytearray(b'\x7f\x00\x00\x00\x00\x00\x00\x00')}

        for i in range(1, 9):
            self.assertEqual(main_decoding(res_data[i], i), value)

    def test_dec_mul_sym(self):
        text = "\xfd\xfe\xfe\xff\xff\xff".encode()
        x = decoding_multiple_characters(text, 4, 6).decode()
        self.assertEqual(x, "=>>???")

    def test_error_three(self):
        path = os.path.join(os.path.dirname(__file__), 'For_tests', 'doc.tiff')
        tiff = decoding(path)
        self.assertEqual(tiff, False)

    def test_error_four(self):
        path = os.path.join(os.path.dirname(__file__), 'For_tests', '1.bmp')
        tiff = decoding(path)
        self.assertEqual(tiff, False)

    def test_error_five(self):
        path = os.path.join(os.path.dirname(__file__),
                            'For_tests', 'primer.bmp')
        tiff = decoding(path)
        self.assertEqual(tiff, False)

    def test_decode(self):
        path = os.path.join(os.path.dirname(__file__),
                            'For_tests', 'primer1.bmp')
        tiff = decoding(path).decode()
        self.assertEqual(tiff, "Привет")


if __name__ == '__main__':
    unittest.main()
