import sys

from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from EditPage import Ui_MainWindow

from base64 import b16encode as enc64
from base64 import b16decode as dec64
from io import BytesIO
import sqlite3

from PIL import Image, ImageFilter


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self, id):
        self.id = id
        super().__init__()
        self.setupUi(self)

        self.count = 0
        self.count_2 = 0
        self.clean_bd()

        self.pushButton.clicked.connect(self.flip_horizontally)
        self.pushButton_2.clicked.connect(self.flip_vertically)
        self.pushButton_3.clicked.connect(self.rotate_left)
        self.pushButton_4.clicked.connect(self.rotate_right)
        self.pushButton_5.clicked.connect(self.cancellation_of_the_action)
        self.pushButton_6.clicked.connect(self.cancellation_cancellation)
        self.pushButton_7.clicked.connect(self.clean_bd)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.clicked.connect(self.gauss)
        self.pushButton_10.clicked.connect(self.contour)
        self.pushButton_11.clicked.connect(self.delite)
        self.pushButton_12.clicked.connect(self.edge)
        self.pushButton_13.clicked.connect(self.edge_more)
        self.pushButton_14.clicked.connect(self.emboss)
        self.pushButton_15.clicked.connect(self.find_edges)
        self.pushButton_16.clicked.connect(self.smooth)
        self.pushButton_17.clicked.connect(self.sharpen)

        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)

    # def save(self, way='Отредактированое', name='Без Имени'):
    #     binary_st = self.binary_pic(pic)
    #     conn = sqlite3.connect("kash.db")
    #     cursor = conn.cursor()
    #     cursor.execute("INSERT INTO keeper (photo, inf, name) VALUES(?, ?, ?)", [sqlite3.Binary(binary_st), way, name])
    #     conn.commit()
    #     cursor.close()
    #     conn.close()

    def open(self):
        conn = sqlite3.connect('kash.db')
        cursor = conn.cursor()
        sql_select_query = """select * from keeper where id_keeper = ?"""
        cursor.execute(sql_select_query, (self.id,))
        records = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return records[0][1]

    def binary_pic(self, pic):
        with open(pic, 'rb') as f:
            binary = enc64(f.read())
        return binary

    def export(self, binary):
        image = BytesIO(dec64(binary))
        i = Image.open(image)
        return i

    def clean_bd(self):
        conn = sqlite3.connect('kash.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cash')
        qim = ImageQt(self.export(self.open()))
        binary_st = dec64(self.open())
        pixmap = QtGui.QPixmap.fromImage(qim)
        pixmap = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.count = 0
        cursor.execute("INSERT INTO cash (id, file) VALUES(?, ?)", [self.count, sqlite3.Binary(binary_st)])
        conn.commit()
        conn.close()

        self.pushButton_5.setEnabled(False)
        i = self.export(self.open())
        i.save('out.JPG')

    def delite(self):
        conn = sqlite3.connect('kash.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cash WHERE id > ?", [self.count])
        conn.commit()
        cursor.close()
        conn.close()

    def write_to_table(self, pic):
        binary_st = self.binary_pic(pic)
        conn = sqlite3.connect("kash.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cash (id, file) VALUES(?, ?)", [self.count, sqlite3.Binary(binary_st)])
        conn.commit()
        cursor.close()
        conn.close()

    def take_from_table(self, id):
        conn = sqlite3.connect("kash.db")
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from cash where id = ?"""
        cursor.execute(sqlite_select_query, (id,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
        return record

    def cancellation_of_the_action(self):
        self.count -= 1
        if self.count == 0:
            self.pushButton_5.setEnabled(False)
            conn = sqlite3.connect('kash.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cash')
            qim = ImageQt(self.export(self.open()))
            binary_st = dec64(self.open())
            pixmap = QtGui.QPixmap.fromImage(qim)
            pixmap = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)
            self.count = 0
            cursor.execute("INSERT INTO cash (id, file) VALUES(?, ?)", [self.count, sqlite3.Binary(binary_st)])
            conn.commit()
            conn.close()
            i = self.export(self.open())
            i.save('out.JPG')
            self.pushButton_6.setEnabled(False)
        else:
            r = self.export(self.take_from_table(self.count)[1])
            r.save('out.JPG')
            pixmap = QPixmap("out.JPG")
            pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap4)
            self.pushButton_6.setEnabled(True)

    def cancellation_cancellation(self):
        self.count += 1
        if self.count == self.count_2:
            self.pushButton_6.setEnabled(False)
        r = self.export(self.take_from_table(self.count)[1])
        r.save('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def flip_horizontally(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.transpose(Image.FLIP_LEFT_RIGHT)
        r.save('out.JPG')
        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def flip_vertically(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.transpose(Image.FLIP_TOP_BOTTOM)
        r.save('out.JPG')
        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def rotate_right(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.transpose(Image.ROTATE_90)
        r.save('out.JPG')
        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def rotate_left(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.transpose(Image.ROTATE_270)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def gauss(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.BLUR)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def contour(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.CONTOUR)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def detail(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.DETAIL)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def edge(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.EDGE_ENHANCE)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def edge_more(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.EDGE_ENHANCE_MORE)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def emboss(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.EMBOSS)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def find_edges(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.FIND_EDGES)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def smooth(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.SMOOTH_MORE)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)

    def sharpen(self):
        if self.count != self.count_2:
            self.delite()
            self.count_2 = self.count
        self.count += 1
        self.count_2 += 1
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

        i = Image.open('out.JPG')
        r = i.filter(ImageFilter.SHARPEN)
        r.save('out.JPG')

        self.write_to_table('out.JPG')
        pixmap = QPixmap("out.JPG")
        pixmap4 = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example(7)
    ex.show()
    sys.exit(app.exec())
