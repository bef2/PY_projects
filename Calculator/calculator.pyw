# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calculator.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 380)
        MainWindow.setMinimumSize(QtCore.QSize(360, 380))
        MainWindow.setMaximumSize(QtCore.QSize(360, 380))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(360, 380))
        self.centralwidget.setMaximumSize(QtCore.QSize(360, 380))
        self.centralwidget.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.centralwidget.setObjectName("centralwidget")
        self.label_result = QtWidgets.QLabel(self.centralwidget)
        self.label_result.setGeometry(QtCore.QRect(10, 10, 340, 50))
        self.label_result.setMaximumSize(QtCore.QSize(340, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_result.setFont(font)
        self.label_result.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.label_result.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_result.setObjectName("label_result")
        self.button_backspace = QtWidgets.QPushButton(self.centralwidget)
        self.button_backspace.setGeometry(QtCore.QRect(10, 70, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.button_backspace.setFont(font)
        self.button_backspace.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_backspace.setObjectName("button_backspace")
        self.button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_1.setGeometry(QtCore.QRect(10, 250, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_1.setFont(font)
        self.button_1.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_1.setObjectName("button_1")
        self.button_0 = QtWidgets.QPushButton(self.centralwidget)
        self.button_0.setGeometry(QtCore.QRect(10, 310, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_0.setFont(font)
        self.button_0.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_0.setObjectName("button_0")
        self.button_oneclear = QtWidgets.QPushButton(self.centralwidget)
        self.button_oneclear.setGeometry(QtCore.QRect(80, 70, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_oneclear.setFont(font)
        self.button_oneclear.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_oneclear.setObjectName("button_oneclear")
        self.button_allclear = QtWidgets.QPushButton(self.centralwidget)
        self.button_allclear.setGeometry(QtCore.QRect(150, 70, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_allclear.setFont(font)
        self.button_allclear.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_allclear.setObjectName("button_allclear")
        self.button_sign = QtWidgets.QPushButton(self.centralwidget)
        self.button_sign.setGeometry(QtCore.QRect(220, 70, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_sign.setFont(font)
        self.button_sign.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_sign.setObjectName("button_sign")
        self.button_sqrt = QtWidgets.QPushButton(self.centralwidget)
        self.button_sqrt.setGeometry(QtCore.QRect(290, 70, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.button_sqrt.setFont(font)
        self.button_sqrt.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_sqrt.setObjectName("button_sqrt")
        self.button_percent = QtWidgets.QPushButton(self.centralwidget)
        self.button_percent.setGeometry(QtCore.QRect(290, 130, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_percent.setFont(font)
        self.button_percent.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_percent.setObjectName("button_percent")
        self.button_inverse = QtWidgets.QPushButton(self.centralwidget)
        self.button_inverse.setGeometry(QtCore.QRect(290, 190, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_inverse.setFont(font)
        self.button_inverse.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_inverse.setObjectName("button_inverse")
        self.button_equal = QtWidgets.QPushButton(self.centralwidget)
        self.button_equal.setGeometry(QtCore.QRect(290, 250, 61, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.button_equal.setFont(font)
        self.button_equal.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.button_equal.setObjectName("button_equal")
        self.button_point = QtWidgets.QPushButton(self.centralwidget)
        self.button_point.setGeometry(QtCore.QRect(150, 310, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.button_point.setFont(font)
        self.button_point.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_point.setObjectName("button_point")
        self.button_plus = QtWidgets.QPushButton(self.centralwidget)
        self.button_plus.setGeometry(QtCore.QRect(220, 310, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_plus.setFont(font)
        self.button_plus.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_plus.setObjectName("button_plus")
        self.button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_2.setGeometry(QtCore.QRect(80, 250, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_2.setFont(font)
        self.button_2.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_2.setObjectName("button_2")
        self.button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.button_3.setGeometry(QtCore.QRect(150, 250, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_3.setFont(font)
        self.button_3.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_3.setObjectName("button_3")
        self.button_4 = QtWidgets.QPushButton(self.centralwidget)
        self.button_4.setGeometry(QtCore.QRect(10, 190, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_4.setFont(font)
        self.button_4.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_4.setObjectName("button_4")
        self.button_5 = QtWidgets.QPushButton(self.centralwidget)
        self.button_5.setGeometry(QtCore.QRect(80, 190, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_5.setFont(font)
        self.button_5.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_5.setObjectName("button_5")
        self.button_6 = QtWidgets.QPushButton(self.centralwidget)
        self.button_6.setGeometry(QtCore.QRect(150, 190, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_6.setFont(font)
        self.button_6.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_6.setObjectName("button_6")
        self.button_7 = QtWidgets.QPushButton(self.centralwidget)
        self.button_7.setGeometry(QtCore.QRect(10, 130, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_7.setFont(font)
        self.button_7.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_7.setObjectName("button_7")
        self.button_8 = QtWidgets.QPushButton(self.centralwidget)
        self.button_8.setGeometry(QtCore.QRect(80, 130, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_8.setFont(font)
        self.button_8.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_8.setObjectName("button_8")
        self.button_9 = QtWidgets.QPushButton(self.centralwidget)
        self.button_9.setGeometry(QtCore.QRect(150, 130, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.button_9.setFont(font)
        self.button_9.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.button_9.setObjectName("button_9")
        self.button_minus = QtWidgets.QPushButton(self.centralwidget)
        self.button_minus.setGeometry(QtCore.QRect(220, 250, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.button_minus.setFont(font)
        self.button_minus.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_minus.setObjectName("button_minus")
        self.button_multyply = QtWidgets.QPushButton(self.centralwidget)
        self.button_multyply.setGeometry(QtCore.QRect(220, 190, 61, 51))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_multyply.setFont(font)
        self.button_multyply.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_multyply.setObjectName("button_multyply")
        self.button_division = QtWidgets.QPushButton(self.centralwidget)
        self.button_division.setGeometry(QtCore.QRect(220, 130, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_division.setFont(font)
        self.button_division.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.button_division.setObjectName("button_division")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ------------------------------------------------------------
        self.add_functions()
        self.is_equal = False
        # ------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Калькулятор"))
        self.label_result.setText(_translate("MainWindow", "0"))
        self.button_backspace.setText(_translate("MainWindow", "BKSPC"))
        self.button_1.setText(_translate("MainWindow", "1"))
        self.button_0.setText(_translate("MainWindow", "0"))
        self.button_oneclear.setText(_translate("MainWindow", "CE"))
        self.button_allclear.setText(_translate("MainWindow", "C"))
        self.button_sign.setText(_translate("MainWindow", "+/-"))
        self.button_sqrt.setText(_translate("MainWindow", "SQRT"))
        self.button_percent.setText(_translate("MainWindow", "%"))
        self.button_inverse.setText(_translate("MainWindow", "1/x"))
        self.button_equal.setText(_translate("MainWindow", "="))
        self.button_point.setText(_translate("MainWindow", ","))
        self.button_plus.setText(_translate("MainWindow", "+"))
        self.button_2.setText(_translate("MainWindow", "2"))
        self.button_3.setText(_translate("MainWindow", "3"))
        self.button_4.setText(_translate("MainWindow", "4"))
        self.button_5.setText(_translate("MainWindow", "5"))
        self.button_6.setText(_translate("MainWindow", "6"))
        self.button_7.setText(_translate("MainWindow", "7"))
        self.button_8.setText(_translate("MainWindow", "8"))
        self.button_9.setText(_translate("MainWindow", "9"))
        self.button_minus.setText(_translate("MainWindow", "-"))
        self.button_multyply.setText(_translate("MainWindow", "*"))
        self.button_division.setText(_translate("MainWindow", "/"))

    # --------------------------------------------------------------
    def add_functions(self):
        self.button_0.clicked.connect(lambda: self.write_number(self.button_0.text()))
        self.button_1.clicked.connect(lambda: self.write_number(self.button_1.text()))
        self.button_2.clicked.connect(lambda: self.write_number(self.button_2.text()))
        self.button_3.clicked.connect(lambda: self.write_number(self.button_3.text()))
        self.button_4.clicked.connect(lambda: self.write_number(self.button_4.text()))
        self.button_5.clicked.connect(lambda: self.write_number(self.button_5.text()))
        self.button_6.clicked.connect(lambda: self.write_number(self.button_6.text()))
        self.button_7.clicked.connect(lambda: self.write_number(self.button_7.text()))
        self.button_8.clicked.connect(lambda: self.write_number(self.button_8.text()))
        self.button_9.clicked.connect(lambda: self.write_number(self.button_9.text()))
        self.button_point.clicked.connect(lambda: self.write_point(self.button_point.text()))
        self.button_plus.clicked.connect(lambda: self.write_number(self.button_plus.text()))
        self.button_minus.clicked.connect(lambda: self.write_number(self.button_minus.text()))
        self.button_multyply.clicked.connect(lambda: self.write_number(self.button_multyply.text()))
        self.button_division.clicked.connect(lambda: self.write_number(self.button_division.text()))
        self.button_equal.clicked.connect(self.results)
        self.button_allclear.clicked.connect(self.erase)



    def write_number(self, number):
        if self.label_result.text() == "0" or self.is_equal:
            self.label_result.setText(number)
            self.is_equal = False
        else: 
            self.label_result.setText(self.label_result.text() + number)

    def results(self):
        res = eval(self.label_result.text())
        self.label_result.setText(str(res))
        self.is_equal = True

    def erase (self):
        self.label_result.setText("0")

    def write_point (self, point):
        if self.label_result.text() == self.is_equal:
            self.is_equal = False
        else: 
            self.label_result.setText(self.label_result.text() + ".")

    # --------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
