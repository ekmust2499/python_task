import sys
import re
import math


DICT_TARIFFS = dict()


def pull_tariffs():
    """
    The function of generating data about the tariff
    in the form of a dictionary. The key is the name
    of the tariff, the value is the cost of different calls.
    """
    with open("tariff.txt", "r") as file:
        for line in file:
            data_tariff = list(re.split(r' \| ', line.rstrip()))
            tariff = data_tariff[0]
            data_tariff.remove(tariff)
            DICT_TARIFFS[tariff] = data_tariff


class Parser():
    def __init__(self):
        self.data_for_id = {}
        self.tariff = ""
        self.out_for_id = dict()

    def data_from_file(self, file_in):
        """
        The function reads data from the log file
        and forms a dictionary in which
        the key is the subscriber's identifier,
        and the value is a list of all its calls
        """
        try:
            with open(file_in, "r") as log:
                for line in log:
                    data = list(re.split(r' \| ', line.rstrip()))
                    id_abonent = data[8]
                    data.remove(id_abonent)
                    checker = self.check_on_exception(data, id_abonent, line)
                    if checker is True:
                        continue
                    if id_abonent not in self.data_for_id.keys():
                        self.data_for_id[id_abonent] = list()
                    self.data_for_id[id_abonent].append(data)
        except FileNotFoundError:
            print("No such file or directory: '{}'".format(file_in))
            return None

    def handler_for_every_id(self):
        """
        The function generates all the detailed information
        about all calls for each subscriber.
        """
        print(self.data_for_id)
        for key, value in self.data_for_id.items():

            self.out_for_id[key] = list([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.out_for_id[key][3] = len(value)
            for data in value:
                name = data[8]
                time_in_sec = 0
                if name not in self.out_for_id[key]:
                    self.out_for_id[key][0] = name
                if not data[5] in self.out_for_id[key]:
                    self.out_for_id[key][1] = data[5]
                if not data[7] in self.out_for_id[key]:
                    self.out_for_id[key][2] = data[7]
                if data[4] == "IN_O" or data[4] == "IN_I":
                    self.out_for_id[key][4] += 1
                    time_in_sec = self.call_time_counting(data[1], data[2])
                    self.out_for_id[key][7] += time_in_sec
                if data[4] == "OUT_O" or data[4] == "OUT_I":
                    self.out_for_id[key][5] += 1
                    time_in_sec = self.call_time_counting(data[1], data[2])
                    self.out_for_id[key][8] += time_in_sec
                cost_for_type = self.counting_cost(data[7], data[4],
                                                   time_in_sec)
                self.out_for_id[key][9] += cost_for_type
                self.out_for_id[key][6] = \
                    self.out_for_id[key][7] + self.out_for_id[key][8]
            self.out_for_id[key][9] = float("%.2f" % self.out_for_id[key][9])

    @staticmethod
    def time_call(time):
        """The function translates the time in seconds."""
        time = re.split(r'\:', time)
        time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        return time

    def call_time_counting(self, start, end):
        """The function counts the duration
        of the call of the subscriber in seconds."""
        start_time = self.time_call(start)
        end_time = self.time_call(end)
        time_call = end_time - start_time
        return time_call

    @staticmethod
    def counting_cost(tariff, call_type, time_in_sec):
        """The function calculates the total cost
        of all calls to the subscriber."""
        cost_for_type = 0
        time_in_min = math.ceil(time_in_sec/60)
        if call_type == "OUT_I":
            cost_for_type = float(DICT_TARIFFS[tariff][1])
        elif call_type == "OUT_O":
            cost_for_type = float(DICT_TARIFFS[tariff][2])
        elif call_type == "IN_I":
            cost_for_type = float(DICT_TARIFFS[tariff][3])
        elif call_type == "IN_O":
            cost_for_type = float(DICT_TARIFFS[tariff][4])
        general_cost = \
            time_in_min * float(DICT_TARIFFS[tariff][0]) + \
            time_in_min * cost_for_type
        return general_cost

    def print_in_file(self):
        """
        The function prints detailed information about
        the calls of each subscriber.
        """
        for identifier in self.out_for_id.keys():
            with open(identifier + ".txt", "w") as file_out:
                file_out.write(
                    "ФИО абонента: " + self.out_for_id[identifier][0] + "\n")
                file_out.write(
                    "Номер абонента: " + self.out_for_id[identifier][1] + "\n")
                file_out.write(
                    "Тариф абонента: " + self.out_for_id[identifier][2] + "\n")
                file_out.write("Количество звонков: " + "\n")
                file_out.write(
                    "    Всего: " + str(self.out_for_id[identifier][3]) + "\n")
                file_out.write(
                    "    Входящих: " + str(
                        self.out_for_id[identifier][4]) + "\n")
                file_out.write(
                    "    Исходящих: " + str(
                        self.out_for_id[identifier][5]) + "\n")
                file_out.write("Количество секунд разговора: " + "\n")
                file_out.write(
                    "    Всего: " + str(self.out_for_id[identifier][6]) + "\n")
                file_out.write(
                    "    Входящих: " + str(
                        self.out_for_id[identifier][7]) + "\n")
                file_out.write(
                    "    Исходящих: " + str(
                        self.out_for_id[identifier][8]) + "\n")
                file_out.write("Итого: " + str(
                    self.out_for_id[identifier][9]
                    ) + "р" + "\n")
                file_out.write("\n")
        return True

    @staticmethod
    def check_on_exception(data, identifier, line):
        """
        The function checks that all the lines
        in the log file are correct.
        Incorrect lines will be output in
        separate files for each id.
        """
        flag = False
        if "" in data or identifier == "":
            with open("error_data" + ".txt", "a") as file:
                file.write(line)
            flag = True
        return flag


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print("""
              This program calculates the payment for each
              subscriber individually with detailed
              information about calls.
              To calculate subscriber payments, enter:
              python billing.py [file.txt]
              [file.txt] - txt file with ATS logs
              """)
    else:
        pull_tariffs()
        billing = Parser()
        if not billing.data_from_file(sys.argv[1]):
            billing.handler_for_every_id()
            billing.print_in_file()


if __name__ == '__main__':
    main()
