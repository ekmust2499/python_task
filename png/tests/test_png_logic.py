import unittest
import os

from png import PNG
from chunk_parser import *
from filters import *


class PNGLogicTest(unittest.TestCase):
    def setUp(self):
        self.file = '7.png'
        self.pixels = PNG()

    def test_filters(self):
        filter_one = Filter()
        with self.assertRaises(NotImplementedError):
            filter_one.filter(1, 2, 3, 4)
        with self.assertRaises(NotImplementedError):
            filter_one.reconstruct(1, 2, 3, 4)

        filter_two = NoneFilter()
        self.assertEqual(filter_two.filter(1, 2, 3, 4), 1)
        self.assertEqual(filter_two.reconstruct(1, 2, 3, 4), 1)

        filter_three = SubFilter()
        self.assertEqual(filter_three.filter(5, 2, 3, 4), 3)
        self.assertEqual(filter_three.reconstruct(5, 2, 3, 4), 7)

        filter_four = UpFilter()
        self.assertEqual(filter_four.filter(5, 2, 3, 4), 2)
        self.assertEqual(filter_four.reconstruct(5, 2, 3, 4), 8)

        filter_five = AverageFilter()
        self.assertEqual(filter_five.filter(5, 2, 3, 4), 3)
        self.assertEqual(filter_five.reconstruct(5, 2, 3, 4), 7)

        filter_six = PaethFilter()
        self.assertEqual(filter_six.filter(5, 2, 2, 4), 3)
        self.assertEqual(filter_six.reconstruct(5, 2, 2, 4), 7)
        self.assertEqual(filter_six.filter(5, 1, 4, 2), 1)
        self.assertEqual(filter_six.reconstruct(5, 5, 4, 3), 10)

    def test_reconstruct(self):
        self.assertEqual(reconstruct_scanline(FILTER[0], [5, 6]), [5, 6])

    def test_not_png(self):
        self.assertFalse(self.pixels.open_png('1.bmp'))

    def test_nothing_file(self):
        self.assertFalse(self.pixels.open_png('99.txt'))

    def test_main(self):
        png = PNG()
        if png.open_png(self.file) is not False:
            self.assertTrue(png.print_info_about_png('out.txt'))

    def test_get_chunk(self):
        self.pixels.open_png('0.bmp')
        self.assertEqual(len(self.pixels.list_pixel), 0)
        if self.pixels.open_png(self.file) is not False:
            self.assertEqual(self.pixels.list_pixel,
                             [[(168, 32, 112), (255, 255, 255)],
                              [(255, 255, 255), (168, 32, 112)]])

    def test_print_data_png(self):
        self.pixels.list_pixel = [[(1, 1), (2, 2)], [(3, 3), (4, 4)]]
        self.assertTrue(self.pixels.print_info_about_png('out.txt'))
        self.assertTrue(os.path.exists('out.txt'))

    def test_any_chunk(self):
        chunk = Chunk(4, "gAMA", bytearray(b'\x00\x00\x00\x04gAMA'
                                           b'\x00\x00\xb1\x8f\x0b\xfca\x05'))
        self.assertEqual(chunk.get_chunk(), "<Chunk: 'gAMA', "
                                            "length=4, crc=0BFC6105>")
        chunk.all_data = b'\x00\x00\x00\x04gAMA\x00\x00'
        with self.assertRaises(ValueError):
            chunk.check_chunk()
        chunk.all_data = b'\x00\x00\x00\x04gAMA\x00\x00\xb1' \
                         b'\x8f\x0b\xfca\x05'
        chunk.length = 3
        with self.assertRaises(ValueError):
            chunk.check_chunk()
        chunk.length = 4
        self.assertEqual(chunk.get_raw_name(), b"gAMA")
        chunk.name = "python"
        with self.assertRaises(ValueError):
            chunk.check_chunk()
        chunk.name = "Питон"
        with self.assertRaises(ValueError):
            chunk.check_chunk()

    def test_chunk_ihdr(self):
        ihdr = IHDR(13, "IHDR", bytearray(b"\x00\x00\x00\rIHDR"
                                          b"\x00\x00\x00\x02\x00"
                                          b"\x00\x00\x02\x10\x02"
                                          b"\x00\x00\x00\xadDF0"))
        self.assertTrue(ihdr.check_ihdr_data())
        self.assertEqual(ihdr.get_chunk(), "<Chunk: 'IHDR', "
                                           "length=13, geometry=2x2, "
                                           "bit_depth=16, color_type=RGB, "
                                           "compression_method=0, "
                                           "filter_method=0, "
                                           "interlace_method=no "
                                           "interlace>")

    def test_chunk_ihdr_false(self):
        ihdr = IHDR(13, "IHDR", bytearray(b"\x00\x00\x00\rIHDR"
                                          b"\x00\x00\x00\x02\x00"
                                          b"\x00\x00\x02\x10\x02"
                                          b"\x00\x00\x00\xadDF0"))
        ihdr.data = ihdr.data[:5]
        self.assertFalse(ihdr.check_ihdr_data())

    def test_chunk_plte(self):
        plte = PLTE(264, "PLTE",
                    bytearray(b'\x00\x00\x01\x08PLTE'
                              b'\x00\x00\x00m\x82\x9cTq'
                              b'\x98Nk\x94Ii\x8fA`\x8a2S'
                              b'\x7f.O{)Jw(Hv\x1c=j\x1c=k'
                              b'\x1e?m\x167d\x1b;g'
                              b'\x00\x00\x00\x00e\xcb\x01\r\x1c'
                              b'\x03a\xce\x04\x1b7\x06 A\x06!B'
                              b'\x06]\xd0\x07[\xd3\x08%J\x08Y\xd4'
                              b'\x08Z\xd3\x0c*Q\x0cS\xd7\x0cT\xd7\r,U'
                              b'\x0eP\xd9\x0eP\xda\x0f.X\x11K\xdd'
                              b'\x12I\xdf\x13H\xdf\x14G\xe0\x187`\x19;h'
                              b'\x1b:b\x1c;c\x1d=k\x1d>k\x1d>l\x1e=f)R'
                              b'\xc8/Lt2Q|2V\xbf7W\xa88X\x9e8Z\x85@_'
                              b'\xb7C`\xb5Da\xb4P\x83\xfeQ^iRs\xc3T~'
                              b'\xe5U{\xd9Vbhc\x88\xa8h|\x91m\x87\xb2t'
                              b'\x84\x99y\x93\xa8|\x8b\x9a}wY'
                              b'\x80{`\x86\xa8\xc2\x87\x82c'
                              b'\x8a\x84f\x90\xa0\xa0\x93'
                              b'\x9a\xa2\x96\xba\xd6\x97'
                              b'\x91s\x9b\x95w\x9e\xde\xe8'
                              b'\xa8\xa9\x9e\xb1\xcf\xc6'
                              b'\xb9\xb3\x95\xbc\xb7\x9b'
                              b'\xbe\xbb\xa5\xca\xc4\xa6'
                              b'\xd3\xcc\xaf\xd7\xd1\xb3'
                              b'\xff\xff\xff\xbd\x90\xfe\xd4'))
        self.assertEqual(plte.get_palette(),
                         [(0, 0, 0), (109, 130, 156),
                          (84, 113, 152), (78, 107, 148),
                          (73, 105, 143), (65, 96, 138),
                          (50, 83, 127), (46, 79, 123),
                          (41, 74, 119), (40, 72, 118),
                          (28, 61, 106), (28, 61, 107),
                          (30, 63, 109), (22, 55, 100),
                          (27, 59, 103), (0, 0, 0),
                          (0, 101, 203), (1, 13, 28),
                          (3, 97, 206), (4, 27, 55),
                          (6, 32, 65), (6, 33, 66),
                          (6, 93, 208), (7, 91, 211),
                          (8, 37, 74), (8, 89, 212),
                          (8, 90, 211), (12, 42, 81),
                          (12, 83, 215), (12, 84, 215),
                          (13, 44, 85), (14, 80, 217),
                          (14, 80, 218), (15, 46, 88),
                          (17, 75, 221), (18, 73, 223),
                          (19, 72, 223), (20, 71, 224),
                          (24, 55, 96), (25, 59, 104),
                          (27, 58, 98), (28, 59, 99),
                          (29, 61, 107), (29, 62, 107),
                          (29, 62, 108), (30, 61, 102),
                          (41, 82, 200), (47, 76, 116),
                          (50, 81, 124), (50, 86, 191),
                          (55, 87, 168), (56, 88, 158),
                          (56, 90, 133), (64, 95, 183),
                          (67, 96, 181), (68, 97, 180),
                          (80, 131, 254), (81, 94, 105),
                          (82, 115, 195), (84, 126, 229),
                          (85, 123, 217), (86, 98, 104),
                          (99, 136, 168), (104, 124, 145),
                          (109, 135, 178), (116, 132, 153),
                          (121, 147, 168), (124, 139, 154),
                          (125, 119, 89), (128, 123, 96),
                          (134, 168, 194), (135, 130, 99),
                          (138, 132, 102), (144, 160, 160),
                          (147, 154, 162), (150, 186, 214),
                          (151, 145, 115), (155, 149, 119),
                          (158, 222, 232), (168, 169, 158),
                          (177, 207, 198), (185, 179, 149),
                          (188, 183, 155), (190, 187, 165),
                          (202, 196, 166), (211, 204, 175),
                          (215, 209, 179), (255, 255, 255)])
        self.assertEqual(plte.get_chunk(), "<Chunk: 'PLTE', "
                                           "length=264, crc=BD90FED4>")

    def test_chunk_iend(self):
        iend = IEND(0, "IEND", bytearray(b'\x00\x00\x00\x00IEND\xaeB`\x82'))
        self.assertEqual(iend.get_chunk(), "<Chunk: 'IEND', "
                                           "length=0, crc=AE426082>")

    def test_chunk_idat(self):
        idat_data_one = bytearray(b'x\xdabX\xb1TA\xa1'
                                  b'\xa0\xe0\xff\xff\xff\xff'
                                  b'\xff\xffg\x80P\x10!'
                                  b'\x00\x00\x00\x00\xff\xff'
                                  b'\x03\x00\xdcG\x10\xcf')
        idat_data_two = (b'\x00\x00\x00!IDATx\xdabX'
                         b'\xb1TA\xa1\xa0\xe0\xff'
                         b'\xff\xff\xff\xff\xffg\x80P'
                         b'\x10!\x00\x00\x00\x00\xff'
                         b'\xff\x03\x00\xdcG\x10\xcf\xb4R\xdbR')
        idat = IDAT(33, "IDAT", idat_data_two, 16, 2, 2, 2, [])
        self.assertEqual(idat.get_chunk(), "<Chunk: 'IDAT', "
                                           "length=33, crc=B452DB52>")
        self.assertEqual(idat.get_list_pixel(idat_data_one),
                         [[(168, 32, 112), (255, 255, 255)],
                          [(255, 255, 255), (168, 32, 112)]])


if __name__ == '__main__':
    unittest.main()
