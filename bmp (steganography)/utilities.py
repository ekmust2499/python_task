import base64
import codecs
import math
from random import SystemRandom


class Utilities:
    def __init__(self, prime="115792089237316195423570985008687"
                 "907853269984665640564039457584007913129639747"):
        self.prime = int(prime)

    def random(self) -> int:
        """
        The function of choosing a random number up to a prime number
        """
        return SystemRandom().randrange(self.prime)

    def split_ints(self, secret: (bytes, str)) -> list():
        """
        Function of division into numbersFunction of division into numbers
        """
        result = []
        try:
            byte_object = bytes(secret, "utf8")
        except TypeError:
            byte_object = bytes(secret)
        text = (codecs.encode(byte_object, 'hex_codec').decode('utf8') +
                "00" * (32 - (len(byte_object) % 32)))
        for i in range(0, int(len(text)/64)):
            result.append(int(text[i*64:(i+1)*64], 16))
        return result

    def merge_ints(self, secrets: list()) -> (str, False):
        """
        Function of merging numbers
        """
        result = ""
        for secret in secrets:
            hex_data = hex(secret)[2:].replace("L", "")
            result += "0"*(64 - (len(hex_data))) + hex_data
        try:
            byte_object = bytes(result, "utf-8")
            x = codecs.decode(byte_object, 'hex_codec')
            y = x.decode("utf-8").rstrip("\00\x00")
            return y
        except UnicodeDecodeError:
            return False

    def evaluate_polynomial(self, coefficients: list(), value: int) -> list():
        """
        Function of creating a polynomial
        """
        result = 0
        for coefficient in reversed(coefficients):
            result = result * value + coefficient
            result = result % self.prime
        return result

    def to_base64(self, number: int) -> (str, None):
        """
        The function of converting from a number to base64
        """
        tmp = hex(number)[2:].replace("L", "")
        tmp = "0"*(64 - len(tmp)) + tmp
        try:
            tmp = bytes(tmp, "utf8")
        except TypeError:
            tmp = bytes(tmp)
        result = (str(base64.urlsafe_b64encode(b'\00'*(64 - len(tmp)) +
                  codecs.decode(tmp, 'hex_codec')).decode('utf8')))
        if len(result) != 44:
            print("Invalid conversion!")
            return None
        return result

    def from_base64(self, number: str) -> int:
        """
        The conversion function from base64 to a number
        """
        byte_number = number
        try:
            byte_number = bytes(byte_number, "utf8")
        except TypeError:
            byte_number = bytes(byte_number)
        tmp = base64.urlsafe_b64decode(byte_number)
        try:
            tmp = bytes(tmp, "utf8")
        except TypeError:
            tmp = bytes(tmp)
        result = int(codecs.encode(tmp, 'hex_codec'), 16)
        return result

    def nod(self, a: int, b: int) -> list():
        """
        GCD computation function
        """
        if b == 0:
            return [a, 1, 0]
        else:
            n = int(math.floor(a*1.0/b))
            c = a % b
            r = self.nod(b, c)
            return [r[0], r[2], r[1] - r[2]*n]

    def mod_inverse(self, number: int) -> int:
        """
        The function of inverse computation of a polynomial
        """
        remainder = (self.nod(self.prime, number % self.prime))[2]
        if number < 0:
            remainder *= -1
        x = (self.prime + remainder) % self.prime
        return x
