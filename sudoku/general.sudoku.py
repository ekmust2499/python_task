from tkinter import *
from sudoku_graphic import GameSudoku
from sudoku_samurai_graphic import GameSudokuSamurai
from PIL import ImageTk, Image


class MainSudoku(Frame):
    def __init__(self, root, *args):
        super().__init__(root, *args)
        self.root = root
        self.image = Image.open("sudoku.png")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self.resize_image)
        self.field = Frame(self.background)
        self.field.bind('<Motion>')
        self.field.pack(ipady=1, padx=1, side=BOTTOM)
        self.but1 = Button(self.field,
                           text="Судоку",
                           command=self.but_1_callback,
                           bg='yellow',
                           fg='black',
                           width=15,
                           height=2)
        self.but2 = Button(self.field,
                           text="Судоку-самурай",
                           command=self.but_2_callback,
                           bg='yellow',
                           fg='black',
                           width=15,
                           height=2)
        self.but1.pack(side=LEFT)
        self.but2.pack(side=RIGHT)

    def resize_image(self, event):
        self.image = self.img_copy.resize((event.width, event.height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

    def but_1_callback(self):
        self.root.destroy()
        sudoku()

    def but_2_callback(self):
        self.root.destroy()
        sudoku_samurai()


def main_sudoku():
    root = Tk()
    root.geometry('800x600+250+0')
    root.title('Игра "Судоку"')
    root.resizable(width=False, height=False)
    game = MainSudoku(root)
    game.pack(fill=BOTH, expand=YES)
    root.mainloop()


def sudoku():
    def but_callback():
        root.destroy()
        main_sudoku()
    root = Tk()
    root.wm_geometry("+%d+%d" % (500, 200))
    game = []
    for i in range(1, 10):
        game += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(9):
        for j in range(9):
            game[i][j] = StringVar(root)
    GameSudoku(root, game)
    but1 = Button(root, text="-> На главную страницу",
                  command=but_callback, bg='grey', fg='white')
    but1.pack()
    root.mainloop()


def sudoku_samurai():
    def but_callback():
        root.destroy()
        main_sudoku()
    root = Tk()
    root.wm_geometry("+%d+%d" % (300, 0))
    game = []
    for i in range(21):
        game += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(21):
        for j in range(21):
            game[i][j] = StringVar(root)
    GameSudokuSamurai(root, game)
    but1 = Button(root, text="-> На главную страницу",
                  command=but_callback, bg='grey', fg='white')
    but1.pack()
    root.mainloop()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "help":
            print(
                """
                This program is a graphical version
                of the Sudoku solve and Sudoku Samurai solve.
                In this program, the Sudoku module is imported from the
                sudoku_file.py file and the Sudoku_Samurai
                module is imported from the sudoku_samurai_file.py file,
                through which a recursive Sudoku solution is implemented.
                To start the program, you need to enter the following data
                in the command line:
                python general_sudoku.py
                """)
    else:
        main_sudoku()


if __name__ == '__main__':
    main()
