import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from png import *


class Widget(QWidget):
    """Window class"""
    def __init__(self, png):
        super().__init__()

        self.setWindowTitle('PNG по пикселям')
        self.png = png
        self.img_width = self.png.width
        self.img_height = self.png.height
        self.resize(self.img_width, self.img_height)
        self.pixel_list = [(x, y) for y in range(self.img_height)
                           for x in range(self.img_width)]

        random.shuffle(self.pixel_list)
        if self.png.color_type == 0 or self.png.color_type == 2 \
                or self.png.color_type == 3:
            self.new_img = QImage(self.img_width,
                                  self.img_height,
                                  QImage.Format_RGB32)
        if self.png.color_type == 4 or self.png.color_type == 6:
            self.new_img = QImage(self.img_width,
                                  self.img_height,
                                  QImage.Format_RGBA8888)
        self.new_img.fill(Qt.white)
        self.layout()

        self.timer = QTimer()
        self.timer.timeout.connect(self._draw_pixel)
        self.timer.start(1)  # 1 ms

    def _draw_pixel(self):
        """Pixel random drawing function"""
        pixels_by_step = 100
        for _ in range(pixels_by_step):
            if self.pixel_list:
                y, x = self.pixel_list.pop()
                pixel = self.png.list_pixel[x][y]

                if self.png.color_type == 0 or \
                        self.png.color_type == 2 or \
                        self.png.color_type == 3:
                    self.new_img.setPixel(y, x, QColor(pixel[0],
                                                       pixel[1],
                                                       pixel[2]).rgba())
                if self.png.color_type == 4 or self.png.color_type == 6:
                    self.new_img.setPixel(y, x, QColor(pixel[0],
                                                       pixel[1],
                                                       pixel[2],
                                                       pixel[3]).rgba())
            else:
                self.timer.stop()
                break
        self.update()

    def paintEvent(self, event):
        """Picture drawing function"""
        painter = QPainter(self)
        painter.drawImage(0, 0, self.new_img)


def main():
    if sys.argv[1] == "--help" or sys.argv[1] == "help":
        print(
            """
            This is a program for visualizing PNG images
            based on a list of pixels. Pixels appear on
            the screen randomly, filling the entire image.
            To run, enter:
            python png.graphic.py [image]
            image - PNG format file
            """)
    else:
        app = QApplication([])
        png = PNG()
        if png.open_png(sys.argv[1]) is False:
            sys.exit(1)
        else:
            w = Widget(png)
            w.show()
            app.exec()


if __name__ == '__main__':
    main()
