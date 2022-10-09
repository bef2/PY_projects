from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setGeometry(100, 100, 200, 100)
    self.label = QLabel('Hello World!', self)
    self.label.setAlignment(Qt.AlignCenter)
    self.label.setStyleSheet('font-size: 12pt; background-color: red')
    self.show()

app = QApplication([])
win = Window()
app.exec()