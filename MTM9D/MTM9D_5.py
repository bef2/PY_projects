import sys, os, time, serial, pandas, openpyxl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


PERIOD_OPROSA = 1
COM_PORT = 'COM18'


class excelWriter:
    def __init__(self):
        self.file_name = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[:10].replace('-', '.') + '_' + \
                         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[11:].replace(':', '.') + '_MTM9D'
        writer = pandas.ExcelWriter(f'{self.file_name}.xlsx')
        writer.save()
        self.excel_file = openpyxl.load_workbook(f'{self.file_name}.xlsx')
        self.excel_sheet = self.excel_file['Sheet1']
        self.excel_sheet[f'A1'] = '№'
        self.excel_sheet[f'B1'] = 'Дата'
        self.excel_sheet[f'C1'] = 'Время'
        self.excel_sheet[f'D1'] = 'Показания'
        self.excel_sheet[f'E1'] = 'Ед. Изм.'

    def write(self,row, line_data):
        self.excel_sheet[f'A{row}'] = line_data['num_pack']
        self.excel_sheet[f'B{row}'] = line_data['date']
        self.excel_sheet[f'C{row}'] = line_data['time']
        self.excel_sheet[f'D{row}'] = line_data['values']
        self.excel_sheet[f'E{row}'] = line_data['unit']
        self.excel_file.save(f'{self.file_name}.xlsx')

        
class serial_485_stream(QThread):
    flag_state = False
    number_packet = 1
    row = 2
    xl_wr = excelWriter()
    data_figure = []

    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
        
        self.ComPort = serial.Serial(COM_PORT) # открыть COM порт
        self.ComPort.baudrate = 9600 # Бит в секунду
        self.ComPort.bytesize = 8    # Биты данных = 8
        self.ComPort.parity   = 'N'  # Нет четности
        self.ComPort.stopbits = 1    # Стоповые биты = 1

    def run(self):
        if self.flag_state:
            self.mainwindow.label_stat_1.setText(f"Запущено")
        while self.flag_state:
            send_command = "001M^\r"
            self.ComPort.write(send_command.encode())
            dataIn = self.ComPort.read(12).decode()

            data_formatted = f"{int(dataIn[4:8]) * 1 / 10 ** (23 - int(dataIn[8:10]))}"
            self.mainwindow.label_digit.setText(data_formatted)

            line_data = {'num_pack': self.number_packet,
                        'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[:11],
                        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[11:],
                        'values': data_formatted,
                        'unit': self.mainwindow.label_unit.text(),}

            self.mainwindow.label_stat_3.setText(f"Измерение: {line_data['num_pack']}, {line_data['date']}, {line_data['time']}")
            self.xl_wr.write(self.row, line_data)

            self.data_figure.append(float(line_data['values']))
            self.mainwindow.plot()

            self.row += 1
            self.number_packet += 1
            time.sleep(PERIOD_OPROSA)    
        self.mainwindow.label_stat_1.setText(f"Остановлено")


class myWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1200, 520)
        self.setMinimumWidth(1200)
        self.setWindowTitle("MTM9D")

        self.frame_remPanel = QtWidgets.QFrame(self)
        
        self.frame_status = QtWidgets.QFrame(self)
        self.frame_status.setMaximumSize(QtCore.QSize(16777215, 100))

        self.label_stat_1 = QtWidgets.QLabel(self.frame_status)
        self.label_stat_1.setText("Остановлено")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_1.setFont(font)
        
        self.label_stat_2 = QtWidgets.QLabel(self.frame_status)
        self.label_stat_2.setText("Чтение измерения давления")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_2.setFont(font)

        self.label_stat_3 = QtWidgets.QLabel(self.frame_status)
        self.label_stat_3.setText("Измерение: 0")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_3.setFont(font)

        self.frame_statusVLayout = QtWidgets.QVBoxLayout(self.frame_status)
        self.frame_statusVLayout.addWidget(self.label_stat_1)
        self.frame_statusVLayout.addWidget(self.label_stat_2)
        self.frame_statusVLayout.addWidget(self.label_stat_3)

        self.frame_value = QtWidgets.QFrame(self)

        self.label_digit = QtWidgets.QLabel(self.frame_value)
        self.label_digit.setText("-0")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(100)
        self.label_digit.setFont(font)
        self.label_digit.setStyleSheet("color: rgb(85, 170, 255);")
        self.label_digit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignTop)
        self.label_digit.setMinimumSize(QtCore.QSize(520, 16777215))

        self.label_unit = QtWidgets.QLabel(self.frame_value)
        self.label_unit.setText("mBar")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(54)
        self.label_unit.setFont(font)
        self.label_unit.setStyleSheet("color: rgb(180, 180, 180);")
        self.label_unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)

        self.layout_frame_value = QtWidgets.QVBoxLayout(self.frame_value)
        self.layout_frame_value.addWidget(self.label_unit)
        self.layout_frame_value.addWidget(self.label_digit)

        self.frame_buttons = QtWidgets.QFrame(self)
        self.frame_buttons.setMaximumSize(QtCore.QSize(16777215, 100))

        self.button_start = QtWidgets.QPushButton(self.frame_buttons)
        self.button_start.setMaximumSize(QtCore.QSize(150, 40))
        self.button_start.setText("Старт")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setWeight(50)
        self.button_start.setFont(font)
        self.button_start.clicked.connect(self.start_485_stream)

        self.button_stop = QtWidgets.QPushButton(self.frame_buttons)
        self.button_stop.setMaximumSize(QtCore.QSize(150, 40))
        self.button_stop.setText("Стоп")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setWeight(50)
        self.button_stop.setFont(font)
        self.button_stop.clicked.connect(self.stop_485_stream)

        self.layout_buttons = QtWidgets.QHBoxLayout(self.frame_buttons)
        self.layout_buttons.addWidget(self.button_start)
        self.layout_buttons.addWidget(self.button_stop)

        self.layout_frame_remPanel = QtWidgets.QVBoxLayout(self.frame_remPanel)
        self.layout_frame_remPanel.addWidget(self.frame_status)
        self.layout_frame_remPanel.addWidget(self.frame_value)
        self.layout_frame_remPanel.addWidget(self.frame_buttons)

        self.frame_figure = QtWidgets.QFrame(self)

        self.figure = plt.figure()
        self.figure.add_subplot(111)
        plt.title("График измерения давления")
        plt.xlabel("Время, с")
        plt.ylabel("Давление, mbar")
        plt.yscale('log')
        plt.grid(which="major", linestyle="solid", color="black", linewidth=0.5)
        plt.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout_frame_figure = QtWidgets.QVBoxLayout(self.frame_figure)
        self.layout_frame_figure.addWidget(self.toolbar)
        self.layout_frame_figure.addWidget(self.canvas)
        # self.layout_frame_figure.addWidget(self.button)

        self.layout_main = QtWidgets.QHBoxLayout(self)
        self.layout_main.addWidget(self.frame_remPanel)
        self.layout_main.addWidget(self.frame_figure)

        self.Thread_instance = serial_485_stream(mainwindow=self)

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(serial_485_stream.data_figure, '*-')
        plt.yscale('log')
        plt.grid(which="major", linestyle="solid", color="black", linewidth=0.5)
        plt.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
        self.canvas.draw()

    def remove_file(self):
        if os.path.isfile(f'{serial_485_stream.xl_wr.file_name}.xlsx'):
            os.remove(f'{serial_485_stream.xl_wr.file_name}.xlsx')
            print("File delete success")
        else:    
            print("File doesn't exists!")
    
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Вы нажали на крестик', "Вы уверены, что хотите уйти?",
                                                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            df = pandas.read_excel(f'{serial_485_stream.xl_wr.file_name}.xlsx')
            if df.empty:
                self.remove_file()
            event.accept()
        else:
            event.ignore()

    def start_485_stream(self):
        serial_485_stream.flag_state = True
        self.Thread_instance.start() 

    def stop_485_stream(self):
        serial_485_stream.flag_state = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_win = myWindow()
    my_win.show()
    sys.exit(app.exec_())
