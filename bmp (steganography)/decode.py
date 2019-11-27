from struct import unpack_from
from math import ceil
import binascii


def main_decoding(encoded: bytearray, spent_bits: int,
                  number_bits=8, index=0) -> int:
    """
    Function of extracting information from one byte
    """
    enumerator = 0
    shift = 0
    total = 0
    everything_is_encoding = False
    bits_left = number_bits
    for index in range(index, len(encoded)):
        difference = 0
        if bits_left < spent_bits:
            difference = spent_bits - bits_left
        total <<= shift - difference
        shift = 0
        for i in range(spent_bits - 1, -1, -1):
            if ((encoded[index] >> i) & 1) == 1:
                total |= 1 << i - difference
            else:
                total |= 0 << i - difference
            enumerator += 1
            if enumerator == number_bits:
                everything_is_encoding = True
                break
            shift += 1
        bits_left -= spent_bits
        if everything_is_encoding is True:
            break
    return total


def decoding_multiple_characters(encoded: bytearray, spent_bits: int,
                                 length_encoded_in_bytes=None) -> bytearray:
    """
    The function of decoding information from a sequence of symbols
    """
    result = bytearray()
    if length_encoded_in_bytes is not None:
        length_encoded = length_encoded_in_bytes
    else:
        length_encoded = len(encoded)
    for i in range(int(length_encoded)):
        result.append(main_decoding(encoded, spent_bits, 8,
                                    ceil(8 / spent_bits) * i))
    return result


def bmp_header(bmp_file: bytearray) -> (str, int):
    """
    The function to collect information about the header of the BMP file
    """
    bf = unpack_from('<2sIHHI', bmp_file)
    bf_type = bf[0].decode()
    bf_off_bits = bf[4]
    return bf_type, bf_off_bits


def decoding(file_to_decode_path: str) -> (bytearray, False):
    """
    The main function of decrypting the message
    """
    with open(file_to_decode_path, 'rb') as bmp_f:
        bmp = bytearray(bmp_f.read())
        code_word = b'coded'
        try:
            bf_type, bf_off_bits = bmp_header(bmp)
            if bf_type != "BM":
                raise FileExistsError()
        except FileExistsError:
            print("This is file not is BMP!")
            return False

        bmp = bmp[bf_off_bits:]
        try:
            decoded_msg = decoding_multiple_characters(bmp, 1, len(code_word))
            if code_word != decoded_msg:
                raise ValueError()
        except ValueError:
            print("This file doesn't encoded...")
            return False

        bmp = bmp[len(code_word) * 8:]

        const = b'E=mc^2'
        try:
            decoded_const = decoding_multiple_characters(bmp, 1, len(const))
            if const != decoded_const:
                raise ValueError()
        except ValueError:
            print("In this file, not my message! Dangerous!!!")
            return False
        bmp = bmp[len(const) * 8:]

        control_sum = bmp[:64]
        control_sum = decoding_multiple_characters(control_sum, 1, 8)
        bmp = bmp[64:]

        file_length = bmp[:32]
        bmp = bmp[32:]
        file_length = main_decoding(file_length, 1, 32)

        num_bits_for_encoding = bmp[:4]
        bmp = bmp[4:]
        num_bits_for_encoding = main_decoding(num_bits_for_encoding, 1, 4)
        result = decoding_multiple_characters(bmp, num_bits_for_encoding,
                                              file_length)

        crc = (binascii.crc32(bytes(result)) & 0xFFFFFFFF)
        crc32 = "%08x" % crc

        if crc32.encode() == control_sum:
            return result
        else:
            return False


def write_in_file(out_file_path: str, result: bytearray) -> None:
    """
    The function of writing an array of bytes in a file
    """
    with open(out_file_path, 'wb') as file:
        file.write(result)
