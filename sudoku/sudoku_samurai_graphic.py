from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import *
from sudoku_samurai_file import SudokuSamurai
from sudoku_samurai_output import fill_squares
from sudoku_file import Sudoku
import sys
import os


class GameSudokuSamurai:
    """Graphical Sudoku samurai Interface"""
    def __init__(self, toplevel, game):
        """
        Creating in the transmitted window toplevel cells to fill,
        in which values from the game, buttons, frames are recorded.
        """
        toplevel.resizable(width=False, height=False)
        toplevel.geometry("+300+0")
        toplevel.title('Решатель судоку-самурай')
        self.game = game
        self.fields = list()
        for i in range(24):
            self.fields.append(Frame(toplevel))
            if i == 23:
                self.fields[i].bind('<Key>', self.check_input)
            else:
                self.fields[i].bind('<Key>', self.check_cells)
            self.fields[i].pack(ipady=0, padx=0)
        main_fonte = ('Arial', 18)
        font_of_letters = ('Arial', 10)
        self.__sudoku = list()
        for i in range(21):
            self.__sudoku += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        variable = self.fields[0]
        color = 'grey'
        for i in range(21):
            for j in range(21):
                variable = self.fields[i]
                if (i in [0, 1, 2, 3, 4, 5] and j in [9, 10, 11])\
                        or (i in [9, 10, 11] and j in [0, 1, 2, 3, 4, 5])\
                        or (i in [15, 16, 17, 18,
                                  19, 20]and j in [9, 10, 11])\
                        or (i in [9, 10,
                                  11] and j in [15, 16, 17, 18, 19, 20]):
                    self.__sudoku[i][j] = Entry(variable, width=2,
                                                font=main_fonte, bg=color,
                                                cursor='arrow', borderwidth=0,
                                                highlightcolor='white',
                                                highlightthickness=1,
                                                highlightbackground='black',
                                                textvar=self.game[i][j],
                                                state='disabled')
                else:
                    self.__sudoku[i][j] = Entry(variable, width=2,
                                                font=main_fonte, bg=color,
                                                cursor='arrow', borderwidth=0,
                                                highlightcolor='white',
                                                highlightthickness=1,
                                                highlightbackground='black',
                                                textvar=self.game[i][j],
                                                state='normal')
                self.__sudoku[i][j].bind('<KeyRelease>', self.check_cells)
                self.__sudoku[i][j].pack(side=LEFT, padx=0, pady=0)

        self.button1 = Button(self.fields[22], text='Решение',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.decide_sudoku)
        self.button1.pack(side=LEFT)
        self.button2 = Button(self.fields[22], text='Открыть',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.open_file)
        self.button2.pack(side=LEFT)
        self.button3 = Button(self.fields[22], text='Очистить всё',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.clear_all_sudoku)
        self.button3.pack(side=RIGHT)
        self.button4 = Button(self.fields[22], text='Очистить',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.clear_not_all_sudoku)
        self.button4.pack(side=RIGHT)
        self.button5 = Button(self.fields[22], text='Сохранить',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.save_sudoku)
        self.button5.pack(side=RIGHT)
        self.button6 = Button(self.fields[22], text='Проверить',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.check_solution)
        self.button6.pack(side=LEFT)
        self.button7 = Button(self.fields[23], text='Открыть последнюю сессию',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.open_last_session)
        self.button7.pack(side=LEFT)
        self._filename = "SudokuSamuraiTEMP.txt"
        self.samurai = SudokuSamurai()
        self.sudoker = Sudoku()
        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.list_squares = [(0, 9, 0, 9), (0, 9, 12, 21),
                             (12, 21, 0, 9), (12, 21, 12, 21), (6, 15, 6, 15)]
        self.cols = self.digits

    def fill_squares(self, samurai):
        """
        Function of filling Sudoku Samurai by squares
        """
        symbol = 'a'  # top left
        self.square_a = samurai.cross(samurai.rows, samurai.cols, symbol)
        symbol = 'b'  # top right
        self.square_b = samurai.cross(samurai.rows, samurai.cols, symbol)
        symbol = 'c'  # bottom left
        self.square_c = samurai.cross(samurai.rows, samurai.cols, symbol)
        symbol = 'd'  # bottom left
        self.square_d = samurai.cross(samurai.rows, samurai.cols, symbol)
        symbol = '+'
        self.square_middle = [samurai.remake_middle(x)
                              for x in samurai.cross(samurai.rows,
                                                     samurai.cols, symbol)]

    def decide_sudoku(self):
        """
        Sudoku Solution Function.
        """
        list_symbols = self.getSudoku()
        samurai_sudoku = self.sudoker.groups(list_symbols, 21)
        list_sq = self.samurai.solve(samurai_sudoku)
        if list_sq is False:
            showwarning("", "Решения нет!")
            return
        squares = fill_squares(self.samurai)
        self.write_in_file(list_sq, squares[0])
        self.write_in_file(list_sq, squares[1])
        self.write_in_file(list_sq, squares[2])
        self.write_in_file(list_sq, squares[3])
        self.write_in_file(list_sq, squares[4])
        index = 0
        for i in self.list_squares:
            self.consider_sudoku(i[0], i[1], i[2], i[3], index)
            index += 1
        with open(self._filename, 'w') as f:
            f.write('')
        self.check_cells(event="Button-1")

    def write_in_file(self, solution, sqr):
        """
        Function of recording sudoku in a file.
        """
        with open(self._filename, "a") as f:
            for r in self.rows:
                for c in self.cols:
                    x = str(solution[sqr[(ord(r) - 65) * 9 + int(c) - 1]])
                    f.write(x + " ")
            f.write('\n')

    def getSudoku(self):
        """
        The function to get the values entered in the cells of the window.
        """
        sudoku = list()
        for i in range(21):
            for j in range(21):
                sudoku.append(self.game[i][j].get())
        for k in range(441):
            if sudoku[k] == '':
                sudoku[k] = '.'
        return sudoku

    def clear_not_all_sudoku(self):
        """
        The function clears only the unfrozen cells in the window.
        """
        for i in self.list_squares:
            self.clear(i[0], i[1], i[2], i[3])
        self.check_cells(event="Button-1")

    def clear(self, m, n, k, l):
        """
        The function clears only the unfrozen cells in the window.
        """
        for i in range(m, n):
            for j in range(k, l):
                if self.__sudoku[i][j]['state'] == 'normal':
                    self.game[i][j].set('')

    def clear_all_sudoku(self):
        """
        The function clears all cells in the window.
        """
        for i in self.list_squares:
            self.clear_sudoku(i[0], i[1], i[2], i[3])
        self.check_cells(event="Button-1")

    def clear_sudoku(self, m, n, k, l):
        """
        The function clears all cells in the window.
        """
        for i in range(m, n):
            for j in range(k, l):
                self.game[i][j].set('')
                self.__sudoku[i][j]['state'] = 'normal'

    def save_in_file(self, f):
        """
        Function of saving sudoku to a file
        """
        for i in range(21):
            for j in range(21):
                if self.__sudoku[i][j]['state'] == 'disabled':
                    if i in [0, 1, 2, 3, 4, 5] and j in [9, 10, 11]:
                        f.write('.!')
                    elif i in [9, 10, 11] and j in [0, 1, 2, 3, 4, 5]:
                        f.write('.!')
                    elif i in [15, 16, 17, 18, 19, 20] and j in [9, 10, 11]:
                        f.write('.!')
                    elif i in [9, 10, 11] and j in [15, 16, 17, 18, 19, 20]:
                        f.write('.!')
                    elif self.game[i][j].get() == "":
                        f.write('0!')
                    else:
                        f.write(self.game[i][j].get() + '!')
                else:
                    if i in [0, 1, 2, 3, 4, 5] and j in [9, 10, 11]:
                        f.write('.?')
                    elif i in [9, 10, 11] and j in [0, 1, 2, 3, 4, 5]:
                        f.write('.?')
                    elif i in [15, 16, 17, 18, 19, 20] and j in [9, 10, 11]:
                        f.write('.?')
                    elif i in [9, 10, 11] and j in [15, 16, 17, 18, 19, 20]:
                        f.write('.?')
                    elif self.game[i][j].get() == "":
                        f.write('0?')
                    else:
                        f.write(self.game[i][j].get() + '?')

    def save_sudoku(self):
        """
        The function of saving sudoku in the selected file.
        """
        f = asksaveasfile()
        if f is None:
            return
        self.save_in_file(f)

    def save_after_clicking(self):
        """
         The function of saving each performed step
         """
        if os.path.exists('save2.txt'):
            with open('save1.txt', 'w') as file:
                self.save_in_file(file)
            os.remove('save2.txt')
        else:
            with open('save2.txt', 'w') as file:
                self.save_in_file(file)
            os.remove('save1.txt')

    def check_input(self):
        """
        The function of checking the correct entry of values into the
        cells of the window.
        """
        digit = '123456789'
        for i in range(21):
            for j in range(21):
                var = self.game[i][j].get()
                if len(var) > 1 or var not in digit:
                    self.game[i][j].set('')

    def check_cells(self, event):
        """
        Check cell function and save the value
        """
        self.check_input()
        self.save_after_clicking()

    def open_last(self, file):
        with open(file) as file:
            list_symbols = file.read()
            for i in self.list_squares:
                self.clear_sudoku(i[0], i[1], i[2], i[3])
            try:
                self.open1(list_symbols)
            except SyntaxError:
                self.open2(list_symbols)
        self.check_cells(event="Button-1")

    def open_last_session(self):
        """
        Function of opening the last session
        """
        if os.path.exists('save1.txt'):
            self.open_last('save1.txt')
        else:
            self.open_last('save2.txt')

    def open_file(self):
        """
        The main function of opening a file
        """
        file = askopenfile()
        if file is None:
            return
        list_symbols = file.read()
        self.clear_all_sudoku()
        try:
            self.open1(list_symbols)
        except SyntaxError:
            self.open2(list_symbols)
        self.check_cells(event="Button-1")

    def open2(self, list_symbols):
        """
        The function of reading Sudoku from 81 characters from
        the selected file inserting the values into the corresponding
        cells, specifying whether they are frozen or not.
        """
        list_symbols = list(''.join(list_symbols))
        digit = '123456789'
        if not len(list_symbols) == 882 or not all([j in '?!.0123456789'
                                                    for j in list_symbols]):
            showwarning("", "Содержимое файла некорректно")
        else:
            for i in range(21):
                for j in range(21):
                    x = (list_symbols[0] == '.' or list_symbols[0] == '0')
                    if x and list_symbols[1] == '!':
                        self.game[i][j].set('')
                        self.__sudoku[i][j]['state'] = 'disabled'
                    elif x and list_symbols[1] == '?':
                        self.game[i][j].set('')
                        self.__sudoku[i][j]['state'] = 'normal'
                    elif list_symbols[0] in digit and list_symbols[1] == '!':
                        self.game[i][j].set(list_symbols[0])
                        self.__sudoku[i][j]['state'] = 'disabled'
                    else:
                        self.game[i][j].set(list_symbols[0])
                        self.__sudoku[i][j]['state'] = 'normal'
                    list_symbols.pop(0)
                    list_symbols.pop(0)

    def open1(self, list_symbols):
        """
        The function of reading sudoku from the selected file and
        inserting the values into corresponding cells.
        """
        list_symbols = list(''.join(list_symbols))
        if not len(list_symbols) == 441 or not all([j in '.0123456789'
                                                    for j in list_symbols]):
            raise SyntaxError
        else:
            samurai_sudoku = self.sudoker.groups(list_symbols, 21)
            list_square = self.samurai.divide_sudoku(samurai_sudoku)
            index = 0
            for i in self.list_squares:
                self.fill_sudoku(list_square[index], i[0], i[1], i[2], i[3])
                index += 1

    def get_values_in_square(self, values, sqr):
        """
        The function of obtaining values from one Sudoku
        """
        return (''.join(values[sqr[(ord(r) - 65) * 9 + int(c) - 1]]
                for r in self.rows for c in self.cols))

    def check_solution(self):
        """
        The function of verifying the correctness of the Sudoku decision.
        """
        list_symbols = self.getSudoku()
        samurai_sudoku = self.sudoker.groups(list_symbols, 21)
        list_squares = self.samurai.divide_sudoku(samurai_sudoku)
        samurai_list = list()
        for i in range(5):
            samurai_list.append(self.sudoker.groups(list_squares[i], 9))
        result = list()
        for sudoku in samurai_list:
            if self.sudoker.check_solution(sudoku) is True:
                result.append('+')
        if result.count('+') == 5:
            showinfo("", "Судоку верно разгадано!")
        else:
            showwarning("", "Решение неверно!")

    def fill_sudoku(self, list_symbols, m, k, l, n):
        """
        Function of filling cells with values
        """
        for i in range(m, k):
            for j in range(l, n):
                if list_symbols[0] == '.' or list_symbols[0] == '0':
                    self.game[i][j].set('')
                else:
                    self.game[i][j].set(list_symbols[0])
                    self.__sudoku[i][j]['state'] = 'disabled'
                list_symbols.pop(0)

    def consider_sudoku(self, m, n, k, l, count):
        """
        Function of reading sudoku from a file.
        """
        with open(self._filename, 'r') as file:
            symbols = file.read()
            symbols = symbols.split('\n')[count]
            symbols = symbols.split(' ')
            for i in range(m, n):
                for j in range(k, l):
                    if symbols[0] == '0' or symbols[0] == '.':
                        self.game[i][j].set('')
                    else:
                        self.game[i][j].set(symbols[0])
                    symbols.pop(0)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "help":
            print("""
                This program is a graphical version
                of the Sudoku Samurai solve.
                In this program, the Sudoku_Samurai module is imported from the
                sudoku_samurai_file.py file, through which a recursive Sudoku
                solution is implemented. To start the program, you need to
                enter the following data in the command line:
                python sudoku_samurai_graphic.py""")
    else:
        root = Tk()
        fields = []
        for i in range(21):
            fields += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(21):
            for j in range(21):
                fields[i][j] = StringVar(root)
        GameSudokuSamurai(root, fields)
        root.mainloop()


if __name__ == "__main__":
    main()
