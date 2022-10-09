import sys
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QApplication, QLayout, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QFrame, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, Qt


class myMainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(150, 100, 800, 500)
        self.setWindowTitle('Archimage')

        # self.frame_image = QFrame()

        # self.label_image = QLabel('Hello')
        
        # self.layout_image = QVBoxLayout(self.frame_image)
        # self.layout_image.addWidget(self.label_image)

        # self.layout_main = QHBoxLayout(self)
        # self.layout_main.addWidget(self.frame_image)

        self.layout_main = QVBoxLayout(self)
        self.layout_image = QVBoxLayout(self.layout_main)
        
        self.label_image = QLabel('Hello')
        self.layout_image.addWidget(self.label_image)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = myMainWindow()
    win.show()
    sys.exit(app.exec())