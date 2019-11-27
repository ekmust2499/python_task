import sys


class Sudoku:
    """Sudoku"""
    def read_from_file(self, file: str) -> list:
        """
        The function of reading sudoku from the transferred file.
        """
        list_symbols = list()
        digit_and_dot = '.123456789'
        with open(file) as file_with_sudoku:
            sudoku = file_with_sudoku.read()
            for symbol in str(sudoku):
                if symbol in digit_and_dot:
                    list_symbols.append(symbol)
        matrix = self.groups(list_symbols, 9)
        return matrix

    def output(self, numbers: list) -> None:
        """
        Function of output sudoku in the form of a square 9 * 9.
        """
        for row in range(9):
            print(''.join(numbers[row][column].center(2)
                          for column in range(9)))
        print()

    def groups(self, numbers: list, n: int) -> list:
        """
        The function groups the values of the numbers in the list,
        consisting of lists of n elements.
        """
        matrix = list()
        previous_row = -1
        for i in range(len(numbers)):
            if i // n > previous_row:
                previous_row += 1
                matrix.append(list())
            matrix[i // n].append(numbers[i])
        return matrix

    def num_in_row_where_pos(self, numbers: list, position: tuple) \
            -> list:
        """
        The function of finding all values for line number in a position.
        """
        return numbers[position[0]]

    def num_in_column_where_pos(self, numbers: list, position: tuple) \
            -> list:
        """
        The function of finding all values for the column number in a position.
        """
        column = list()
        for i in range(9):
            column.append(numbers[i][position[1]])
        return column

    def num_in_square_where_pos(self, numbers: list, position: tuple) \
            -> list:
        """
        The function of finding all values from the square 3 * 3 with position.
        """
        block = list()
        one = (position[0] // 3) * 3
        two = (position[1] // 3) * 3
        for i in range(3):
            for j in range(3):
                block.append(numbers[one + i][two + j])
        return block

    def find_empty_positions(self, matrix: list) -> (tuple, bool):
        """
        The function of finding the first free position in Sudoku
        in the form of a point.
        """
        position = (-1, -1)
        for row in range(0, len(matrix)):
            for column in range(0, len(matrix[row])):
                if matrix[row][column] == '.':
                    return (row, column)
        if position == (-1, -1):
            return False

    def find_possible_values(self, matrix: list, position: tuple) \
            -> list:
        """
        The search function of all possible values that can be set
        in position.
        """
        numbers = list()
        digit = '123456789'
        for x in digit:
            numbers.append(x)
        num_in_row = self.num_in_row_where_pos(matrix, position)
        num_in_column = self.num_in_column_where_pos(matrix, position)
        num_in_block = self.num_in_square_where_pos(matrix, position)
        numbers = self.remove_in_list(numbers, num_in_row)
        numbers = self.remove_in_list(numbers, num_in_column)
        numbers = self.remove_in_list(numbers, num_in_block)
        return numbers

    def remove_in_list(self, numbers: list, num_in: list) -> list:
        """
        The function of checking whether a number belongs to both lists.
        If it is contained in both lists, then we delete it from the first.
        """
        for k in num_in:
            for m in numbers:
                if k == m:
                    numbers.remove(k)
        return numbers

    def solve(self, matrix: list) -> (list, bool):
        """
        Sudoku Solution Function.
        """
        position = self.find_empty_positions(matrix)
        if position is False:
            return matrix
        row, column = position
        poss_values = self.find_possible_values(matrix, position)
        for i in poss_values:
            matrix[row][column] = i
            if self.solve(matrix) is not False:
                return matrix
            matrix[row][column] = '.'
        return False

    def check_solution(self, decision: list) -> bool:
        """
        The function of verifying the correctness of Sudoku decisions.
        If the solution is true, it returns True, otherwise False.
        """
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = self.num_in_square_where_pos(decision, (i, j))
                if not self.check(block):
                    return False

        for i in range(9):
            row = self.num_in_row_where_pos(decision, (i, 0))
            column = self.num_in_column_where_pos(decision, (0, i))
            if not self.check(row) and not self.check(column):
                return False

        return True

    def check(self, list_check: list) -> bool:
        """
        The function of checking whether there are all the digits
        from 1 to 9 in the transferred list.
        """
        return all(i in list_check for i in '123456789')

    def check_input_sudoku(self, sudoku: list) -> bool:
        """
        The function of checking the correctness of the input sudoku.
        """
        list_numbers = list()
        if not len(sudoku) == 9:
            return False
        for i in range(len(sudoku)):
            if not len(sudoku[i]) == 9:
                return False
        for i in range(len(sudoku)):
            for k in sudoku[i]:
                list_numbers.append(k)
        for i in range(9):
            row = self.num_in_row_where_pos(sudoku, (i, 0))
            column = self.num_in_column_where_pos(sudoku, (0, i))
            for j in range(1, 10):
                var = '{0}'.format(j)
                if row.count(var) > 1 or column.count(var) > 1:
                    return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = self.num_in_square_where_pos(sudoku, (i, j))
                for k in range(1, 10):
                    if block.count('{0}'.format(k)) > 1:
                        return False
        return True


def solver_sudoku():
    obj_sudoku = Sudoku()
    if len(sys.argv[1]) == 81:
        list_symbols = list()
        digit_and_dop = '.123456789'
        for symbol in str(sys.argv[1]):
            if symbol in digit_and_dop:
                list_symbols.append(symbol)
        sudoku = obj_sudoku.groups(list_symbols, 9)
    else:
        sudoku = obj_sudoku.read_from_file(sys.argv[1])
    if obj_sudoku.check_input_sudoku(sudoku) is False:
        print("Sudoku doesn't have a solution")
        return
    solution = obj_sudoku.solve(sudoku)
    if obj_sudoku.check_solution(solution) is True:
        obj_sudoku.output(solution)


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print("""
            This is the program - the console version of the sudoku solver.
            The program is implemented using the Sudoku class,
            which can be imported as a module. The solution is recursive.
            To start, type: python sudoku_file.py [file/line]
            file - path to txt file, with Sudoku from 81 symbols in 1 line
            line - Sudoku, recorded in one line of 81 characters""")
    else:
        try:
            solver_sudoku()
        except (FileNotFoundError, IOError) as exception:
            print(exception)


if __name__ == '__main__':
    main()
