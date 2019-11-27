import sys
from encode import open_file_for_encoding
from decode import decoding, write_in_file


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print(
            """
            This program is a steganography of BMP.
            This is a way of transferring or storing information,
            taking into account the fact that such a transfer is kept secret.
            The program is implemented based on the LSB method,
            that is, replacing the last significant bits in the
            container with bits of the hidden message.
            To encode a message in a BMP image, you need to enter:
            python main.py -e [item1] [in.txt] [item3] [empty/item4]
            item1 - path to bmp-picture without encryption
            in.txt - path to a text file in.txt with text for encryption
            item3 - the name of the bmp image where
            the message will be encrypted
            item4 - number of bits to be replaced for encryption
            To decode the message, enter:
            python main.py -d [item1] [out.txt]
            item1 - path to bmp-picture with encrypted message
            out.txt - path to the text file out.txt where the decrypted
            message will be written
            """
        )
    elif sys.argv[1] == "-e" and len(sys.argv) == 6:
        open_file_for_encoding(sys.argv[2], sys.argv[3],
                               sys.argv[4], sys.argv[5])
    elif sys.argv[1] == "-e" and len(sys.argv) == 5:
        open_file_for_encoding(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-d" and len(sys.argv) == 4:
        result = decoding(sys.argv[2])
        if result is False:
            print("Oops! Something went wrong...")
        else:
            write_in_file(sys.argv[3], result)
    else:
        print("You entered incorrect parameters")


if __name__ == "__main__":
    main()
