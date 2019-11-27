"""
Throughout this program we have:
r is a row,    e.g. 'A'
c is a column, e.g. '3'
s is a square, e.g. 'A3'
d is a digit,  e.g. '9'
u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
"""
from sudoku_file import Sudoku
from sudoku_samurai_output import output
import sys


class SudokuSamurai:
    def __init__(self):
        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.cols = self.digits
        self.list_unitlist = list()
        self.list_sudoku = list()
        word = 'abcd'
        for i in range(4):
            symbol = word[i]
            x = ([self.cross(self.rows, c, symbol)
                 for c in self.cols] +
                 [self.cross(r, self.cols, symbol)
                 for r in self.rows] +
                 [self.cross(rs, cs, symbol)
                 for rs in ('ABC', 'DEF', 'GHI')
                 for cs in ('123', '456', '789')])
            y = self.cross(self.rows, self.cols, symbol)
            self.list_unitlist.append(x)
            self.list_sudoku.append(y)

        self.sudoku_a = self.list_sudoku[0]
        self.unitlist_a = self.list_unitlist[0]
        self.sudoku_b = self.list_sudoku[1]
        self.unitlist_b = self.list_unitlist[1]
        self.sudoku_c = self.list_sudoku[2]
        self.unitlist_c = self.list_unitlist[2]
        self.sudoku_d = self.list_sudoku[3]
        self.unitlist_d = self.list_unitlist[3]
        symbol = '+'
        self.sudoku_middle = [self.remake_middle(x)
                              for x in
                              self.cross(self.rows, self.cols, symbol)]
        self.unitlist_mid = ([self.sudoku_middle[x * 9:x * 9 + 9]
                             for x in range(9)] +
                             [self.sudoku_middle[x::9]
                             for x in range(9)] +
                             [self.cross(rs, cs, symbol)
                             for rs in ('ABC', 'DEF', 'GHI')
                             for cs in ('123', '456', '789')
                             if not (rs in 'ABCGHI' and cs in '123789')])
        self.all_sudoku = set(self.sudoku_a + self.sudoku_b +
                              self.sudoku_c + self.sudoku_d +
                              self.sudoku_middle)
        self.all_unitlists = (self.unitlist_a + self.unitlist_b +
                              self.unitlist_c + self.unitlist_d +
                              self.unitlist_mid)

        self.units = dict((s, [u for u in self.all_unitlists if s in u])
                          for s in self.all_sudoku)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s]))
                          for s in self.all_sudoku)
        self.sudoker = Sudoku()

    def remake_middle(self, c: str) -> str:
        """
        Renames elements in the middle squares of the middle Sudoku
        to the elements of angular Sudoku
        """
        a = b = 0
        s = ""
        if c[0] in 'ABCGHI' and c[1] in '123789':
            if c[0] in 'ABC':
                s += chr(ord(c[0]) + 6)
                a = 1
            elif c[0] in 'GHI':
                s += chr(ord(c[0]) - 6)
                a = 2
            if c[1] in '123':
                s += chr(ord(c[1]) + 6)
                b = 1
            elif c[1] in '789':
                s += chr(ord(c[1]) - 6)
                b = 2
        else:
            return c
        if a == 1 and b == 1:
            s += 'a'
        elif a == 1 and b == 2:
            s += 'b'
        elif a == 2 and b == 1:
            s += 'c'
        elif a == 2 and b == 2:
            s += 'd'
        return s

    def cross(self, rows: str, columns: str, symbol='') -> list:
        """
        Returns all elements in which a string, column,
        and symbol can be simultaneously
        """
        return [row + column + symbol for row in rows for column in columns]

    def parse_grid_samurai(self, sudoku: list) -> (dict, False):
        """
        Convert grid to a dict of possible values, {square: digits}, or
        return False if a contradiction is detected.
        """
        cells = dict((s, self.digits) for s in self.all_sudoku)
        for key, value in self.grid_values(sudoku).items():
            if value in self.digits and not \
                    self.find_possible_value(cells, key, value):
                return False
        return cells

    def find_possible_value(self, cells: dict, key: str,
                            value: str) -> (dict, False):
        """
        Eliminate all the other values (except d) from values[s] and propagate.
        """
        other_values = cells[key].replace(value, '')
        if all(self.remove_invalid_values(cells, key, val)
               for val in other_values):
            return cells

    def remove_invalid_values(self, cells: dict, key: str,
                              value: str) -> (dict, False):
        """
        Eliminate d from values[s]; propagate when values or places <= 2.
        Return values, except return False if a contradiction is detected.
        """

        if value not in cells[key]:
            # Already eliminated
            return cells
        cells[key] = cells[key].replace(value, '')
        # (1) If a square s is reduced to one value d2,
        # then eliminate d2 from the peers.
        if len(cells[key]) == 1:
            if not all(self.remove_invalid_values(cells, s2, cells[key])
                       for s2 in self.peers[key]):
                return False
        for u in self.units[key]:
            dplaces = [s for s in u if value in cells[s]]
            if len(dplaces) == 1:
                if not self.find_possible_value(cells, dplaces[0], value):
                    return False
        return cells

    def display_samurai(self, cells: dict) -> None:
        """
        Prints samurai sudoku on the console
        """
        output(cells, self.sudoku_a, self.sudoku_b,
               self.sudoku_c, self.sudoku_d, self.sudoku_middle)

    def generate_sudoku(self, values: dict, sqr: list) -> list:
        """
        Return a sudoku with the given values and square
        Return the sudoku in a 2D grid format
        """
        sudoku = [[None]*9]*9
        i = 0
        for r in self.rows:
            sudoku[i] = [str(values[sqr[(ord(r) - 65) * 9 + int(c) - 1]])
                         for c in self.cols]
            i += 1
            if i == 9:
                i = 0
        return sudoku

    def check_solution(self, cells: dict, sqrs: list) -> (True, False):
        """
        Checking Sudoku Solution
        """
        samurai = []
        for sqr in sqrs:
            samurai.append(self.generate_sudoku(cells, sqr))
        result = list()
        for sudoku in samurai:
            if self.sudoker.check_solution(sudoku) is True:
                result.append('+')
        if result.count('+') == 5:
            return True
        else:
            return False

    def solve(self, sudoku: list) -> dict:
        """
        Sudoku samurai decision function
        """
        return self.search(self.parse_grid_samurai(sudoku))

    def search(self, values: dict) -> (dict, False):
        """
        A function that uses the depth and spread search,
        try all possible values.
        """
        if all(len(values[s]) == 1 for s in self.all_sudoku):
            return values
        n, s = min((len(values[s]), s)
                   for s in self.all_sudoku if len(values[s]) > 1)
        return self.some(self.search(self.find_possible_value(
                         values.copy(), s, d)) for d in values[s])

    def some(self, seq) -> dict:
        """
        Return some element of seq that is true.
        """
        for e in seq:
            if e is not None:
                return e

    def read_from_file(self, file: str, count: int) -> list:
        """
        The function of reading sudoku from the transferred file.
        """
        list_symbols = list()
        with open(file) as file_with_sudoku:
            sudoku = file_with_sudoku.read()
            for symbol in str(sudoku):
                if symbol in '.0123456789':
                    list_symbols.append(symbol)
        matrix = self.sudoker.groups(list_symbols, count)
        return matrix

    def get_values_in_one_sudoku(self, arr: list) -> list:
        """
        The function of obtaining all the values of one of the 5 Sudoku
        """
        return [x for sub in arr for x in sub]

    def divide_sudoku(self, sudoku: list) -> list:
        """
        Function of dividing Sudoku-samurai for 5 Sudoku
        """
        list_sudoku = list()
        left_top = self.get_values_in_one_sudoku([x[:9] for x in sudoku[:9]])
        right_top = self.get_values_in_one_sudoku([x[12:] for x in sudoku[:9]])
        left_bottom = self.get_values_in_one_sudoku([x[:9]
                                                    for x in sudoku[12:]])
        right_bottom = self.get_values_in_one_sudoku([x[12:]
                                                     for x in sudoku[12:]])
        middle = self.get_values_in_one_sudoku([x[6:15] for x in sudoku[6:15]])

        list_sudoku.append(left_top)
        list_sudoku.append(right_top)
        list_sudoku.append(left_bottom)
        list_sudoku.append(right_bottom)
        list_sudoku.append(middle)
        return list_sudoku

    def grid_values(self, sudoku: list) -> dict:
        """
        Function of obtaining a grid of values
        """
        sudoku = self.divide_sudoku(sudoku)
        chars = sudoku[0] + sudoku[1] + sudoku[2] + sudoku[3] + sudoku[4]
        sqrs = (self.sudoku_a + self.sudoku_b +
                self.sudoku_c + self.sudoku_d + self.sudoku_middle)
        assert len(chars) == 405
        return dict(zip(sqrs, chars))


def solver_sudoku():
    samurai = SudokuSamurai()
    sudoker = Sudoku()
    if len(sys.argv[1]) == 441:
        list_symbols = list()
        for symbol in str(sys.argv[1]):
            if symbol in '.0123456789':
                list_symbols.append(symbol)
        samurai_sudoku = sudoker.groups(list_symbols, 21)
    else:
        samurai_sudoku = samurai.read_from_file(sys.argv[1], 21)
    sudoku_split = samurai.divide_sudoku(samurai_sudoku)
    for sud in sudoku_split:
        if sudoker.check_input_sudoku(sudoker.groups(sud, 9)) is False:
            print("Sudoku doesn't have a solution")
            return
    list_square = samurai.solve(samurai_sudoku)
    if samurai.check_solution(list_square,
                              [samurai.sudoku_a, samurai.sudoku_b,
                               samurai.sudoku_c, samurai.sudoku_d,
                               samurai.sudoku_middle]) is True:
        samurai.display_samurai(list_square)


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print("""
        This is a console version of Sudoku samurai solver.
        The program is implemented in the class of Sudoku_Samurai,
        which can be is imported as a module. The solution is recursive.
        To start, type: python sudoku_samurai_file.py [file/line]
        file -path to txt file, with Sudoku from 441 symbols in 1 line
        line - Sudoku-samurai, recorded in one line of 441 characters.""")
    else:
        try:
            solver_sudoku()
        except (FileNotFoundError, IOError) as exception:
            print(exception)


if __name__ == '__main__':
    main()
