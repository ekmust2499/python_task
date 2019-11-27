import os
import sys
import glob
from encode import encoding, write_in_file
from decode import decoding
from secret import SecretSharing


def for_encode(dir_with_bmp: str, text: str,
               dir_after_enc: str, bit_count=1) -> None:
    count_file_bmp = 0
    for _ in glob.glob(os.path.join(dir_with_bmp, '*.bmp')):
        count_file_bmp += 1
    delimiter = SecretSharing()
    counter = 0
    with open(text, "r") as file_f:
        file = file_f.read().encode("utf-8")
        shares = delimiter.divide(count_file_bmp, count_file_bmp, file)
        if shares is False:
            print("The division failed!")
            sys.exit(2)
    for filename in glob.glob(os.path.join(sys.argv[2], '*.bmp')):
        new_name = ("{0}".format(dir_after_enc) + '\\' +
                    filename.split('\\')[-1].split('.')[0] + "_new")
        share = bytearray(shares[counter].encode("utf-8"))
        header = encoding(filename, share, bit_count)
        if header is False:
            print("File encryption failed!")
            sys.exit(2)
        file = "{0}.bmp".format(new_name)
        write_in_file(file, header)
        if count_file_bmp == counter:
            break
        counter += 1


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print(
            """
            This program is a steganography of BMP,
            in which the content is encrypted on the basis of the
            Shamir secret sharing scheme
            (the Lagrange interpolation polynomial scheme).
            To separate the secret, a polynomial of degree k-1 is created,
            where k is the number of fractions.
            To restore the secret, we need to compute
            the Lagrange interpolation polynomial.
            To encode a message in a BMP images, you need to enter:
            python share.py -e [item1] [in.txt] [item3] [empty/item4]
            item1 - path to the directory with images bmp,
            in which you want to put the message part
            in.txt - path to a text file in.txt with text for encryption
            item3 - the name of the bmp image wherepath
            to the directory into which you want to save bmp-images
            with the encrypted part of the message.
            item4 - number of bits to be replaced for encryption
            To decode the message, enter:
            python share.py -d [item1] [out.txt]
            item1 - path to the directory with bmp-pictures,
            from which you need to decrypt the message
            out.txt - path to the text file out.txt where the decrypted
            message will be written
            """
        )
    elif sys.argv[1] == "-e" and len(sys.argv) == 6:
        for_encode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == "-e" and len(sys.argv) == 5:
        for_encode(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "-d" and len(sys.argv) == 4:
        delimiter = SecretSharing()
        secrets = list()
        for filename in glob.glob(os.path.join(sys.argv[2], '*.bmp')):
            res = decoding(filename)
            if res is False:
                print("The decryption of the file failed!")
                sys.exit(2)
            result = str(res.decode("utf-8"))
            secrets.append(result)
        result = delimiter.unite(secrets)
        if result is False:
            print("The number of pictures is not enough "
                  "to decrypt the message!")
            sys.exit(2)
        else:
            with open(sys.argv[3], 'w') as file:
                file.write(result)
    else:
        print("You entered incorrect parameters!")


if __name__ == "__main__":
    main()
