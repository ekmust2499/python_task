import unittest
import os
from billing import *


class TestBilling(unittest.TestCase):
    def setUp(self):
        self.file = 'log.txt'
        self.parser = Parser()

    def test_open_log_file(self):
        self.parser.data_from_file(self.file)
        self.assertTrue(len(self.parser.data_for_id.items()) != 0)
        self.assertIsNone(self.parser.data_from_file("billing"))

    def test_time_call(self):
        self.assertEqual(self.parser.time_call("01:55:02"), 6902)

    def test_call_time_counting(self):
        self.assertEqual(self.parser.call_time_counting("01:55:02",
                                                        "01:56:48"), 106)

    def test_counting_cost(self):
        pull_tariffs()
        self.assertEqual(self.parser.counting_cost("\"Black\"", "OUT_I",
                                                   100), 3.2)
        self.assertEqual(self.parser.counting_cost("\"Black\"", "OUT_O",
                                                   100), 5.2)
        self.assertEqual(self.parser.counting_cost("\"Black\"", "IN_I",
                                                   100), 0.2)
        self.assertEqual(self.parser.counting_cost("\"Black\"", "IN_O",
                                                   100), 0.8)

    def test_check_on_exception(self):
        line = "2018/10/12 | 13:02:58 | 13:07:42 | 00:04:44 | " \
               "OUT_O | 79514882403 | 79025167525 | \"Black\" | " \
               "Фёдоров Павел Анатольевич | Россия, Архангельская область, " \
               "Онега, Малышева, 41, 78"
        list_data = list(re.split(r' \| ', line.rstrip()))
        self.assertFalse(self.parser.check_on_exception(list_data, "17", line))
        self.assertTrue(self.parser.check_on_exception(list_data, "", line))

    def test_get_data(self):
        pull_tariffs()
        self.parser.data_for_id = {
            '17': [['2018/10/12', '13:02:58', '13:07:42',
                    '00:04:44', 'OUT_O', '79514882403',
                    '79025167525', '"Black"', 'Фёдоров Павел Анатольевич',
                    'Россия, Архангельская область, Онега, Малышева, 41, 78'],
                   ['2018/10/11', '15:00:11', '15:02:15', '00:02:04',
                    'OUT_I', '79514882403', '79024163724', '"Black"',
                    'Фёдоров Павел Анатольевич',
                    'Россия, Архангельская область, Онега, Малышева, 41, 78']],
            '11': [['2018/10/13', '14:05:32', '14:36:54', '00:31:22',
                    'IN_I', '79527916822', '79849599301', '"Red"',
                    'Будько Иван Степанович',
                    'Россия, Московская область, Москва, Гагарина, 169, 52'],
                   ['2018/10/05', '11:08:14', '12:08:54', '01:00:40',
                    'IN_O', '79527916822', '79849594332', '"Red"',
                    'Будько Иван Степанович', 'Россия, Московская область, '
                                              'Москва, Гагарина, 169, 52']]
        }
        dict_out = {
            '17': ['Фёдоров Павел Анатольевич', '79514882403',
                   '"Black"', 2, 0, 2, 408, 0, 408, 17.8],
            '11': ['Будько Иван Степанович', '79527916822',
                   '"Red"', 2, 2, 0, 5522, 5522, 0, 64.35]}
        self.parser.handler_for_every_id()
        self.assertDictEqual(dict_out, self.parser.out_for_id)

    def test_print_data(self):
        self.parser.out_for_id = {
            '17': ['Фёдоров Павел Анатольевич', '79514882403',
                   '"Black"', 9, 4, 5, 11050, 6661, 4389, 210.8],
            '11': ['Будько Иван Степанович', '79527916822',
                   '"Red"', 7, 4, 3, 15531, 8953, 6578, 311.05],
            '15': ['Климова Ольга Леонидовна', '79524420362',
                   '"Yellow"', 6, 2, 4, 16883, 9124, 7759, 352.5],
            '22': ['Алуфьева Мария Наумовна', '79858836101',
                   '"Blue"', 6, 2, 4, 8716, 3937, 4779, 358.8],
            '8': ['Щукин Борис Григорьевич', '79074925635',
                  '"Green"', 7, 1, 6, 23833, 3743, 20090, 380.4]}
        self.parser.print_in_file()
        self.assertTrue(os.path.exists('8.txt'))
        self.assertTrue(os.path.exists('error_data.txt'))
        self.assertFalse(os.path.exists('65556.txt'))


if __name__ == '__main__':
    unittest.main()
