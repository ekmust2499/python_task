from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from encode import encoding, write_in_file
from decode import decoding
import math


class Graphic_BMP(Frame):
    def __init__(self, root=None):
        self.file_name = ''
        self.file = ''
        Frame.__init__(self, root)
        self.root = root
        self.root.title("Стеганография BMP")
        self.pack()
        self.create_widgets()
        self.left_img = None
        self.left_photo = None
        self.right_img = None
        self.right_photo = None

    def open_file(self):
        """
        Function of opening a file and outputting it to the left field
        """
        self.file_name = askopenfilename(filetypes=[('BMP File', '*.bmp')])
        if self.file_name == "":
            return

        if self.msg_box.get('1.0', END) != '':
            self.msg_box.delete('1.0', END)

        self.left_img = Image.open(self.file_name)
        w, h = self.left_img.size

        scale_w = 600 / w
        scale_h = 400 / h
        scale = min(scale_w, scale_h)
        new_w = math.ceil(scale * w)
        new_h = math.ceil(scale * h)
        self.left_img = self.left_img.resize((new_w, new_h), Image.NEAREST)

        self.left_photo = ImageTk.PhotoImage(self.left_img)

        self.left_img_canvas.create_image(600 / 2, 400 / 2, anchor=CENTER,
                                          image=self.left_photo)

    def decod(self):
        """
        The function of decoding a message from a file and outputting
        the result to a text field
        """
        if self.file_name == '':
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Откройте файл формата BMP!')
            return 0
        file = self.msg_box.get('1.0', END).replace("\n", "")
        if file == "":
            self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Введите названиe файла '
                                     'для сохранения сообщения!')
        else:
            decry_msg = decoding(self.file_name)
            if decry_msg is False:
                self.msg_box.delete('1.0', END)
                self.msg_box.insert(END, "В этом файле ничего не зашифровано!")
                return
            try:
                file_result = '{0}.txt'.format(file)
                write_in_file(file_result, decry_msg)
                with open(file_result, 'r') as result:
                    result = result.read()
                    self.msg_box.delete('1.0', END)
                    self.msg_box.insert(END, 'Закодированное сообщение: ' +
                                        "\n" + '"' + result + '".')
            except FileNotFoundError:
                self.msg_box.delete('1.0', END)
                self.msg_box.insert(END, 'Неверный ввод данных!')
                return

    def encod(self):
        """
        The function of encrypting a message in a file and outputting
        the result to the right field
        """
        text = self.msg_box.get('1.0', END).replace("\n", "").split(" ")

        hide_msg = text[0]

        if self.file_name == '':
            if hide_msg == '':
                self.msg_box.delete('1.0', END)
            self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Откройте файл формата BMP!')
            return
        elif hide_msg == '':
            self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Введите путь до файла '
                                'с сообщением для зашифровки и '
                                'название bmp-изображения!')
            return
        else:
            if not len(text) == 2:
                self.msg_box.delete('1.0', END)
                self.msg_box.insert(END, 'Вы некорректно ввели данные!')
                return
            origin_file_name = self.file_name
            self.file = '{0}.bmp'.format(text[1])
            dest = self.scale.get()
            try:
                with open(hide_msg, 'rb') as file:
                    msg_enc = bytearray(file.read())
                    encryption = encoding(origin_file_name, msg_enc, dest)
                    if encryption is False:
                        self.msg_box.delete('1.0', END)
                        self.msg_box.insert(END, 'Файл для кодировки '
                                                 'слишком большой!')
                        self.left_img_canvas.delete('all')
                        return
                    else:
                        write_in_file(self.file, encryption)
            except (IOError, ValueError, UnicodeDecodeError,
                    UnicodeEncodeError, FileNotFoundError):
                self.msg_box.delete('1.0', END)
                self.msg_box.insert(END, 'Неверный формат ввода данных!')
                return

            self.right_img = Image.open(self.file)
            w, h = self.right_img.size
            scale_w = 600 / w
            scale_h = 400 / h
            scale = min(scale_w, scale_h)
            new_w = math.ceil(scale * w)
            new_h = math.ceil(scale * h)
            img = self.right_img.resize((new_w, new_h), Image.NEAREST)

            self.right_photo = ImageTk.PhotoImage(img)
            self.right_img_canvas.create_image(600 / 2, 400 / 2, anchor=CENTER,
                                               image=self.right_photo)

            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)

    def clear(self):
        """
        Function for cleaning the text field
        """
        self.msg_box.delete('1.0', END)

    def create_widgets(self):
        """
        Function for creating widgets
        """
        left_frame = Frame(self)
        left_frame.pack(side=LEFT)

        show_frame = Frame(left_frame)
        show_frame.pack(side=TOP)

        open_frame = Frame(show_frame)
        open_frame.pack(side=TOP)

        open_label = Label(open_frame, text='Открыть BMP-файл:')
        open_label.pack(side=LEFT)

        open_button = Button(open_frame, text='Открыть',
                             command=self.open_file)
        open_button.pack(side=LEFT)

        self.left_img_canvas = Canvas(left_frame, bg='grey',
                                      width=600, height=400)
        self.left_img_canvas.pack(side=BOTTOM)

        right_frame = Frame(self)
        right_frame.pack(side=RIGHT)

        en_de_cry_frame = Frame(left_frame, height=10, width=20)
        en_de_cry_frame.pack(side=TOP)

        encod_button = Button(en_de_cry_frame, text='Закодировать',
                              command=self.encod)
        encod_button.pack(side=LEFT)

        decod_button = Button(en_de_cry_frame, text='Раскодировать',
                              command=self.decod)
        decod_button.pack(side=RIGHT)

        clear_button = Button(en_de_cry_frame, text="Очистить",
                              command=self.clear)
        clear_button.pack(side=RIGHT)

        center_frame = Frame(self)
        center_frame.pack(side=LEFT)
        msg_frame = Frame(right_frame)
        msg_frame.pack(side=TOP)

        self.scale = Scale(left_frame, orient=HORIZONTAL,
                           highlightbackground='black',
                           length=500, width=20, from_=1,
                           to=8, tickinterval=1, resolution=1)
        self.scale.pack(side=TOP)

        self.msg_box = Text(msg_frame, width=75, height=7)
        self.msg_box.pack(side=TOP)

        self.right_img_canvas = Canvas(right_frame, bg='grey',
                                       width=600, height=400)
        self.right_img_canvas.pack(side=BOTTOM)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "help":
            print(
                """
                This program is a graphical version of BMP steganography.
                Steganography is a way of transferring or storing information,
                taking into account the fact that such a
                transfer is kept secret.
                The program is implemented based on the LSB method,
                that is, replacing the last significant bits in the
                container with bits of the hidden message.
                To start the program, you need to enter the following data
                in the command line:
                python stegano_graphic.py
                To encode a message, you first need to open
                the bmp format picture.
                Next, the text box requires input: [path] [image]
                path - the path of the text file with the message
                for encryption.
                image - the name of the picture in which this
                message will be saved.
                To decode a message, you first need to open a BMP format image.
                Next, the text field requires input: [image]
                image - the name of the text file in which the decrypted
                message will be stored.
                """)
    else:
        root = Tk()
        graphic = Graphic_BMP(root)
        root.mainloop()


if __name__ == "__main__":
    main()
