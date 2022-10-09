import serial, sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread



class Serial_stream(QThread):
    move = False
    
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
        self.ser_1 = serial.Serial()
        self.init_port(self.ser_1, 'COM4')
        self.commands = {}
        self.dataOut = []
        self.dataIn = ''


    def init_port(self, serial_name, port_name):
        serial_name.baudrate = 9600 # Бит в секунду
        serial_name.bytesize = 8    # Биты данных = 8
        serial_name.parity   = 'E'  # Нет четности
        serial_name.stopbits = 1    # Стоповые биты = 1
        serial_name.timeout = 0.1   # Время ожидания данных чтения
        # serial_name.writeTimeout = 0.2
        serial_name.port = port_name
        try:
            serial_name.open()
            if serial_name.isOpen():
                print('Порт', serial_name.port, 'открыт')
            else:
                print('Неудалось открыть порт', serial_name.port)
        except Exception:
            print('Ошибка при открытии порта', serial_name.port)


    def serial_write(self, serial_name):
        # self.dataOut = ['LD*', 'BG*', self.commands['direction'], 'AL+800*', 'SS50*',
        #                 self.commands['speed'], self.commands['steps'], 'ED*', 'EN*', 'ST*']
        self.dataOut = ['LD*', 'BG*', self.commands['direction'],
                        self.commands['speed'], self.commands['steps'], 'ED*', 'EN*', 'ST*']
        try:
            print('Начинаю запись')

            if self.move:
                for item in self.dataOut:
                    serial_name.write(item.encode())
                    time.sleep(0.05)
            else:
                self.ser_1.write('DS*'.encode())
                time.sleep(0.05)

            print('Запись прошла: ', *self.dataOut)
        except Exception:
            print('Ошибка при записи', serial_name.port)


    def serial_read(self, serial_name):
        try:
            print('Начинаю чтение')
            self.dataIn = serial_name.read(128).decode()
            print('Чтение прошло: ', self.dataIn.replace('*', '* '))
        except Exception:
            print('Ошибка при чтении', serial_name.port)


    def panel_read(self):
        self.commands = {'direction': None, 'speed': f'SD{self.mainwindow.line_velocity.text()}*', 'steps': f'MV{self.mainwindow.line_steps.text()}*'}
        if self.mainwindow.direction:
            self.commands['direction'] = 'DR*'
        else:
            self.commands['direction'] = 'DL*'


    def run(self):
        print()
        self.panel_read()
        self.serial_write(self.ser_1)
        self.serial_read(self.ser_1)
        print('Выход')


class myWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.strem_state = False
        self.direction = True

        # Параметры окна
        self.resize(500, 300)
        self.setMinimumSize(QtCore.QSize(500, 300))
        self.setWindowTitle("SMSD-4.2")

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        # Рамка параметров движения
        self.frame_parameters = QtWidgets.QFrame(self)

#------------------------------------------------------------------------------------------

        # Рамка установки скорости
        self.frame_velocity = QtWidgets.QFrame(self.frame_parameters)

        # Ярлык Скорость
        self.label_velocity = QtWidgets.QLabel('Скорость', self.frame_velocity)
        self.label_velocity.setFont(QtGui.QFont("Arial", 12))
        self.label_velocity.setStyleSheet("color: rgb(80, 80, 80);")

        # Поле ввода: Скорость
        self.line_velocity = QtWidgets.QLineEdit(self.frame_velocity)
        self.line_velocity.setMinimumHeight(35)
        self.line_velocity.setFont(QtGui.QFont("Arial", 12))
        self.line_velocity.setText('400')

        # Сетка рамки установки скорости
        self.layout_velocity = QtWidgets.QHBoxLayout(self.frame_velocity)
        self.layout_velocity.addWidget(self.label_velocity)
        self.layout_velocity.addWidget(self.line_velocity)

#------------------------------------------------------------------------------------------

        # Рамка установки шагов
        self.frame_steps = QtWidgets.QFrame(self.frame_parameters)

        # Ярлык: Шаги
        self.label_steps = QtWidgets.QLabel('Шаги', self.frame_steps)
        self.label_steps.setFont(QtGui.QFont("Arial", 12))
        self.label_steps.setStyleSheet("color: rgb(80, 80, 80);")

        # Поле ввода: Шаги
        self.line_steps = QtWidgets.QLineEdit(self.frame_steps)
        self.line_steps.setMinimumHeight(35)
        self.line_steps.setFont(QtGui.QFont("Arial", 12))
        self.line_steps.setText('1200')

        # Сетка рамки установки шагов
        self.layout_steps = QtWidgets.QHBoxLayout(self.frame_steps)
        self.layout_steps.addWidget(self.label_steps)
        self.layout_steps.addWidget(self.line_steps)

#------------------------------------------------------------------------------------------

        # Сетка рамки параметров движения
        self.layout_parameters = QtWidgets.QHBoxLayout(self.frame_parameters)
        self.layout_parameters.addWidget(self.frame_velocity)
        self.layout_parameters.addWidget(self.frame_steps)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

        # Рамка выбора направления движения
        self.frame_direction = QtWidgets.QFrame(self)

        # Кнопки выбора направления движения
        self.button_back = QtWidgets.QPushButton('Назад')
        self.button_back.setMinimumHeight(50)
        self.button_back.setFont(QtGui.QFont("Arial", 12))
        self.button_back.setStyleSheet('background: rgb(210,210,210);')
        self.button_back.clicked.connect(self.pushed_back)

        self.button_forvard = QtWidgets.QPushButton('Вперед')
        self.button_forvard.setMinimumHeight(50)
        self.button_forvard.setFont(QtGui.QFont("Arial", 12))
        self.button_forvard.setStyleSheet('background: rgb(254,225,0);')
        self.button_forvard.clicked.connect(self.pushed_forvard)

        # Сетка рамки выбора направления движения
        self.layout_direction = QtWidgets.QHBoxLayout(self.frame_direction)
        self.layout_direction.addWidget(self.button_back)
        self.layout_direction.addWidget(self.button_forvard)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

        # Рамка пуска останова
        self.frame_launch = QtWidgets.QFrame(self)

        # Кнопки пуска останова
        self.button_start = QtWidgets.QPushButton('СТАРТ')
        self.button_start.setMinimumHeight(50)
        self.button_start.setFont(QtGui.QFont("Arial", 12))
        self.button_start.setStyleSheet('background: rgb(210,210,210);')
        self.button_start.clicked.connect(self.pushed_start)

        self.button_stop = QtWidgets.QPushButton('СТОП')
        self.button_stop.setMinimumHeight(50)
        self.button_stop.setFont(QtGui.QFont("Arial", 12))
        self.button_stop.setStyleSheet('background: rgb(254,30,30);')
        self.button_stop.clicked.connect(self.pushed_stop)
        
        # Сетка рамки пуска останова
        self.layout_launch = QtWidgets.QHBoxLayout(self.frame_launch)
        self.layout_launch.addWidget(self.button_start)
        self.layout_launch.addWidget(self.button_stop)
        
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        
        # Сетка основного окна
        self.layout_window = QtWidgets.QVBoxLayout(self)
        self.layout_window.addWidget(self.frame_parameters)
        self.layout_window.addWidget(self.frame_direction)
        self.layout_window.addWidget(self.frame_launch)

#//////////////////////////////////////////////////////////////////////////////////////////

        self.Thread_serial = Serial_stream(mainwindow=self)


    def start_stream(self):
        self.stream_state = True
        self.Thread_serial.start()


    def stop_stream(self):
        self.stream_state = False


    def pushed_back(self):
        self.direction = False
        self.button_forvard.setStyleSheet('background: rgb(210,210,210);')
        self.button_back.setStyleSheet('background: rgb(254,225,0);')


    def pushed_forvard(self):
        self.direction = True
        self.button_forvard.setStyleSheet('background: rgb(254,225,0);')
        self.button_back.setStyleSheet('background: rgb(210,210,210);')


    def pushed_start(self):
        Serial_stream.move = True
        self.start_stream()
        self.button_start.setStyleSheet('background: rgb(30,254,30);')
        self.button_stop.setStyleSheet('background: rgb(210,210,210);')


    def pushed_stop(self):
        Serial_stream.move = False
        self.start_stream()
        self.button_start.setStyleSheet('background: rgb(210,210,210);')
        self.button_stop.setStyleSheet('background: rgb(254,30,30);')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_win = myWindow()
    my_win.show()
    sys.exit(app.exec())
