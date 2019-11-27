from utilities import Utilities


class SecretSharing:
    def __init__(self):
        self.prime = str("115792089237316195423570985008687907853269"
                         "984665640564039457584007913129639747")
        self.util = Utilities()

    def divide(self, minimum: int, shares: int,
               text: (str, bytes)) -> (list(), False):
        """
        The main function of dividing the message into shares
        """
        if shares < minimum:
            return
        secret = self.util.split_ints(text)
        numbers = [0]
        polynomial = []
        for i in range(len(secret)):
            polynomial.append([secret[i]])
            for j in range(1, minimum):
                value = self.util.random()
                while value in numbers:
                    value = self.util.random()
                numbers.append(value)
                polynomial[i].append(value)
        result = [""] * shares
        for i in range(shares):
            for j in range(len(secret)):
                value = self.util.random()
                while value in numbers:
                    value = self.util.random()
                numbers.append(value)
                polynom = self.util.evaluate_polynomial(polynomial[j], value)
                val = self.util.to_base64(value)
                if val is None:
                    return False
                pol = self.util.to_base64(polynom)
                if pol is None:
                    return False
                result[i] += val
                result[i] += pol
        return result

    def unite(self, shares: list()) -> (str, False):
        """
        The main function of the connection from the fraction of the message
        """
        secrets = []
        for index, share in enumerate(shares):
            if len(share) % 88 != 0:
                return False
            count = int(len(share) / 88)
            secrets.append([])
            for i in range(count):
                split_share = share[i*88:(i+1)*88]
                one = self.util.from_base64(split_share[0:44])
                two = self.util.from_base64(split_share[44:88])
                secrets[index].append([one, two])

        secret = [0] * len(secrets[0])

        for part_index, part in enumerate(secret):
            for share_index, share in enumerate(secrets):
                origin = share[part_index][0]
                origin_y = share[part_index][1]
                numerator = 1
                denominator = 1
                for product_index, product in enumerate(secrets):
                    if product_index != share_index:
                        current = product[part_index][0]
                        numerator = ((numerator * (-1*current)) %
                                     self.util.prime)
                        denominator = ((denominator * (origin - current))
                                       % self.util.prime)
                working = (((origin_y * numerator *
                            self.util.mod_inverse(denominator)) +
                            self.util.prime))
                secret[part_index] = ((secret[part_index] + working) %
                                      self.util.prime)
        result = self.util.merge_ints(secret)
        return result
