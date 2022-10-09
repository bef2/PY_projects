import sys, time
from serial import Serial
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, Qt


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
    
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow

        self.ser_group = {'ser_x': Serial(), 'ser_y': Serial(), 'ser_z': Serial()}
        self.init_port(self.ser_group['ser_x'], 'COM4')
        self.init_port(self.ser_group['ser_y'], 'COM15')
        self.init_port(self.ser_group['ser_z'], 'COM11')

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

        print()
        print('Время торможения: ', self.brake_time)
        print('Тормозной путь: ', self.brake_path)

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


    def read_panel(self, axis):
        self.max_speed = int(self.mainwindow.var['line_velocity_' + axis].text())
        self.acceleration = self.max_speed # Такое же как скорость
        self.steps = int(self.mainwindow.var['line_steps_' + axis].text())
        self.min_speed = 10

        self.commands = {'direction': None, 'accel': f'AL+{self.acceleration}*', 'speed': f'SD{self.max_speed}*',
                        'steps': f'MV{self.steps}*'}
        
        if self.mainwindow.flags['direction_' + axis]:
            self.commands['direction'] = 'DR*'
        else:
            self.commands['direction'] = 'DL*'

        if int(self.mainwindow.var['line_velocity_' + axis].text()) > 800:
            self.commands['accel'] = 'AL800*'

        self.brake_time = ((self.max_speed - self.min_speed) / self.acceleration)
        self.brake_path = round(self.acceleration * (self.brake_time ** 2) / 2)

        if self.steps < (self.brake_path * 2):
            self.brake_path = round(self.steps / 2)


    def loop_exe(self, axis):
        # report = ''
        try:
            report = self.ser_group['ser_' + axis].read(128).decode()
            # self.check_E14 = False

            if (report.find('E14') > -1 or self.data_in.find('E14') > -1) and self.mainwindow.flags['btn_start_lock_' + axis]:
            # if command.find('E14') > -1 or self.data_in.find('E14') > -1:
                # self.check_E14 = True
                self.mainwindow.flags['btn_start_lock_' + axis] = False
                self.mainwindow.flags['btn_stop_lock_' + axis] = True
                self.mainwindow.var['button_start_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')
                self.mainwindow.var['button_stop_' + axis].setStyleSheet(f'background: rgb{BTN_STOP};')
        except Exception:
            time.sleep(0.1)

        if self.mainwindow.flags['moving_' + axis]:
            self.mainwindow.flags['btn_start_lock_' + axis] = True
            self.read_panel(axis)

            if int(self.commands['speed'][2:-1]) < 1 or int(self.commands['speed'][2:-1]) > 800:
                self.mainwindow.flags['moving_' + axis] = False
                self.mainwindow.flags['btn_start_lock_' + axis] = False
                self.mainwindow.flags['btn_stop_lock_' + axis] = True
                self.mainwindow.var['button_start_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')
                self.mainwindow.var['button_stop_' + axis].setStyleSheet(f'background: rgb{BTN_STOP};')
                
            else:
                self.serial_write(self.ser_group['ser_' + axis])
                # self.serial_read(self.ser_1)
                self.mainwindow.flags['moving_' + axis] = False

        if self.mainwindow.flags['move_stop_' + axis]:
            self.mainwindow.flags['btn_stop_lock_' + axis] = True
            self.ser_group['ser_' + axis].write('ST*'.encode())
            # time.sleep(0.02)
            # self.serial_read(self.ser_1)
            self.mainwindow.flags['move_stop_' + axis] = False

        # if self.check_E14:
        #     print('Поиск конца: ', self.check_E14)

    def run(self):
        time.sleep(1) # Ожидание загрузки интерфейса
        while self.mainwindow.flags['stream_state']:

            self.loop_exe('x')
            self.loop_exe('y')
            self.loop_exe('z')

        print('Выход')


class Main_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.var = {}
        self.flags = {}
        
        
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # Параметры основного окна
        self.setGeometry(250, 200, 885, 430)
        self.setMaximumSize(885, 430)
        self.setWindowTitle("Пульт управления контроллерами SMSD-4.2 по трём осям")

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        # Рамка статуса и настроек портов
        self.frame_status = QFrame(self)
        self.frame_status.setMinimumHeight(55)

        # Текст статуса
        self.label_status = QLabel('Ожидает', self.frame_status)
        self.frame_status.setFont(QFont('Arial', 10))
        self.frame_status.setStyleSheet(f'color: rgb{TEXT};')

        # Кнопка настроек портов
        self.button_ports = QPushButton('Порты')
        self.button_ports.setMaximumSize(120, 32)
        self.button_ports.setFont(QFont("Arial", 10))
        self.button_ports.clicked.connect(self.pushed_ports)

        # Сетка рамки статуса и настроек портов
        self.layout_status = QHBoxLayout(self.frame_status)
        self.layout_status.addWidget(self.label_status)
        self.layout_status.addWidget(self.button_ports)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        # Рамка настроек движения по осям
        self.frame_set_drive = QFrame(self) 

#------------------------------------------------------------------------------------------
        # Создание рамок по осям с входящими в неё виджетами
        self.init_axis('x')
        self.init_axis('y')
        self.init_axis('z')

#------------------------------------------------------------------------------------------
        # Сетка рамки настроек движения по осям
        self.layout_set_drive = QHBoxLayout(self.frame_set_drive)
        self.layout_set_drive.addWidget(self.var['frame_axis_x'])
        self.layout_set_drive.addWidget(self.var['frame_axis_y'])
        self.layout_set_drive.addWidget(self.var['frame_axis_z'])

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        # Сетка основного окна
        self.layout_window = QVBoxLayout(self)
        self.layout_window.addWidget(self.frame_status)
        self.layout_window.addWidget(self.frame_set_drive)
#//////////////////////////////////////////////////////////////////////////////////////////

        self.thread_serial = Serial_stream(mainwindow=self)
        self.start_stream()


    def init_axis(self, axis):

        # Рамка оси
        self.var['frame_axis_' + axis] = QFrame(self)
        self.var['frame_axis_' + axis].setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.var['frame_axis_' + axis].setLineWidth(2)

        # Надпись - имя оси
        self.var['label_axis_' + axis] = QLabel(f'{axis.upper()}', self.var['frame_axis_' + axis])
        self.var['label_axis_' + axis].setFont(QFont("Arial", 16))
        self.var['label_axis_' + axis].setStyleSheet(f"color: rgb{TEXT};")
        self.var['label_axis_' + axis].setAlignment(Qt.AlignHCenter)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

        # Рамка параметров движения
        self.var['frame_parameters_' + axis] = QFrame(self)
        self.var['frame_parameters_' + axis].setMinimumHeight(100)

#------------------------------------------------------------------------------------------

        # Рамка установки скорости
        self.var['frame_velocity_' + axis] = QFrame(self.var['frame_parameters_' + axis])

        # Надпись - Скорость
        self.var['label_velocity_' + axis] = QLabel('Скор.', self.var['frame_velocity_' + axis])
        self.var['label_velocity_' + axis].setFont(QFont("Arial", 12))
        self.var['label_velocity_' + axis].setStyleSheet(f"color: rgb{TEXT};")

        # Поле ввода: Скорость
        self.var['line_velocity_' + axis]= QLineEdit(self.var['frame_velocity_' + axis])
        self.var['line_velocity_' + axis].setMinimumHeight(35)
        self.var['line_velocity_' + axis].setFont(QFont("Arial", 12))
        self.var['line_velocity_' + axis].setText(f'{VELOCITY}')

        # Сетка рамки установки скорости
        self.var['layout_velocity_' + axis] = QVBoxLayout(self.var['frame_velocity_' + axis])
        self.var['layout_velocity_' + axis].addWidget(self.var['label_velocity_' + axis])
        self.var['layout_velocity_' + axis].addWidget(self.var['line_velocity_' + axis])

#------------------------------------------------------------------------------------------

        # Рамка установки шагов
        self.var['frame_steps_' + axis] = QFrame(self.var['frame_parameters_' + axis])

        # Надпись - Шаги
        self.var['label_steps_' + axis] = QLabel('Шаги', self.var['frame_steps_' + axis])
        self.var['label_steps_' + axis].setFont(QFont("Arial", 12))
        self.var['label_steps_' + axis].setStyleSheet(f"color: rgb{TEXT};")

        # Поле ввода: Шаги
        self.var['line_steps_' + axis] = QLineEdit(self.var['frame_steps_' + axis])
        self.var['line_steps_' + axis].setMinimumHeight(35)
        self.var['line_steps_' + axis].setFont(QFont("Arial", 12))
        self.var['line_steps_' + axis].setText(f'{STEPS}')

        # Сетка рамки установки шагов
        self.var['layout_steps_' + axis] = QVBoxLayout(self.var['frame_steps_' + axis])
        self.var['layout_steps_' + axis].addWidget(self.var['label_steps_' + axis])
        self.var['layout_steps_' + axis].addWidget(self.var['line_steps_' + axis])

#------------------------------------------------------------------------------------------

        # Сетка рамки параметров движения
        self.var['layout_parameters_' + axis] = QHBoxLayout(self.var['frame_parameters_' + axis])
        self.var['layout_parameters_' + axis].addWidget(self.var['frame_velocity_' + axis])
        self.var['layout_parameters_' + axis].addWidget(self.var['frame_steps_' + axis])

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

        # Рамка выбора направления движения
        self.var['frame_direction_' + axis] = QFrame(self)

        # Кнопки выбора направления движения
        self.var['button_back_' + axis] = QPushButton('Назад')
        self.var['button_back_' + axis].setMinimumHeight(50)
        self.var['button_back_' + axis].setFont(QFont("Arial", 12))
        self.var['button_back_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.var['button_back_' + axis].clicked.connect(lambda: self.pushed_back(axis))

        self.var['button_forward_' + axis] = QPushButton('Вперед')
        self.var['button_forward_' + axis].setMinimumHeight(50)
        self.var['button_forward_' + axis].setFont(QFont("Arial", 12))
        self.var['button_forward_' + axis].setStyleSheet(f'background: rgb{BTN_DIRECTION};')
        self.var['button_forward_' + axis].clicked.connect(lambda: self.pushed_forward(axis))
        self.flags['direction_' + axis] = True

        # Сетка рамки выбора направления движения
        self.var['layout_direction_' + axis] = QHBoxLayout(self.var['frame_direction_' + axis])
        self.var['layout_direction_' + axis].addWidget(self.var['button_back_' + axis])
        self.var['layout_direction_' + axis].addWidget(self.var['button_forward_' + axis])

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

        # Рамка пуска останова
        self.var['frame_launch_' + axis] = QFrame(self)

        # Кнопки пуска останова
        self.var['button_start_' + axis] = QPushButton('СТАРТ')
        self.var['button_start_' + axis].setMinimumHeight(50)
        self.var['button_start_' + axis].setFont(QFont("Arial", 12))
        self.var['button_start_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.var['button_start_' + axis].clicked.connect(lambda: self.pushed_start(axis))
        self.flags['moving_' + axis] = False
        self.flags['btn_start_lock_' + axis] = False

        self.var['button_stop_' + axis] = QPushButton('СТОП')
        self.var['button_stop_' + axis].setMinimumHeight(50)
        self.var['button_stop_' + axis].setFont(QFont("Arial", 12))
        self.var['button_stop_' + axis].setStyleSheet(f'background: rgb{BTN_STOP};')
        self.var['button_stop_' + axis].clicked.connect(lambda: self.pushed_stop(axis))
        self.flags['move_stop_' + axis] = False
        self.flags['btn_stop_lock_' + axis] = True

        # Сетка рамки пуска останова
        self.var['layout_launch_' + axis] = QHBoxLayout(self.var['frame_launch_' + axis])
        self.var['layout_launch_' + axis].addWidget(self.var['button_start_' + axis])
        self.var['layout_launch_' + axis].addWidget(self.var['button_stop_' + axis])
        
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

        # Сетка рамки оси
        self.var['layout_axis_' + axis] = QVBoxLayout(self.var['frame_axis_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['label_axis_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['frame_parameters_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['frame_direction_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['frame_launch_' + axis])


    def start_stream(self):
        self.flags['stream_state'] = True
        self.thread_serial.start()
        

    def stop_stream(self):
        self.flags['stream_state'] = False


    def pushed_ports(self):
        self.child_win = Child_window()
        self.child_win.show()


    def pushed_back(self, axis):
        self.flags['direction_' + axis] = False
        self.var['button_forward_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.var['button_back_' + axis].setStyleSheet(f'background: rgb{BTN_DIRECTION};')


    def pushed_forward(self, axis):
        self.flags['direction_' + axis] = True
        self.var['button_forward_' + axis].setStyleSheet(f'background: rgb{BTN_DIRECTION};')
        self.var['button_back_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')


    def pushed_start(self, axis):
        if not self.flags['btn_start_lock_' + axis]:
            self.flags['moving_' + axis] = True
            self.flags['move_stop_' + axis] = False
            self.flags['btn_stop_lock_' + axis] = False
        self.var['button_start_' + axis].setStyleSheet(f'background: rgb{BTN_START};')
        self.var['button_stop_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')

               
    def pushed_stop(self, axis):
        if not self.flags['btn_stop_lock_' + axis]:
            self.flags['move_stop_' + axis] = True
            self.flags['moving_' + axis] = False
            self.flags['btn_start_lock_' + axis] = False
        self.var['button_start_' + axis].setStyleSheet(f'background: rgb{BTN_UNPUSH};')
        self.var['button_stop_' + axis].setStyleSheet(f'background: rgb{BTN_STOP};')


class Child_window(QWidget):
    def __init__(self):
        super().__init__()

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # Параметры основного окна
        self.setGeometry(200, 245, 885, 430)
        self.setMaximumSize(885, 430)
        self.setWindowTitle("Настройки портов")

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        # Рамка настроек порта
        self.frame_settings = QFrame(self)

#------------------------------------------------------------------------------------------
        # рамка скорости передачи данных
        self.frame_baudrate = QFrame(self.frame_settings)
        
        # Надпись скорости передачи данных
        self.label_baudrate = QLabel('Бит/с', self.frame_baudrate)
        self.label_baudrate.setFont(QFont("Arial", 12))
        self.label_baudrate.setStyleSheet(f"color: rgb{TEXT};")

        # Ввод скорости передачи данных
        self.line_baudrate = QLineEdit(self.frame_baudrate)

        # Сетка рамки скорости передачи данных
        self.layout_baudrate = QHBoxLayout(self.frame_baudrate)
        self.layout_baudrate.addWidget(self.label_baudrate)
        self.layout_baudrate.addWidget(self.line_baudrate)

#------------------------------------------------------------------------------------------
        # рамка - биты данных
        self.frame_bytesize = QFrame(self.frame_settings)
        
        # Надпись биты данных
        self.label_bytesize = QLabel('Биты данных', self.frame_bytesize)
        self.label_bytesize.setFont(QFont("Arial", 12))
        self.label_bytesize.setStyleSheet(f"color: rgb{TEXT};")

        # Ввод - биты данных
        self.line_bytesize = QLineEdit(self.frame_bytesize)

        # Сетка рамки - биты данных
        self.layout_bytesize = QHBoxLayout(self.frame_bytesize)
        self.layout_bytesize.addWidget(self.label_bytesize)
        self.layout_bytesize.addWidget(self.line_bytesize)

#------------------------------------------------------------------------------------------
        # Сетка рамки настроек порта
        self.layout_1 = QVBoxLayout(self.frame_settings)
        self.layout_1.addWidget(self.frame_baudrate)
        self.layout_1.addWidget(self.frame_bytesize)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        self.frame_opens = QFrame(self)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        self.layout_main = QHBoxLayout(self)
        self.layout_main.addWidget(self.frame_settings)
        self.layout_main.addWidget(self.frame_opens)
#//////////////////////////////////////////////////////////////////////////////////////////



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = Main_window()
    main_win.show()
    sys.exit(app.exec())
