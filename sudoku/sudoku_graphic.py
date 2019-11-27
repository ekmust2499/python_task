from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import *
from sudoku_file import Sudoku
import sys
import os


class GameSudoku:
    """Graphical Sudoku Interface"""
    def __init__(self, toplevel, game):
        """
        Creating in the transmitted window toplevel cells to fill,
        in which values from the game, buttons, frames are recorded.
        """
        toplevel.resizable(width=False, height=False)
        toplevel.geometry("+450+100")
        toplevel.title('Решатель судоку')
        self.game = game
        font_of_letters = ('Arial', 10)
        self.fields = list()
        for i in range(11):
            self.fields.append(Frame(toplevel))
            if i == 10:
                self.fields[i].bind('<Key>', self.check_input)
            else:
                self.fields[i].bind('<Key>', self.check_cells)
            self.fields[i].pack(ipady=0, padx=0)
        self.__sudoku = list()
        for i in range(1, 10):
            self.__sudoku += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(9):
            for j in range(9):
                variable = self.fields[i]
                if j in [3, 4, 5] and i in [0, 1, 2, 6, 7, 8]\
                        or j in [0, 1, 2, 6, 7, 8] and i in [3, 4, 5]:
                    color = 'beige'
                else:
                    color = 'grey'
                self.__sudoku[i][j] = Entry(variable, width=2,
                                            font=('Arial', 18), bg=color,
                                            cursor='arrow', borderwidth=0,
                                            highlightcolor='white',
                                            highlightthickness=1,
                                            highlightbackground='black',
                                            textvar=self.game[i][j],
                                            state='normal')
                self.__sudoku[i][j].bind('<KeyRelease>', self.check_cells)
                self.__sudoku[i][j].pack(side=LEFT, padx=0, pady=0)

        self.button1 = Button(self.fields[9], text='Решение',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.decide_sudoku)
        self.button1.pack(side=LEFT)
        self.button2 = Button(self.fields[9], text='Открыть',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.open_file)
        self.button2.pack(side=LEFT)
        self.button3 = Button(self.fields[10], text='Очистить всё',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.clear_all_sudoku)
        self.button3.pack(side=RIGHT)
        self.button4 = Button(self.fields[10], text='Очистить',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.clear_sudoku)
        self.button4.pack(side=RIGHT)
        self.button5 = Button(self.fields[9], text='Сохранить',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.save_sudoku)
        self.button5.pack(side=RIGHT)
        self.button6 = Button(self.fields[9], text='Проверить',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.check_solution)
        self.button6.pack(side=LEFT)
        self.button7 = Button(self.fields[10], text='Открыть последнюю сессию',
                              bg='grey', fg='white',
                              font=font_of_letters,
                              command=self.open_last_session)
        self.button7.pack(side=LEFT)
        self._filename = "SudokuTEMP.txt"
        self.sudoker = Sudoku()

    def check_solution(self):
        """
        The function of verifying the correctness of the Sudoku decision.
        """
        list_symbols = self.getSudoku()
        sudoku = self.sudoker.groups(list_symbols, 9)
        if self.sudoker.check_solution(sudoku) is True:
            showinfo("", "Судоку верно разгадано!")
        else:
            showwarning("", "Решение неверно!")

    def decide_sudoku(self):
        """
        Sudoku Solution Function.
        """
        list_symbols = self.getSudoku()
        sudoku = self.sudoker.groups(list_symbols, 9)
        if self.sudoker.check_input_sudoku(sudoku) is False:
            showwarning("", "Решения нет!")
        else:
            solution = self.sudoker.solve(sudoku)
            if solution is False:
                showwarning("", "Решения нет!")
            elif self.sudoker.check_solution(solution) is True:
                for i in range(0, 9):
                    for j in range(0, 9):
                        self.game[i][j].set(str(solution[i][j]))
        self.check_cells(5)

    def getSudoku(self):
        """
        The function to get the values entered in the cells of the window.
        """
        sudoku = list()
        for i in range(9):
            for j in range(9):
                sudoku.append(self.game[i][j].get())
        for k in range(81):
            if sudoku[k] == '':
                sudoku[k] = '.'
        return sudoku

    def clear_sudoku(self):
        """
        The function clears only the unfrozen cells in the window.
        """
        for i in range(9):
            for j in range(9):
                if self.__sudoku[i][j]['state'] == 'normal':
                    self.game[i][j].set('')
        self.check_cells(5)

    def clear_all_sudoku(self):
        """
        The function clears all cells in the window.
        """
        for i in range(9):
            for j in range(9):
                self.game[i][j].set('')
                self.__sudoku[i][j]['state'] = 'normal'
        self.check_cells(5)

    def save_in_file(self, f):
        """
        Function of saving sudoku to a file
        """
        for i in range(9):
            for j in range(9):
                if self.__sudoku[i][j]['state'] == 'disabled':
                    if self.game[i][j].get() == "":
                        f.write('.!')
                    else:
                        f.write(self.game[i][j].get() + '!')
                else:
                    if self.game[i][j].get() == "":
                        f.write('.?')
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

    def check_cells(self, x):
        """
        Check cell function and save the value
        """
        self.check_input()
        self.save_after_clicking()

    def check_input(self):
        """
        The function of checking the correct entry of values into the
        cells of the window.
        """
        digit = '123456789'
        for i in range(9):
            for j in range(9):
                var = self.game[i][j].get()
                if len(var) > 1 or var not in digit:
                    self.game[i][j].set('')

    def open_last(self, file):
        with open(file) as file:
            list_symbols = file.read()
            for i in range(9):
                for j in range(9):
                    self.game[i][j].set('')
                    self.__sudoku[i][j]['state'] = 'normal'
            try:
                self.open1(list_symbols)
            except SyntaxError:
                self.open2(list_symbols)
        self.check_cells(5)

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
        self.check_cells(5)

    def open2(self, list_symbols):
        """
        The function of reading Sudoku from 81 characters from
        the selected file inserting the values into the corresponding
        cells, specifying whether they are frozen or not.
        """
        list_symbols = list(''.join(list_symbols))
        digit = '123456789'
        allowable_symbols = all([j in digit + "?!." for j in list_symbols])
        if not len(list_symbols) == 162 or not allowable_symbols:
            showwarning("", "Содержимое файла некорректно")
        else:
            for i in range(0, 9):
                for j in range(0, 9):
                    if list_symbols[0] == '.' or list_symbols[0] == '0':
                        self.game[i][j].set('')
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
        The function of reading Sudoku from 81 characters from
        the selected file inserting the values into the corresponding cells.
        """
        list_symbols = list(''.join(list_symbols))
        digit_and_dot = '.123456789'
        allowable_symbols = all([j in digit_and_dot for j in list_symbols])
        if not len(list_symbols) == 81 or not allowable_symbols:
            raise SyntaxError
        else:
            for i in range(9):
                for j in range(9):
                    if list_symbols[0] == '.' or list_symbols[0] == '0':
                        self.game[i][j].set('')
                    else:
                        self.game[i][j].set(list_symbols[0])
                        self.__sudoku[i][j]['state'] = 'disabled'
                    list_symbols.pop(0)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "help":
            print(
                """
                This program is a graphical version of the Sudoku solver
                In this program, the Sudoku module is imported from the
                sudoku_file.py file, through which a recursive Sudoku
                solution is implemented. To start the program, you need
                to enter the following data in the command line:
                python sudoku_graphic.py
                """)
    else:
        root = Tk()
        fields = []
        for i in range(1, 10):
            fields += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(9):
            for j in range(9):
                fields[i][j] = StringVar(root)
        GameSudoku(root, fields)
        root.mainloop()


if __name__ == "__main__":
    main()
