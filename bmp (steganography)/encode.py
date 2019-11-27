from struct import unpack_from
from math import ceil
import binascii


def main_encoding(encoded: int, byte_in_bmp: int, spent_bits: int,
                  number_of_encoded_bits: int) -> (int, int):
    """
    Coding function in one byte
    """
    bits_shift_in_byte = spent_bits - 1
    while number_of_encoded_bits >= 0 and bits_shift_in_byte >= 0:
        if ((encoded >> number_of_encoded_bits) & 1) == 1:
            byte_in_bmp |= 1 << bits_shift_in_byte
        else:
            byte_in_bmp &= ~(1 << bits_shift_in_byte)
        number_of_encoded_bits -= 1
        bits_shift_in_byte -= 1
    return byte_in_bmp, number_of_encoded_bits


def encoding_multiple_characters(encoded: (bytearray, tuple), bmp: bytearray,
                                 spent_bits: int, count_bits: int):
    """
    Function of encoding a sequence of symbols
    """
    number_of_bytes_for_encoding = round(ceil(count_bits / spent_bits))
    for i, coded_number in enumerate(encoded):
        shift_within_container = number_of_bytes_for_encoding * i
        shift_of_coded_number = count_bits - 1
        for j in range(number_of_bytes_for_encoding):
            bmp[j + shift_within_container], shift_of_coded_number = \
                main_encoding(coded_number, bmp[j + shift_within_container],
                              spent_bits, shift_of_coded_number)
            if shift_of_coded_number < 0:
                break


def bmp_header(bmp_file: bytearray) -> (str, int):
    """
    The function to collect information about the header of the BMP file
    """
    bf = unpack_from('<2sIHHI', bmp_file)
    bf_type = bf[0].decode()
    bf_off_bits = bf[4]
    return bf_type, bf_off_bits


def encoding(file_bmp: str, file_to_encode_path: bytearray,
             bit_count=1) -> (bytearray, False):
    """
    The main function of message encryption
    """
    with open(file_bmp, "rb") as bmp_f:
        bmp = bytearray(bmp_f.read())

        file = bytearray(file_to_encode_path)
        bit_count = int(bit_count)
        code_word = b'coded'
        try:
            bf_type, bf_off_bits = bmp_header(bmp)
            if bf_type != "BM":
                raise FileExistsError()
        except FileExistsError:
            print("This is file not is BMP!")
            return False
        header = bmp[:bf_off_bits]
        bmp = bmp[bf_off_bits:]

        encoding_multiple_characters(bytearray(code_word), bmp, 1, 8)
        encoded_msg = bmp[:len(code_word) * 8]
        bmp = bmp[len(code_word) * 8:]

        const = b'E=mc^2'
        encoding_multiple_characters(bytearray(const), bmp, 1, 8)
        encoded_const = bmp[:len(const) * 8]

        bmp = bmp[len(const) * 8:]

        crc = (binascii.crc32(file) & 0xFFFFFFFF)
        crc32 = "%08x" % crc

        encoding_multiple_characters(bytearray(crc32.encode()), bmp, 1, 8)
        encoded_crc = bmp[:len(crc32) * 8]
        bmp = bmp[len(crc32) * 8:]

        file_length = len(file)
        encoding_multiple_characters((file_length,), bmp, 1, 32)
        encoded_file_length = bmp[:32]
        bmp = bmp[32:]

        encoding_multiple_characters((bit_count,), bmp, 1, 4)
        encoded_bit_count = bmp[:4]
        bmp = bmp[4:]
        try:
            if (len(file) * round(ceil(8 / bit_count))) > len(bmp):
                raise OverflowError()
        except OverflowError:
            print("The file for the encoding is too large"
                  "for this picture and the number of bits")
            return False

        encoding_multiple_characters(file, bmp, bit_count, 8)

        header.extend(encoded_msg)
        header.extend(encoded_const)
        header.extend(encoded_crc)
        header.extend(encoded_file_length)
        header.extend(encoded_bit_count)
        header.extend(bmp)
        return header


def write_in_file(file_bmp: str, header: bytearray) -> None:
    """
    The function of writing an array of bytes in a file
    """
    with open(file_bmp, 'wb') as file:
        file.write(header)


def open_file_for_encoding(file_bmp: str, file_to_encode_path: str,
                           file_result: str, bit_count=1) -> None:
    """
    Function of opening a file with a message and then coding it
     into a BMP image
    """
    with open(file_to_encode_path, "rb") as file_f:
        file = bytearray(file_f.read())
        header = encoding(file_bmp, file, bit_count)
        if header is False:
            return None
        file = "{0}.bmp".format(file_result)
        write_in_file(file, header)
