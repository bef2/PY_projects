from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))

        self.main_widget = QtWidgets.QWidget(MainWindow)
        self.main_widget.setObjectName("main_widget")
        self.main_widgetVLayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widgetVLayout.setObjectName("main_widgetVLayout")

        self.frame_status = QtWidgets.QFrame(self.main_widget)
        self.frame_status.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_status.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_status.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_status.setObjectName("frame_status")

        self.frame_statusVLayout = QtWidgets.QVBoxLayout(self.frame_status)
        self.frame_statusVLayout.setContentsMargins(5, 5, 5, 5)
        self.frame_statusVLayout.setSpacing(1)
        self.frame_statusVLayout.setObjectName("frame_statusVLayout")

        self.label_stat_1 = QtWidgets.QLabel(self.frame_status)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_1.setFont(font)
        self.label_stat_1.setObjectName("label_stat_1")
        self.frame_statusVLayout.addWidget(self.label_stat_1)

        self.label_stat_2 = QtWidgets.QLabel(self.frame_status)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_2.setFont(font)
        self.label_stat_2.setObjectName("label_stat_2")
        self.frame_statusVLayout.addWidget(self.label_stat_2)

        self.label_stat_3 = QtWidgets.QLabel(self.frame_status)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_3.setFont(font)
        self.label_stat_3.setObjectName("label_stat_3")
        self.frame_statusVLayout.addWidget(self.label_stat_3)


        self.main_widgetVLayout.addWidget(self.frame_status)
        

        self.frame_value = QtWidgets.QFrame(self.main_widget)
        self.frame_value.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_value.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_value.setObjectName("frame_value")

        self.frame_valueHLayout = QtWidgets.QHBoxLayout(self.frame_value)
        self.frame_valueHLayout.setSpacing(15)
        self.frame_valueHLayout.setObjectName("frame_valueHLayout")

        self.label_digit = QtWidgets.QLabel(self.frame_value)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(100)
        self.label_digit.setFont(font)
        self.label_digit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_digit.setObjectName("label_digit")

        self.frame_valueHLayout.addWidget(self.label_digit)

        self.label_unit = QtWidgets.QLabel(self.frame_value)
        self.label_unit.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(54)
        self.label_unit.setFont(font)
        self.label_unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_unit.setObjectName("label_unit")

        self.frame_valueHLayout.addWidget(self.label_unit)
        self.main_widgetVLayout.addWidget(self.frame_value)

        self.frame_btns = QtWidgets.QFrame(self.main_widget)
        self.frame_btns.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns.setObjectName("frame_btns")

        self.frame_btnsHLayout = QtWidgets.QHBoxLayout(self.frame_btns)
        self.frame_btnsHLayout.setSpacing(0)
        self.frame_btnsHLayout.setObjectName("frame_btnsHLayout")

        self.btn_start = QtWidgets.QPushButton(self.frame_btns)
        self.btn_start.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.frame_btnsHLayout.addWidget(self.btn_start)

        self.btn_stop = QtWidgets.QPushButton(self.frame_btns)
        self.btn_stop.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.frame_btnsHLayout.addWidget(self.btn_stop)
        
        self.main_widgetVLayout.addWidget(self.frame_btns)
        MainWindow.setCentralWidget(self.main_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_stat_1.setText(_translate("MainWindow", "Статус 1"))
        self.label_stat_2.setText(_translate("MainWindow", "Статус 2"))
        self.label_stat_3.setText(_translate("MainWindow", "Статус 3"))
        self.label_digit.setText(_translate("MainWindow", "9999"))
        self.label_unit.setText(_translate("MainWindow", "Torr"))
        self.btn_start.setText(_translate("MainWindow", "Старт"))
        self.btn_stop.setText(_translate("MainWindow", "Стоп"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
