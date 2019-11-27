import sys
import struct
from chunk_parser import Chunk, IHDR, IDAT, IEND, PLTE

PNG_Signature = '89504E470D0A1A0A'


class PNG(object):
    """PNG internal structure description class"""
    def __init__(self):

        self.list_chunks = list()
        self.list_pixel = list()
        self.count_chunks = 0
        self.png_name = ""
        self.png_length = 0
        self.palette = list()
        self.width = 0
        self.height = 0
        self.chunk_obj = ""
        self.color_type = ""

    def get_chunks(self, png):
        """The function of getting all image chunks and a list of pixels"""
        start_chunk = 8
        bit_depth = 0
        data_idat = bytearray()
        length_idat = 0
        name_idat = ""

        while start_chunk < self.png_length:
            (length_chunk, name_chunk) = struct.unpack(
                ">I4s", png[start_chunk:start_chunk + 8])
            name_chunk = name_chunk.decode('ascii')

            end_chunk = start_chunk + length_chunk + 12
            data_chunk = png[start_chunk:end_chunk]
            if name_chunk == 'IHDR':
                try:
                    self.chunk_obj = IHDR(length_chunk, name_chunk, data_chunk)
                    bit_depth = self.chunk_obj.bit_depth
                    self.color_type = self.chunk_obj.color_type
                    self.width = self.chunk_obj.width
                    self.height = self.chunk_obj.height
                except ValueError:
                    return False
            elif name_chunk == 'PLTE':
                self.chunk_obj = PLTE(length_chunk, name_chunk, data_chunk)
                self.palette = self.chunk_obj.get_palette()
            elif name_chunk == 'IDAT':
                self.chunk_obj = IDAT(length_chunk,
                                      name_chunk, data_chunk,
                                      bit_depth, self.color_type,
                                      self.width, self.height,
                                      self.palette)
                data_idat = data_idat + self.chunk_obj.data
                length_idat = length_idat + length_chunk
                name_idat = name_chunk
            elif name_chunk == 'IEND':
                self.chunk_obj = IEND(length_chunk, name_chunk, data_chunk)
            else:
                self.chunk_obj = Chunk(length_chunk, name_chunk, data_chunk)
            try:
                chunk = self.chunk_obj.get_chunk()
            except ValueError:
                return False
            self.count_chunks += 1
            self.list_chunks.append(chunk)

            start_chunk = end_chunk
        self.chunk_obj = IDAT(length_idat, name_idat,
                              data_idat, bit_depth,
                              self.color_type, self.width,
                              self.height, self.palette)
        self.list_pixel = self.chunk_obj.get_list_pixel(data_idat)

    def open_png(self, file_png):
        """Image open function"""
        try:
            with open(file_png, 'rb') as png_f:
                self.png_name = file_png
                png = bytearray(png_f.read())
            self.png_length = len(png)
            png_header = png[:8]
            png_header = png_header.hex().upper()
            if png_header != PNG_Signature:
                return False
            if self.get_chunks(png) is False:
                return False
        except FileNotFoundError:
            return False

    def print_info_about_png(self, file):
        """
        The function of outputting the internal
        structure of the image to the console
        """
        with open(file, "w") as file_out:
            file_out.write("<PNG file: '{0}', length={1}, "
                           "count chunks={2}>".format(self.png_name,
                                                      self.png_length,
                                                      self.count_chunks
                                                      ) + "\n")
            for chunk in self.list_chunks:
                file_out.write(chunk + "\n")
            for line in self.list_pixel:
                for pixel in line:
                    file_out.write(str(pixel))
                file_out.write("\n")
        return True


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print(
            """
            This program extracts data from a PNG image and
            describes the internal structure of the file.
            To run the program, enter:
            python png.py [image]
            image - PNG format file""")
    else:
        if len(sys.argv) != 3:
            sys.stderr.write("Неверный формат строки")
        else:
            png = PNG()
            if png.open_png(sys.argv[1]) is not False:
                png.print_info_about_png(sys.argv[2])


if __name__ == '__main__':
    main()
