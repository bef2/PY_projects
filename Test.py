from PyQt5 import Qt
import sys
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QPushButton, QSizePolicy, QFrame, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, Qt



class Widget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()

        btn1 = QPushButton("Button 1")

        btn_layout.addWidget(btn1)

        layout.addLayout(btn_layout)


if __name__ == '__main__':
    app = QApplication([])
    w = Widget()
    w.show()
    app.exec()