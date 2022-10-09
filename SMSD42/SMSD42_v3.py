from cmath import sqrt
import serial, sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread


# Параметры движения
VELOCITY = 400
STEPS = 400
ACCELERATION = 400

# Цвета интерфейса
BTN_STOP = (254, 30, 30)
BTN_START = (30, 254, 30)
BTN_DIRECTION = (254, 225, 0)
BTN_UNPUSH = (210, 210, 210)
TEXT = (80, 80, 80)


class Serial_stream(QThread):
    
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
        self.ser_1 = serial.Serial()
        self.init_port(self.ser_1, 'COM4')
        self.commands = {}
        self.data_out = []
        self.data_in = ''
        self.check_E14 = False
        self.steps = 0
        self.max_speed = 0
        self.min_speed = 0
        self.acceleration = 0
        self.brake_path = 0
        self.brake_time = 0


    def init_port(self, serial_name, port_name):
        serial_name.baudrate = 9600 # Бит в секунду
        serial_name.bytesize = 8    # Биты данных = 8
        serial_name.parity   = 'E'  # Нет четности
        serial_name.stopbits = 1    # Стоповые биты = 1
        serial_name.timeout = 0.1   # Время ожидания данных чтения
        serial_name.writeTimeout = 0.1
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

        if int(self.commands['steps'][2:-1]) <= 50:
            self.data_out = ['LD*', 'BG*', self.commands['direction'],
                            f'SS{self.min_speed}*', self.commands['accel'], self.commands['speed'], self.commands['steps'],
                            'ED*', 'EN*', 'ST*']
        else:
            self.data_out = ['LD*', 'BG*', self.commands['direction'],
                            f'SS{self.min_speed}*', self.commands['accel'], self.commands['speed'], f'MV' + str(int(self.commands['steps'][2:-1]) - self.brake_path) + '*',
                            self.commands['accel'].replace('+', '-'), f'SD10*', f'MV{self.brake_path}*',
                            'ED*', 'EN*', 'ST*']

        # print()
        # print('Время торможения: ', self.brake_time)
        # print('Тормозной путь: ', self.brake_path)

        try:
            # print('Начинаю запись')
            for item in self.data_out:
                serial_name.write(item.encode())
                time.sleep(0.05)
            # print('Запись прошла: ', *self.data_out)
        except Exception:
            print('Ошибка при записи', serial_name.port)


    def serial_read(self, serial_name):
        try:
            print('Начинаю чтение')
            self.data_in = serial_name.read(128).decode()
            print('Чтение прошло: ', self.data_in.replace('*', '* '))
        except Exception:
            print('Ошибка при чтении', serial_name.port)


    def read_panel(self):
        self.max_speed = int(self.mainwindow.line_velocity.text())
        self.acceleration = self.max_speed # Такое же как скорость
        self.steps = int(self.mainwindow.line_steps.text())
        self.min_speed = 10

        self.commands = {'direction': None, 'accel': f'AL+{self.acceleration}*', 'speed': f'SD{self.max_speed}*',
                        'steps': f'MV{self.steps}*'}
        
        if self.mainwindow.direction:
            self.commands['direction'] = 'DR*'
        else:
            self.commands['direction'] = 'DL*'

        if int(self.mainwindow.line_velocity.text()) > 800:
            self.commands['accel'] = 'AL800*'

        self.brake_time = ((self.max_speed - self.min_speed) / self.acceleration)
        self.brake_path = round(self.acceleration * (self.brake_time ** 2) / 2)

        if self.steps < (self.brake_path * 2):
            self.brake_path = round(self.steps / 2)


    def run(self):
        report = ''
        time.sleep(1) # Ожидание загрузки интерфейса
        while self.mainwindow.stream_state:

            report = self.ser_1.read(128).decode()
            self.check_E14 = False

            if (report.find('E14') > -1 or self.data_in.find('E14') > -1) and self.mainwindow.btn_start_lock:
            # if command.find('E14') > -1 or self.data_in.find('E14') > -1:
                self.check_E14 = True
                self.mainwindow.btn_start_lock = False
                self.mainwindow.btn_stop_lock = True
                self.mainwindow.button_start.setStyleSheet(f'background: rgb{BTN_UNPUSH};')
                self.mainwindow.button_stop.setStyleSheet(f'background: rgb{BTN_STOP};')

            if self.mainwindow.moving:
                self.mainwindow.btn_start_lock = True
                self.read_panel()

                if int(self.commands['speed'][2:-1]) < 1 or int(self.commands['speed'][2:-1]) > 800:
                    self.mainwindow.moving = False
                    self.mainwindow.btn_start_lock = False
                    self.mainwindow.btn_stop_lock = True
                    self.mainwindow.button_start.setStyleSheet(f'background: rgb{BTN_UNPUSH};')
                    self.mainwindow.button_stop.setStyleSheet(f'background: rgb{BTN_STOP};')
                    
                else:
                    self.serial_write(self.ser_1)
                    # self.serial_read(self.ser_1)
                    self.mainwindow.moving = False

            if self.mainwindow.move_stop:
                self.mainwindow.btn_stop_lock = True
                self.ser_1.write('ST*'.encode())
                # time.sleep(0.02)
                # self.serial_read(self.ser_1)
                self.mainwindow.move_stop = False

            # if self.check_E14:
            #     print('Поиск конца: ', self.check_E14)

        print('Выход')


class myWindow(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.stream_state = False
        self.direction = True
        self.moving = False
        self.move_stop = False
        self.btn_start_lock = False
        self.btn_stop_lock = True
        

        # Параметры окна
        self.resize(350, 250)
        self.setMinimumSize(QtCore.QSize(350, 250))
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
        self.label_velocity.setStyleSheet(f"color: rgb{TEXT};")

        # Поле ввода: Скорость
        self.line_velocity = QtWidgets.QLineEdit(self.frame_velocity)
        self.line_velocity.setMinimumHeight(35)
        self.line_velocity.setFont(QtGui.QFont("Arial", 12))
        self.line_velocity.setText(f'{VELOCITY}')

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
        self.label_steps.setStyleSheet(f"color: rgb{TEXT};")

        # Поле ввода: Шаги
        self.line_steps = QtWidgets.QLineEdit(self.frame_steps)
        self.line_steps.setMinimumHeight(35)
        self.line_steps.setFont(QtGui.QFont("Arial", 12))
        self.line_steps.setText(f'{STEPS}')

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
        self.button_back.setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.button_back.clicked.connect(self.pushed_back)

        self.button_forvard = QtWidgets.QPushButton('Вперед')
        self.button_forvard.setMinimumHeight(50)
        self.button_forvard.setFont(QtGui.QFont("Arial", 12))
        self.button_forvard.setStyleSheet(f'background: rgb{BTN_DIRECTION};')
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
        self.button_start.setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.button_start.clicked.connect(self.pushed_start)

        self.button_stop = QtWidgets.QPushButton('СТОП')
        self.button_stop.setMinimumHeight(50)
        self.button_stop.setFont(QtGui.QFont("Arial", 12))
        self.button_stop.setStyleSheet(f'background: rgb{BTN_STOP};')
        self.button_stop.clicked.connect(self.pushed_stop)
        self.btn_stop_lock = True
        
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

        self.thread_serial = Serial_stream(mainwindow=self)
        self.start_stream()


    def start_stream(self):
        self.stream_state = True
        self.thread_serial.start()
        

    def stop_stream(self):
        self.stream_state = False


    def pushed_back(self):
        self.direction = False
        self.button_forvard.setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.button_back.setStyleSheet(f'background: rgb{BTN_DIRECTION};')


    def pushed_forvard(self):
        self.direction = True
        self.button_forvard.setStyleSheet(f'background: rgb{BTN_DIRECTION};')
        self.button_back.setStyleSheet(f'background: rgb{BTN_UNPUSH};')


    def pushed_start(self):
        if not self.btn_start_lock:
            self.moving = True
            self.move_stop = False
            self.btn_stop_lock = False
        self.button_start.setStyleSheet(f'background: rgb{BTN_START};')
        self.button_stop.setStyleSheet(f'background: rgb{BTN_UNPUSH};')

        
        
    def pushed_stop(self):
        if not self.btn_stop_lock:
            self.move_stop = True
            self.moving = False
            self.btn_start_lock = False
        self.button_start.setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.button_stop.setStyleSheet(f'background: rgb{BTN_STOP};')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_win = myWindow()
    my_win.show()
    sys.exit(app.exec())
