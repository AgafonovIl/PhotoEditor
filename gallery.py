import sys

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, \
    QPushButton
from GPage import Ui_MainWindow

from base64 import b16encode as enc64
from base64 import b16decode as dec64
from io import BytesIO
import sqlite3
import editing


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.vbox = QVBoxLayout()
        self.widget = QWidget()
        self.pushButton.clicked.connect(self.add_new_label)
        self.scrollArea.setWidgetResizable(True)
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_2.clicked.connect(self.update)
        self.pushButton_4.clicked.connect(self.change)

        for i in self.take_from_table():
            qim = ImageQt(self.export(i[1]))
            pixmap = QtGui.QPixmap.fromImage(qim)
            pixmap = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
            id = QLabel(str(i[0]))
            name = QLabel(i[2])
            name.resize(50, 100)
            object = QLabel()
            object.setPixmap(pixmap)
            hbox = QHBoxLayout()
            hbox.addWidget(id)
            hbox.addWidget(object)
            hbox.addWidget(name)
            self.vbox.addLayout(hbox)
            self.widget.setLayout(self.vbox)
            self.scrollArea.setWidget(self.widget)

    def add_new_label(self):
        # Открытие файла
        pic = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(* .jpg * .png)")
        way = pic[0]
        name_pic = pic[0].split('/')[-1][:pic[0].split('/')[-1].index('.')]
        imagePath = pic[0]
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)

        # Сохранение в БД
        self.write_to_table(way, way, name=name_pic)

        # Отображение на экране
        name = QLabel(name_pic)
        name.resize(50, 100)
        object = QLabel()
        object.setPixmap(pixmap)
        hbox = QHBoxLayout()
        hbox.addWidget(object)
        hbox.addWidget(name)
        self.vbox.addLayout(hbox)
        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)

    def binary_pic(self, pic):
        with open(pic, 'rb') as f:
            binary = enc64(f.read())
        return binary

    def export(self, binary):
        image = BytesIO(dec64(binary))
        i = Image.open(image)
        return i

    def update(self):

        #self.scrollArea.

        for i in self.take_from_table():
            qim = ImageQt(self.export(i[1]))
            pixmap = QtGui.QPixmap.fromImage(qim)
            pixmap = pixmap.scaled(750, 750, QtCore.Qt.KeepAspectRatio)
            id = QLabel(str(i[0]))
            name = QLabel(i[2])
            name.resize(50, 100)
            object = QLabel()
            object.setPixmap(pixmap)
            hbox = QHBoxLayout()
            hbox.addWidget(id)
            hbox.addWidget(object)
            hbox.addWidget(name)
            self.vbox.addLayout(hbox)
            self.widget.setLayout(self.vbox)
            self.scrollArea.setWidget(self.widget)

    def write_to_table(self, pic, way, name='Без Имени'):
        binary_st = self.binary_pic(pic)
        conn = sqlite3.connect("kash.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO keeper (photo, inf, name) VALUES(?, ?, ?)", [sqlite3.Binary(binary_st), way, name])
        conn.commit()
        cursor.close()
        conn.close()

    def take_from_table(self):
        conn = sqlite3.connect("kash.db")
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from keeper"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records

    def change(self):
        self.bla = editing.Example(int(self.lineEdit_2.text()))
        self.bla.show()

    def delete(self):
        conn = sqlite3.connect('kash.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM keeper WHERE id_keeper = ?", [int(self.lineEdit.text())])
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
