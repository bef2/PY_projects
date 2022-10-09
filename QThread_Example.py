import sys, time
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QProgressBar, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QThread

import socket

TCP_IP = "192.168.0.134"
TCP_PORT = 5000
BUFFER_SIZE = 256

class ProgressBarThread(QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        value = 0
        while value < 100:
            value = value + 1
            self.mainwindow.progressbar.setValue(value)
            time.sleep(0.2)

class MyProgressbarWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.progressbar = QProgressBar()
        self.PushButtonLaunchLoading = QPushButton('Launch Loading')
        self.TextEditor = QTextEdit()
        self.setGeometry(300, 300, 300, 150)
        vbox = QVBoxLayout()
        vbox.addWidget(self.PushButtonLaunchLoading)
        vbox.addWidget(self.TextEditor)
        vbox.addWidget(self.progressbar)
        self.setLayout(vbox)

        self.PushButtonLaunchLoading.clicked.connect(self.launch_progressbar_filling)
        self.ProgressbarThread_instance = ProgressBarThread(mainwindow=self)

    def launch_progressbar_filling(self):
        self.ProgressbarThread_instance.start()

app = QApplication(sys.argv)
main = MyProgressbarWindow()
main.show()
sys.exit(app.exec_())