import unittest
from secret import SecretSharing
from utilities import *


class TestLinksExtractor(unittest.TestCase):
    def test_div_un(self):
        shared = SecretSharing()
        values = ["Зима пришла", "•◘☺♠•♥*#0▲$",
                  "7YtCUMYhwQDryESiYabFID1PKBfKn5WS"
                  "GgJBIsDw5g2HB2AqC1r3K8GboDN"]
        minimum = [4, 6, 11]
        shares = [5, 9, 14]
        for index, value in enumerate(values):
            div = shared.divide(minimum[index], shares[index], value)
            self.assertEqual(shared.unite(div), value)

        x = shared.divide(2, 2, "I love python!")

    def test_un(self):
        shared = SecretSharing()
        shares = ['ROIsgTzhUQBQLF3uoH89r-efcVepJdxSSQJ55ruLzN8='
                  'tmTzuqq2ud5mDEFZJ48me236tyBaBJTo4-r4Ipxeyc4=',
                  'CEL23UQrmoXPFKXVwgch7ja2_GulgZUQVrT9zQKbVUE='
                  'C25orIQdOQjeNI8glb607uZxzaeT2U7CDbdiw2tIbFM=']
        self.assertEqual(shared.unite(shares), "I love python!")

    def test_random(self):
        util = Utilities()
        for i in range(1000):
            self.assertEqual(util.random() < util.prime, True)

    def test_base_conversion(self):
        util = Utilities()
        for i in range(1000):
            value = util.random()
            self.assertEqual(util.from_base64(util.to_base64(value)), value)

    def test_to_base64(self):
        util = Utilities()
        for i in range(1000):
            value = util.random()
            self.assertEqual(len(util.to_base64(value)), 44)

    def test_evaluate_polynomial(self):
        util = Utilities()
        values = [[[15, 8, 36], 0], [[1, 2, 3, 4, 5], 10], [[0, 0, 0], 3]]
        results = [15, 54321, 0]
        for index, value in enumerate(values):
            polynom = util.evaluate_polynomial(value[0], value[1])
            self.assertEqual(polynom, results[index])

    def test_mod_inverse(self):
        util = Utilities()
        for i in range(1000):
            value = util.random()
            self.assertEqual((value * util.mod_inverse(value)) % util.prime, 1)

    def test_split_merge1(self):
        util = Utilities()
        values = ["ь" + "\0" * 100 + "z", "w" * 31 + "哈囉世界",
                  "♠•☺◘▲◙♫☼◄", "こんにちは、世界" * 8]
        for value in values:
            self.assertEqual(util.merge_ints(util.split_ints(value)), value)

    def test_split_merge2(self):
        util = Utilities()
        values = ["Мама", "Папа"]
        for value in values:
            x = util.split_ints(value)
            y = util.merge_ints(x)
            self.assertEqual(y, value)


if __name__ == '__main__':
    unittest.main()
