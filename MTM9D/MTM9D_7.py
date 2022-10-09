import sys, os, time, serial, pandas, openpyxl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class excelWriter:
    path = 'C:\Манометр MTM9D\Таблицы давления'
    try:
        os.mkdir('C:\Манометр MTM9D')                
        os.mkdir('C:\Манометр MTM9D\Таблицы давления')                
    except Exception:
        try:
            os.mkdir('C:\Манометр MTM9D\Таблицы давления')
        except Exception:
            pass
        pass
    
    def __init__(self):
        self.file_name = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[:10].replace('-', '.') + '_' + \
                         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[11:].replace(':', '.') + '_MTM9D'
        writer = pandas.ExcelWriter(self.path + f'\{self.file_name}.xlsx')
        writer.save()

        self.excel_file = openpyxl.load_workbook(self.path + f'\{self.file_name}.xlsx')
        self.excel_sheet = self.excel_file['Sheet1']
        self.excel_sheet[f'A1'] = '№'
        self.excel_sheet[f'B1'] = 'Дата'
        self.excel_sheet[f'C1'] = 'Время'
        self.excel_sheet[f'D1'] = 'Ед.Изм.'
        self.excel_sheet[f'E1'] = 'Приб.1'
        self.excel_sheet[f'F1'] = 'Приб.2'
        self.excel_sheet[f'G1'] = 'Приб.3'


    def write(self,row, line_data):
        self.excel_sheet[f'A{row}'] = line_data['num_pack']
        self.excel_sheet[f'B{row}'] = line_data['date']
        self.excel_sheet[f'C{row}'] = line_data['time']
        self.excel_sheet[f'D{row}'] = line_data['unit']
        self.excel_sheet[f'E{row}'] = line_data['values_1']
        self.excel_sheet[f'F{row}'] = line_data['values_2']
        self.excel_sheet[f'G{row}'] = line_data['values_3']

        self.excel_file.save(self.path + f'\{self.file_name}.xlsx')


class search_COM(QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        try:
            list_ports = self.mainwindow.serial_ports()
            while True:
                new_ports = self.mainwindow.serial_ports()
                if new_ports != list_ports:
                    list_ports = new_ports
                    self.mainwindow.combobox_setCOM.clear()
                    self.mainwindow.combobox_setCOM.addItems(self.mainwindow.serial_ports())
                    if self.mainwindow.combobox_setCOM.count() == 0:
                        self.mainwindow.combobox_setCOM.addItem(self.mainwindow.name_COM)
                time.sleep(1)
        except Exception:
            pass


class serial_485_stream(QThread):
    flag_state = False
    number_packet = 1
    row = 2

    try:
        xl_wr = excelWriter()
    except Exception:
        time.sleep(0.5)
        try:
            xl_wr = excelWriter()
        except Exception:
            pass
        pass

    data_figure = []
    # time_list = []
    interval = 1
    # count_error = 0
    dataIn = {'adr1': '', 'adr2': '', 'adr3': ''}
    data_formatted = {'adr1': '', 'adr2': '', 'adr3': ''}

    ser = serial.Serial()
    ser.baudrate = 9600 # Бит в секунду
    ser.bytesize = 8    # Биты данных = 8
    ser.parity   = 'N'  # Нет четности
    ser.stopbits = 1    # Стоповые биты = 1
    ser.timeout = 0.1   # Время ожидания данных чтения

    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
        
    def run(self):
        if self.flag_state:
            self.mainwindow.label_stat_1.setStyleSheet("color: rgb(0, 210, 0);")
            self.mainwindow.label_stat_1.setText("Запущено")

        while self.flag_state:
            for i in range(1, 4):
                send_command = f"00{i}M^\r"    # Команда: Чтение измерения давления
                try:
                    self.ser.write(send_command.encode())
                    self.dataIn[f'adr{i}'] = self.ser.read(12).decode()
                except Exception:
                    self.mainwindow.label_stat_2.setStyleSheet("color: rgb(255, 0, 0);")
                    self.mainwindow.label_stat_2.setText(f"Связь потеряна")
                    time.sleep(1)
                    try:
                        self.ser.port = self.mainwindow.name_COM
                        self.ser.open()
                        if self.ser.isOpen():
                            self.mainwindow.label_stat_2.setStyleSheet("color: rgb(0, 0, 0);")
                            self.mainwindow.label_stat_2.setText("Чтение измерения давления " + serial_485_stream.ser.port)
                    except Exception:
                        # self.count_error += 1
                        self.mainwindow.label_digit.setText("-0")
                        self.mainwindow.label_stat_3.setText(f"")
                    continue
                
                # FIXME
                if self.dataIn[f'adr{i}'] == '':
                    self.mainwindow.label_stat_2.setText("")
                    self.mainwindow.label_stat_3.setText("")
                    self.mainwindow.label_digit.setText("-0")
                    continue
            
                try:
                    self.data_formatted[f'adr{i}'] = f"{int(self.dataIn[f'adr{i}'][4:8]) * 1 / 10 ** (23 - int(self.dataIn[f'adr{i}'][8:10]))}"
                except Exception:
                    pass

            self.mainwindow.label_digit.setText(self.data_formatted['adr1'])

            try:
                line_data = {'num_pack': self.number_packet,
                            'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[:11],
                            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())[11:],
                            'unit': self.mainwindow.label_unit.text(),
                            'values_1': self.data_formatted['adr1'],
                            'values_2': self.data_formatted['adr2'],
                            'values_3': self.data_formatted['adr3'],}

                self.mainwindow.label_stat_3.setText(f"Измерение: {line_data['num_pack']}, {line_data['date']}, {line_data['time']}")

                self.xl_wr.write(self.row, line_data)

                self.data_figure.append(float(line_data['values_1']))
                if len(self.data_figure) > 60: self.data_figure.pop(0)
                # self.time_list.append(line_data['time'])
                # if len(self.time_list) > 60: self.time_list.pop(0)
                self.mainwindow.plot()
            except Exception:
                time.sleep(0.5)
                continue

            self.row += 1
            self.number_packet += 1
            k = 0
            while k < self.interval:
                if self.flag_state == False:
                    break
                k += 1
                time.sleep(1)
            
        self.mainwindow.label_stat_1.setStyleSheet("color: rgb(255, 0, 0);")
        self.mainwindow.label_stat_1.setText(f"Остановлено")


class myWindow(QtWidgets.QWidget):
    count_openCOM = 0
    count_serial_ports = 0
    name_COM = ''

    def __init__(self):
        super().__init__()

        self.resize(1200, 540)
        self.setMinimumSize(QtCore.QSize(550, 540))
        self.setWindowTitle("Манометр MTM9D")
        
        self.frame_remPanel = QtWidgets.QFrame(self)
        self.frame_remPanel.setMinimumWidth(520)
        self.frame_remPanel.setMaximumWidth(520)

        self.frame_preset = QtWidgets.QFrame(self.frame_remPanel)
        self.frame_preset.setMaximumHeight(100)

        self.frame_status = QtWidgets.QFrame(self.frame_preset)

        self.label_stat_1 = QtWidgets.QLabel(self.frame_status)
        self.label_stat_1.setText("COM порт закрыт")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_1.setFont(font)
        
        self.label_stat_2 = QtWidgets.QLabel(self.frame_status)
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_2.setFont(font)

        self.label_stat_3 = QtWidgets.QLabel(self.frame_status)
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_stat_3.setFont(font)

        self.layout_frame_status = QtWidgets.QVBoxLayout(self.frame_status)
        self.layout_frame_status.addWidget(self.label_stat_1)
        self.layout_frame_status.addWidget(self.label_stat_2)
        self.layout_frame_status.addWidget(self.label_stat_3)
        self.layout_frame_status.setContentsMargins(0,0,0,0)

        self.frame_settings = QtWidgets.QFrame(self.frame_preset)
        self.frame_settings.setMaximumWidth(160)

        self.frame_setCOM = QtWidgets.QFrame(self.frame_settings)

        self.combobox_setCOM = QtWidgets.QComboBox(self.frame_setCOM)
        self.combobox_setCOM.addItems(self.serial_ports())

        self.button_setCOM = QtWidgets.QPushButton(self.frame_setCOM)
        self.button_setCOM.setText("Открыть")
        self.button_setCOM.setMaximumWidth(82)
        font.setFamily("Arial")
        font.setPointSize(8)
        self.button_setCOM.setFont(font)
        self.button_setCOM.clicked.connect(self.openCOM)

        self.layout_frame_setCOM = QtWidgets.QHBoxLayout(self.frame_setCOM)
        self.layout_frame_setCOM.addWidget(self.combobox_setCOM)
        self.layout_frame_setCOM.addWidget(self.button_setCOM)
        self.layout_frame_setCOM.setContentsMargins(0,0,0,0)

        self.frame_setInterval = QtWidgets.QFrame(self.frame_settings)

        self.combobox_setInterval = QtWidgets.QComboBox(self.frame_setInterval)
        self.combobox_setInterval.addItems(['1', '5', '10', '30', '60', '120', '300'])

        self.button_setInterval = QtWidgets.QPushButton(self.frame_setInterval)
        self.button_setInterval.setText("Задать")
        self.button_setInterval.setMaximumWidth(82)
        font.setFamily("Arial")
        font.setPointSize(8)
        self.button_setInterval.setFont(font)
        self.button_setInterval.clicked.connect(self.set_interval)

        self.layout_frame_setInterval = QtWidgets.QHBoxLayout(self.frame_setInterval)
        self.layout_frame_setInterval.addWidget(self.combobox_setInterval)
        self.layout_frame_setInterval.addWidget(self.button_setInterval)
        self.layout_frame_setInterval.setContentsMargins(0,0,0,0)

        self.label_setCOM = QtWidgets.QLabel(self.frame_settings)
        self.label_setCOM.setText("Порт")
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_setCOM.setFont(font)

        self.label_setInterval = QtWidgets.QLabel(self.frame_settings)
        self.label_setInterval.setText("Интервал, с")
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_setInterval.setFont(font)

        self.layout_frame_settings = QtWidgets.QVBoxLayout(self.frame_settings)
        self.layout_frame_settings.addWidget(self.label_setCOM)
        self.layout_frame_settings.addWidget(self.frame_setCOM)
        self.layout_frame_settings.addWidget(self.label_setInterval)
        self.layout_frame_settings.addWidget(self.frame_setInterval)
        self.layout_frame_settings.setContentsMargins(0,0,0,0)

        self.layout_frame_preset = QtWidgets.QHBoxLayout(self.frame_preset)
        self.layout_frame_preset.addWidget(self.frame_status)
        self.layout_frame_preset.addWidget(self.frame_settings)
        self.layout_frame_preset.setContentsMargins(0,0,0,0)


        self.frame_value = QtWidgets.QFrame(self.frame_remPanel)
        self.frame_value.setMaximumHeight(300)

        self.label_digit = QtWidgets.QLabel(self.frame_value)
        self.label_digit.setText("-0")
        font.setFamily("Arial")
        font.setPointSize(100)
        self.label_digit.setFont(font)
        self.label_digit.setStyleSheet("color: rgb(85, 170, 255);")
        self.label_digit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        

        self.label_unit = QtWidgets.QLabel(self.frame_value)
        self.label_unit.setText("mbar")
        font.setFamily("Arial")
        font.setPointSize(54)
        self.label_unit.setFont(font)
        self.label_unit.setStyleSheet("color: rgb(180, 180, 180);")
        self.label_unit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)

        self.layout_frame_value = QtWidgets.QVBoxLayout(self.frame_value)
        self.layout_frame_value.addWidget(self.label_unit)
        self.layout_frame_value.addWidget(self.label_digit)


        self.frame_buttons = QtWidgets.QFrame(self.frame_remPanel)
        self.frame_buttons.setMinimumHeight(40)
        self.frame_buttons.setMaximumHeight(40)

        self.button_start = QtWidgets.QPushButton(self.frame_buttons)
        self.button_start.setMaximumSize(QtCore.QSize(150, 40))
        self.button_start.setText("Старт")
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setWeight(50)
        self.button_start.setFont(font)
        self.button_start.clicked.connect(self.start_485_stream)

        self.button_stop = QtWidgets.QPushButton(self.frame_buttons)
        self.button_stop.setMaximumSize(QtCore.QSize(150, 40))
        self.button_stop.setText("Стоп")
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setWeight(50)
        self.button_stop.setFont(font)
        self.button_stop.clicked.connect(self.stop_485_stream)

        self.layout_buttons = QtWidgets.QHBoxLayout(self.frame_buttons)
        self.layout_buttons.addWidget(self.button_start)
        self.layout_buttons.addWidget(self.button_stop)
        self.layout_buttons.setContentsMargins(0,0,0,0)

        self.label_creator = QtWidgets.QLabel(self.frame_remPanel)
        self.label_creator.setText("Разработал Ефименко Б.О.")
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_creator.setFont(font)
        self.label_creator.setStyleSheet("color: rgb(180, 180, 180);")
        self.label_creator.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)

        self.layout_frame_remPanel = QtWidgets.QVBoxLayout(self.frame_remPanel)
        self.layout_frame_remPanel.addWidget(self.frame_preset)
        self.layout_frame_remPanel.addWidget(self.frame_value)
        self.layout_frame_remPanel.addWidget(self.frame_buttons)
        self.layout_frame_remPanel.addWidget(self.label_creator)
        self.layout_frame_remPanel.setContentsMargins(0,0,0,0)

        # self.frame_figure = QtWidgets.QFrame(self)

        self.figure = plt.figure()
        self.figure.add_subplot(111)
        plt.title("График измерения давления")
        # plt.xlabel("Время, с")
        plt.ylabel("Давление, mbar")
        plt.yscale('log')
        plt.grid(which="major", linestyle="solid", color="black", linewidth=0.5)
        plt.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
        self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, self)

        # self.Layout_frame_figure = QtWidgets.QVBoxLayout(self.frame_figure)
        # self.Layout_frame_figure.addWidget(self.toolbar)
        # self.Layout_frame_figure.addWidget(self.canvas)

        self.layout_main = QtWidgets.QHBoxLayout(self)
        self.layout_main.addWidget(self.frame_remPanel)
        # self.layout_main.addWidget(self.frame_figure)
        self.layout_main.addWidget(self.canvas)

        self.Thread_serial = serial_485_stream(mainwindow=self)
        self.Thread_searchCOM = search_COM(mainwindow=self)
        self.Thread_searchCOM.start()

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # ax.set_xticklabels(serial_485_stream.time_list, rotation=45)
        ax.plot(serial_485_stream.data_figure, color="red", linewidth=1)
        # ax.plot(serial_485_stream.time_list, serial_485_stream.data_figure, color="red", linewidth=1)
        plt.title("График измерения давления")
        # plt.xlabel("Время, с")
        plt.ylabel("Давление, mbar")
        plt.yscale('log')
        plt.grid(which="major", linestyle="solid", color="black", linewidth=0.5)
        plt.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
        self.canvas.draw()

    def remove_file(self):
        if os.path.isfile(excelWriter.path + f'\{serial_485_stream.xl_wr.file_name}.xlsx'):
            os.remove(excelWriter.path + f'\{serial_485_stream.xl_wr.file_name}.xlsx')
            print("Файл удален успешно")
        else:    
            print("Файл не существует!")
    
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Подтвеждение выхода', "Завершить работу приложения?",
                                                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            df = pandas.read_excel(excelWriter.path + f'\{serial_485_stream.xl_wr.file_name}.xlsx')
            if df.empty:
                self.remove_file()
            event.accept()
        else:
            event.ignore()

    def start_485_stream(self):
        if serial_485_stream.ser.isOpen():
            serial_485_stream.flag_state = True
            self.label_stat_2.setStyleSheet("color: rgb(0, 0, 0);")
            self.label_stat_2.setText("Чтение измерения давления " + serial_485_stream.ser.port)
            self.Thread_serial.start()
        else:
            self.label_stat_2.setText("Необходимо открыть COM порт")

    def stop_485_stream(self):
        serial_485_stream.flag_state = False
    
    def serial_ports(self): 
        ports = ['COM%s' % (i + 1) for i in range(128)]
        result = []

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        result.reverse()
        return result

    def openCOM(self):
        self.count_openCOM += 1
        serial_485_stream.flag_state = False
        self.name_COM = self.combobox_setCOM.currentText()
        serial_485_stream.ser.port = self.name_COM
        try:
            serial_485_stream.ser.close()
            serial_485_stream.ser.open()
            if serial_485_stream.ser.isOpen():
                self.label_stat_1.setStyleSheet("color: rgb(0, 0, 0);")
                self.label_stat_1.setText(self.combobox_setCOM.currentText() + " открыт")
                self.label_stat_2.setText("")
        except Exception:
            print("Неудалось открыть порт, попытка:", self.count_openCOM)
            time.sleep(0.5)
            if self.count_openCOM < 4:
                self.openCOM()

    def set_interval(self):
        serial_485_stream.interval = int(self.combobox_setInterval.currentText())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_win = myWindow()
    my_win.show()
    sys.exit(app.exec_())
