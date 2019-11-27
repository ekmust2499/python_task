import struct
import string
import zlib
import math

from bitstring import BitArray
from filters import FILTER, reconstruct_scanline


class Chunk():
    def __init__(self, length=None, name=None, data=None):
        self.length = length
        self.name = name
        self.all_data = data
        self.data = b""
        self.crc = 0

    def check_chunk(self):
        """Data validation function"""
        if not self.check_length_all_data():
            raise ValueError
        if not self.check_length():
            raise ValueError
        if not self.check_name():
            raise ValueError
        if not self.check_crc():
            raise ValueError

    def get_chunk(self):
        """Chunk information retrieval function"""
        self.check_chunk()
        return (f"<Chunk: '{self.name}', length={self.length}, "
                f"crc={self.crc:08X}>")

    def check_length_all_data(self):
        """Function of checking the obtained length of all data"""
        if len(self.all_data) >= 12:
            self.data = self.all_data[8:-4]
            return True
        else:
            return False

    def check_length(self):
        """Function of checking the resulting length
        from that specified in the image"""
        if self.length != len(self.data):
            return False
        return True

    def check_name(self):
        """Image name verification function"""
        for letter in self.name:
            if letter not in string.ascii_letters:
                return False
        return True

    def check_crc(self):
        """Checksum check function"""
        self.crc = struct.unpack("!I", self.all_data[8 + self.length:
                                                     8 + self.length + 4])[0]
        crc_computation = zlib.crc32(self.get_raw_name() + self.data)
        if self.crc != crc_computation:
            return False
        return True

    def get_raw_name(self):
        """Name processing function"""
        if isinstance(self.name, bytes):
            name = self.name
        else:
            name = self.name.encode("ascii")
        return name


class IHDR(Chunk):
    color_type_gray = 0
    color_type_rgb = 2
    color_type_plte = 3
    color_type_graya = 4
    color_type_rgba = 6
    color_types = {
        color_type_gray: ("Grayscale", (1, 2, 4, 8, 16)),
        color_type_rgb: ("RGB", (8, 16)),
        color_type_plte: ("Palette", (1, 2, 4, 8)),
        color_type_graya: ("Greyscale+Alpha", (8, 16)),
        color_type_rgba: ("RGBA", (8, 16)),
    }
    interlace_types = {
        0: "no interlace",
        1: "Adam7 interlace"
    }

    def __init__(self, length, name, data):
        self.width = 0
        self.height = 0
        self.bit_depth = 0
        self.color_type = 0
        self.compression_method = 0
        self.filter_method = 0
        self.interlace_method = 0
        super().__init__(length, name, data)
        self.init_attributs_ihdr()

    def init_attributs_ihdr(self):
        """IHDR attribute initialization function"""
        super().check_chunk()
        if not self.check_ihdr_data():
            raise ValueError
        data_unpack = struct.unpack(">IIBBBBB", self.data)
        self.width = data_unpack[0]
        self.height = data_unpack[1]
        self.bit_depth = data_unpack[2]
        self.color_type = data_unpack[3]
        self.compression_method = data_unpack[4]
        self.filter_method = data_unpack[5]
        self.interlace_method = data_unpack[6]

    def get_chunk(self):
        """Chunk information retrieval function"""
        return f"<Chunk: '{self.name}', length={self.length}, " \
            f"geometry={self.width}x{self.height}, " \
            f"bit_depth={self.bit_depth}, " \
            f"color_type={self.color_types[self.color_type][0]}, " \
            f"compression_method={self.compression_method}, " \
            f"filter_method={self.filter_method}, " \
            f"interlace_method=" \
            f"{self.interlace_types[self.interlace_method]}>"\


    def check_ihdr_data(self):
        """IHDR chunk data check function"""
        if len(self.data) != 13:
            return False
        return True


class PLTE(Chunk):
    def __init__(self, length, name, data):
        super().__init__(length, name, data)

    def get_chunk(self):
        """Chunk information retrieval function"""
        return (f"<Chunk: '{self.name}', length={self.length}, "
                f"crc={self.crc:08X}>")

    def get_palette(self):
        """Function to get the color palette in the image"""
        super().check_chunk()
        if len(self.data) % 3 != 0:
            raise ValueError
        z = BitArray(hex=self.data.hex()).bin
        start = 0
        end = 8
        array = list()
        while end <= len(z):
            line = z[start:end]
            linex = int(line, 2)
            array.append(linex)
            start = start + 8
            end = end + 8
        if len(array) % 3 != 0:
            raise ValueError
        palette = list()
        num_element = 0
        while num_element <= len(array) - 3:
            elements = list()
            elements.append(array[num_element])
            elements.append(array[num_element+1])
            elements.append(array[num_element+2])
            palette.append(tuple(elements))
            num_element = num_element + 3
        return palette


class IDAT(Chunk):
    colors_bit_depth = {
        '0': ['1', '2', '4', '8', '16'],
        '2': ['8', '16'],
        '3': ['1', '2', '4', '8'],
        '4': ['8', '16'],
        '6': ['8', '16']
    }
    colors = {
        '0': 1,
        '2': 3,
        '3': 1,
        '4': 2,
        '6': 4}

    def __init__(self, length, name, data, bit_depth,
                 color_type, width, height, palette=None):
        super().__init__(length, name, data)
        super().check_length_all_data()
        self.bit_depth = bit_depth
        self.color_type = color_type
        self.width = int(width)
        self.height = int(height)
        self.palette = palette

    @staticmethod
    def filters(line_size, decompressed, pixel_size):
        """IDAT chunk filtering function"""
        scanlines = []
        filter_bytes = []
        for i in range(0, len(decompressed), line_size):
            filter_bytes.append(decompressed[i])
            scanlines.append(decompressed[i + 1:i + line_size])
        reconstructed_scanlines = []
        for p in range(len(scanlines)):
            reconstructed_scanline = reconstruct_scanline(
                FILTER[filter_bytes[p]],
                scanlines[p],
                reconstructed_scanlines[p - 1] if p > 0 else None,
                pixel_size
            )
            reconstructed_scanlines.append(reconstructed_scanline)
        return reconstructed_scanlines

    def get_list_pixel(self, data):
        """Pixel list function"""
        decompress = zlib.decompressobj(zlib.MAX_WBITS | 32)
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        count_bits_on_pix = self.colors[str(self.color_type)] * self.bit_depth
        count_bytes_on_pix = int(count_bits_on_pix / 8)
        count_bytes_on_line = count_bytes_on_pix * self.width + 1
        count_bits_on_line = count_bytes_on_line * 8
        count_lines = int(len(inflated) / count_bytes_on_line)

        list_otfilter_bytes = self.filters(count_bytes_on_line,
                                           inflated, count_bytes_on_pix)
        list_pixels = list()
        for line in list_otfilter_bytes:
            list_pix_in_line = list()
            start_pix = 0
            end_pix = count_bytes_on_pix
            while end_pix <= len(line):
                list_pix = list()
                one_pixel = line[start_pix:end_pix]
                start_pix = start_pix + count_bytes_on_pix
                end_pix = end_pix + count_bytes_on_pix
                if self.bit_depth == 16:
                    for e in range(0, len(one_pixel), 2):
                        c = "{0:{fill}8b}".format(one_pixel[e], fill='0') + \
                            "{0:{fill}8b}".format(one_pixel[e+1], fill='0')
                        r = int(c, 2)
                        x = math.ceil((255 * r) / 65535)
                        list_pix.append(x)
                    list_pix_in_line.append(tuple(list_pix))
                elif self.bit_depth == 8:
                    list_pix_in_line.append(tuple(x for x in one_pixel))
            list_pixels.append(list_pix_in_line)

        if self.color_type == 0:
            for line in list_pixels:
                for index, pixel in enumerate(line):
                    list_pix = list()
                    one = pixel[0]
                    list_pix.append(one)
                    list_pix.append(one)
                    list_pix.append(one)
                    line.remove(pixel)
                    line.insert(index, tuple(list_pix))

        if self.palette is not None and self.color_type == 3:
            for line in list_pixels:
                for index, pixel in enumerate(line):
                    one = pixel[0]
                    new_pixel = self.palette[int(one)]
                    line.remove(pixel)
                    line.insert(index, new_pixel)

        if self.color_type == 4:
            for line in list_pixels:
                for index, pixel in enumerate(line):
                    list_pix = list()
                    one = pixel[0]
                    list_pix.append(one)
                    list_pix.append(one)
                    list_pix.append(one)
                    list_pix.append(pixel[1])
                    line.remove(pixel)
                    line.insert(index, tuple(list_pix))
        return list_pixels

    def get_chunk(self):
        """Chunk information retrieval function"""
        super().check_chunk()
        return (f"<Chunk: '{self.name}', length={self.length}, "
                f"crc={self.crc:08X}>")


class IEND(Chunk):
    def __init__(self, length, name, data):
        super().__init__(length, name, data)

    def get_chunk(self):
        """Chunk information retrieval function"""
        super().check_chunk()
        return (f"<Chunk: '{self.name}', length={self.length}, "
                f"crc={self.crc:08X}>")
