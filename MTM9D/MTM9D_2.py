import sys, time, serial, pandas, openpyxl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread


PERIOD_OPROSA = 1
COM_PORT = 'COM18'


class excelWriter:

    def __init__(self):
        self.file_name = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[:10].replace('-', '.') + '_' + \
                         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[11:].replace(':', '.') + '_MTM9D'
        writer = pandas.ExcelWriter(f'{self.file_name}.xlsx')
        writer.save()
        writer.close()
        self.excel_file = openpyxl.load_workbook(f'{self.file_name}.xlsx')
        self.excel_sheet = self.excel_file['Sheet1']
        self.excel_sheet[f'A1'] = '№'
        self.excel_sheet[f'B1'] = 'Дата'
        self.excel_sheet[f'C1'] = 'Время'
        self.excel_sheet[f'D1'] = 'Показания'
        self.excel_sheet[f'E1'] = 'Ед. Изм.'
        # self.excel_file.save(f'{self.file_name}.xlsx')

    def write(self,number_packet, line_data):
        self.excel_sheet[f'A{number_packet + 1}'] = number_packet
        self.excel_sheet[f'B{number_packet + 1}'] = line_data['date']
        self.excel_sheet[f'C{number_packet + 1}'] = line_data['time']
        self.excel_sheet[f'D{number_packet + 1}'] = line_data['values']
        self.excel_sheet[f'E{number_packet + 1}'] = line_data['unit']
        self.excel_file.save(f'{self.file_name}.xlsx')

    def save(self):
        self.excel_file.save(f'{self.file_name}.xlsx')
        


class serial_485_stream(QThread):
    flag_state = False

    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
        
        self.ComPort = serial.Serial(COM_PORT) # открыть COM порт
        self.ComPort.baudrate = 9600 # Бит в секунду
        self.ComPort.bytesize = 8    # Биты данных = 8
        self.ComPort.parity   = 'N'  # Нет четности
        self.ComPort.stopbits = 1    # Стоповые биты = 1
        # self.flag_state = False       # Флаг для кнопок Старт(True) и Стоп(False)

    def run(self):

        xl_wr = excelWriter()

        number_packet = 1
        if self.flag_state:
            self.mainwindow.label_stat_1.setText(f"Запущено")
        while self.flag_state:
            send_command = "001M^\r"
            self.ComPort.write(send_command.encode())
            dataIn = self.ComPort.read(12).decode()

            data_formatted = f"{int(dataIn[4:8]) * 1 / 10 ** (23 - int(dataIn[8:10]))}"
            self.mainwindow.label_digit.setText(data_formatted)

            line_data = {'num_pack': number_packet,
                            'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[:11],
                            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[11:],
                            'values': data_formatted,
                            'unit': self.mainwindow.label_unit.text(),
                        }

            self.mainwindow.label_stat_3.setText(f"Измерение: {line_data['num_pack']}, {line_data['date']}, {line_data['time']}")

            xl_wr.write(number_packet, line_data)
            
            number_packet += 1
            time.sleep(PERIOD_OPROSA)

        self.mainwindow.label_stat_1.setText(f"Остановлено")
        # xl_wr.save()


class Ui_MainWindow():

    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)

        self.main_widget = QtWidgets.QWidget(MainWindow)
        

        self.frame_status = QtWidgets.QFrame(self.main_widget)
        self.frame_status.setMaximumSize(QtCore.QSize(16777215, 100))

        self.label_stat_1 = QtWidgets.QLabel(self.frame_status)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_1.setFont(font)
        
        self.label_stat_2 = QtWidgets.QLabel(self.frame_status)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_2.setFont(font)

        self.label_stat_3 = QtWidgets.QLabel(self.frame_status)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_3.setFont(font)

        self.frame_statusVLayout = QtWidgets.QVBoxLayout(self.frame_status)
        self.frame_statusVLayout.addWidget(self.label_stat_1)
        self.frame_statusVLayout.addWidget(self.label_stat_2)
        self.frame_statusVLayout.addWidget(self.label_stat_3)

        
        self.frame_value = QtWidgets.QFrame(self.main_widget)

        self.label_digit = QtWidgets.QLabel(self.frame_value)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(100)
        self.label_digit.setFont(font)
        self.label_digit.setStyleSheet("color: rgb(85, 170, 255);")
        self.label_digit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

        self.label_unit = QtWidgets.QLabel(self.frame_value)
        self.label_unit.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(54)
        self.label_unit.setFont(font)
        self.label_unit.setStyleSheet("color: rgb(180, 180, 180);")
        self.label_unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

        self.frame_valueHLayout = QtWidgets.QHBoxLayout(self.frame_value)
        self.frame_valueHLayout.addWidget(self.label_digit)
        self.frame_valueHLayout.addWidget(self.label_unit)


        self.frame_btns = QtWidgets.QFrame(self.main_widget)
        self.frame_btns.setMaximumSize(QtCore.QSize(16777215, 100))

        self.btn_start = QtWidgets.QPushButton(self.frame_btns)
        self.btn_start.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setWeight(50)
        self.btn_start.setFont(font)

        self.btn_stop = QtWidgets.QPushButton(self.frame_btns)
        self.btn_stop.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setWeight(50)
        self.btn_stop.setFont(font)

        self.frame_btnsHLayout = QtWidgets.QHBoxLayout(self.frame_btns)
        self.frame_btnsHLayout.addWidget(self.btn_start)
        self.frame_btnsHLayout.addWidget(self.btn_stop)
        
        
        self.main_widgetVLayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widgetVLayout.addWidget(self.frame_status)
        self.main_widgetVLayout.addWidget(self.frame_value)
        self.main_widgetVLayout.addWidget(self.frame_btns)
        
        MainWindow.setCentralWidget(self.main_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btn_start.clicked.connect(self.start_485_stream)
        self.btn_stop.clicked.connect(self.stop_485_stream)

        self.stream_485_Thread_instance = serial_485_stream(mainwindow=self)

    def closeEvent(self, event):
        # Переопределить colseEvent
        reply = QtWidgets.QMessageBox.question\
        (self, 'Вы нажали на крестик',
            "Вы уверены, что хотите уйти?",
             QtWidgets.QMessageBox.Yes,
             QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def start_485_stream(self):
        serial_485_stream.flag_state = True
        # self.stream_485_Thread_instance.flag_state = True
        self.stream_485_Thread_instance.start() 
        # self.label_stat_1.setText(f'Запущено')

    def stop_485_stream(self):
        serial_485_stream.flag_state = False
        # self.stream_485_Thread_instance.flag_state = False
        # self.stream_485_Thread_instance.terminate()
        # self.label_stat_1.setText(f'Остановлено')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MTM9D"))
        self.label_stat_1.setText(_translate("MainWindow", "Остановлено"))
        self.label_stat_2.setText(_translate("MainWindow", "Чтение измерения давления"))
        self.label_stat_3.setText(_translate("MainWindow", "Измерение: 0"))
        self.label_digit.setText(_translate("MainWindow", "-0"))
        self.label_unit.setText(_translate("MainWindow", "mBar"))
        self.btn_start.setText(_translate("MainWindow", "Старт"))
        self.btn_stop.setText(_translate("MainWindow", "Стоп"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
