import sys, time
from serial import Serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLabel, QLineEdit, QPushButton,\
                            QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread


# Параметры движения
VELOCITY = 400
STEPS = 400
ACCELERATION = 400

# Цвета интерфейса
RED = (254, 30, 30)
GREEN = (30, 230, 30)
BLUE = (0, 0, 255)
YELLOW = (254, 225, 0)
GREY = (210, 210, 210)
DARK_GREY = (80, 80, 80)


class Serial_stream(QThread):
    
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.ser_group = {'ser_x': Serial(), 'ser_y': Serial(), 'ser_z': Serial()}
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


    def serial_write(self, serial_name):
        try:
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
        except Exception:
            time.sleep(0.1)
            print('Error creat commands')

        try:
            for item in self.data_out:
                serial_name.write(item.encode())
                time.sleep(0.05)
        except Exception:
            time.sleep(0.1)
            print('Error write', serial_name.port)


    def serial_read(self, serial_name):
        try:
            print('Начинаю чтение')
            self.data_in = serial_name.read(128).decode()
            print('Чтение прошло: ', self.data_in.replace('*', '* '))
        except Exception:
            print('Ошибка при чтении', serial_name.port)


    def read_panel(self, axis):
        try:
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
        except Exception:
            time.sleep(0.1)
            print('Error read panel')


    def loop_exe(self, axis):
        time.sleep(0.05)
        try:
            if self.mainwindow.flags['state_COM_' + axis]:
                report = self.ser_group['ser_' + axis].read(128).decode()
                if (report.find('E14') > -1 or self.data_in.find('E14') > -1) and self.mainwindow.flags['btn_start_lock_' + axis]:
                    print('boo')
                    self.mainwindow.flags['btn_start_lock_' + axis] = False
                    self.mainwindow.flags['btn_stop_lock_' + axis] = True
                    self.mainwindow.var['button_start_' + axis].setStyleSheet(f'background: rgb{GREY};')
                    self.mainwindow.var['button_stop_' + axis].setStyleSheet(f'background: rgb{RED};')
        except Exception:
            time.sleep(0.1)
            print('Error check E14')

        if self.mainwindow.flags['moving_' + axis]:
            self.mainwindow.flags['btn_start_lock_' + axis] = True
            self.read_panel(axis)
            if int(self.commands['speed'][2:-1]) < 1 or int(self.commands['speed'][2:-1]) > 800 or int(self.commands['steps'][2:-1]) < 1:
                self.mainwindow.flags['moving_' + axis] = False
                self.mainwindow.flags['btn_start_lock_' + axis] = False
                self.mainwindow.flags['btn_stop_lock_' + axis] = True
                self.mainwindow.var['button_start_' + axis].setStyleSheet(f'background: rgb{GREY};')
                self.mainwindow.var['button_stop_' + axis].setStyleSheet(f'background: rgb{RED};')    
            else:
                self.serial_write(self.ser_group['ser_' + axis])
                self.mainwindow.flags['moving_' + axis] = False

        if self.mainwindow.flags['move_stop_' + axis]:
            self.mainwindow.flags['btn_stop_lock_' + axis] = True
            self.ser_group['ser_' + axis].write('ST*'.encode())
            self.mainwindow.flags['move_stop_' + axis] = False


    def run(self):
        time.sleep(0.5) # Ожидание загрузки интерфейса
        while self.mainwindow.flags['stream_state']:
            self.loop_exe('x')
            self.loop_exe('y')
            self.loop_exe('z')


class Main_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.var = {'count_openCOM': 0, 'COM_opened': []}
        self.flags = {}
              
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # Параметры основного окна
        self.setGeometry(250, 200, 887, 393)
        self.setMaximumSize(887, 393)
        self.setWindowTitle("Пульт управления контроллерами SMSD-4.2 по трём осям")

#------------------------------------------------------------------------------------------
        self.label_family = QLabel('Разработал Ефименко Б.О.')
        self.label_family.setFont(QFont("Arial", 8))
        self.label_family.setStyleSheet(f"color: rgb{GREY};")

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
        self.layout_window.addWidget(self.frame_set_drive)
        self.layout_window.addWidget(self.label_family)
        self.layout_window.setSpacing(0)

#//////////////////////////////////////////////////////////////////////////////////////////

        self.thread_serial = Serial_stream(mainwindow=self)
        self.start_stream()
        

    def init_axis(self, axis):

        # Рамка оси
        self.var['frame_axis_' + axis] = QFrame()
        self.var['frame_axis_' + axis].setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.var['frame_axis_' + axis].setLineWidth(2)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
        # Рамка настройки порта
        self.var['frame_setCOM_' + axis] = QFrame()

        # Надпись - имя оси
        self.var['label_axis_' + axis] = QLabel(f'{axis.upper()}')
        self.var['label_axis_' + axis].setFont(QFont("Arial", 20))
        self.var['label_axis_' + axis].setStyleSheet(f"color: rgb{BLUE};")

        # Надпись - статус порта
        self.var['label_status_' + axis] = QLabel('\N{Large Red Circle}')
        self.var['label_status_' + axis].setFont(QFont("Arial", 10))
        self.var['label_status_' + axis].setStyleSheet(f"color: rgb{RED};")

        # Выпадающий список портов
        self.var['combobox_setCOM_' + axis] = QComboBox()
        self.var['combobox_setCOM_' + axis].addItems(self.serial_ports())
        self.var['name_COM' + axis] = ''

        # Кнопка - открыть порт
        self.var['button_setCOM_' + axis] = QPushButton('Открыть')
        self.var['button_setCOM_' + axis].setFont(QFont('Arial', 9))
        self.var['button_setCOM_' + axis].setMaximumWidth(74)
        self.var['button_setCOM_' + axis].setMaximumHeight(24)
        self.var['button_setCOM_' + axis].clicked.connect(lambda: self.openCOM(axis))
        self.flags['state_COM_' + axis] = False

        # Сетка рамки настройки порта
        self.var['layout_choice_port_' + axis] = QHBoxLayout(self.var['frame_setCOM_' + axis])
        self.var['layout_choice_port_' + axis].addWidget(self.var['label_axis_' + axis])
        self.var['layout_choice_port_' + axis].addWidget(self.var['label_status_' + axis])
        self.var['layout_choice_port_' + axis].addWidget(self.var['combobox_setCOM_' + axis])
        self.var['layout_choice_port_' + axis].addWidget(self.var['button_setCOM_' + axis])

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
        self.var['label_velocity_' + axis].setStyleSheet(f"color: rgb{DARK_GREY};")

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
        self.var['label_steps_' + axis].setStyleSheet(f"color: rgb{DARK_GREY};")

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
        self.var['button_back_' + axis].setStyleSheet(f'background: rgb{GREY};')
        self.var['button_back_' + axis].clicked.connect(lambda: self.pushed_back(axis))

        self.var['button_forward_' + axis] = QPushButton('Вперед')
        self.var['button_forward_' + axis].setMinimumHeight(50)
        self.var['button_forward_' + axis].setFont(QFont("Arial", 12))
        self.var['button_forward_' + axis].setStyleSheet(f'background: rgb{YELLOW};')
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
        self.var['button_start_' + axis].setStyleSheet(f'background: rgb{GREY};')
        self.var['button_start_' + axis].clicked.connect(lambda: self.pushed_start(axis))
        self.flags['moving_' + axis] = False
        self.flags['btn_start_lock_' + axis] = False

        self.var['button_stop_' + axis] = QPushButton('СТОП')
        self.var['button_stop_' + axis].setMinimumHeight(50)
        self.var['button_stop_' + axis].setFont(QFont("Arial", 12))
        self.var['button_stop_' + axis].setStyleSheet(f'background: rgb{RED};')
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
        self.var['layout_axis_' + axis].addWidget(self. var['frame_setCOM_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['frame_parameters_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['frame_direction_' + axis])
        self.var['layout_axis_' + axis].addWidget(self.var['frame_launch_' + axis])


    def start_stream(self):
        self.flags['stream_state'] = True
        self.thread_serial.start()
        

    def pushed_back(self, axis):
        self.flags['direction_' + axis] = False
        self.var['button_forward_' + axis].setStyleSheet(f'background: rgb{GREY};')
        self.var['button_back_' + axis].setStyleSheet(f'background: rgb{YELLOW};')


    def pushed_forward(self, axis):
        self.flags['direction_' + axis] = True
        self.var['button_forward_' + axis].setStyleSheet(f'background: rgb{YELLOW};')
        self.var['button_back_' + axis].setStyleSheet(f'background: rgb{GREY};')


    def pushed_start(self, axis):
        if not self.flags['btn_start_lock_' + axis] and self.flags['state_COM_' + axis]:
            self.flags['moving_' + axis] = True
            self.flags['move_stop_' + axis] = False
            self.flags['btn_stop_lock_' + axis] = False
            self.var['button_start_' + axis].setStyleSheet(f'background: rgb{GREEN};')
            self.var['button_stop_' + axis].setStyleSheet(f'background: rgb{GREY};')

               
    def pushed_stop(self, axis):
        if not self.flags['btn_stop_lock_' + axis]:
            self.flags['move_stop_' + axis] = True
            self.flags['moving_' + axis] = False
            self.flags['btn_start_lock_' + axis] = False
            self.var['button_start_' + axis].setStyleSheet(f'background: rgb{GREY};')
            self.var['button_stop_' + axis].setStyleSheet(f'background: rgb{RED};')


    def serial_ports(self):
        try:
            ports = serial.tools.list_ports.comports()
            connected = []
            for elem in ports:
                connected.append(elem.device)
            return connected
        except Exception:
            time.sleep(0.1)
            print('Неудалось составить список портов')


    def openCOM(self, axis):
        self.var['count_openCOM'] += 1
        self.var['name_COM_' + axis] = self.var['combobox_setCOM_' + axis].currentText()
        try:
            if self.thread_serial.ser_group['ser_' + axis].isOpen():
                self.thread_serial.ser_group['ser_' + axis].close()
            # Проверяю есть ли открытые порты с указанным именем, закрываю их
            for item in ['x', 'y', 'z']:
                if self.thread_serial.ser_group['ser_' + item].port == self.var['name_COM_' + axis]:
                    self.thread_serial.ser_group['ser_' + item].close()
                    self.flags['state_COM_' + item] = False
                    self.var['label_status_'+ item].setText('\N{Large Red Circle}')
                    self.var['label_status_' + item].setStyleSheet(f"color: rgb{RED};")
            
            # Открываю порт с указанным именем      
            self.thread_serial.init_port(self.thread_serial.ser_group['ser_' + axis], self.var['name_COM_' + axis])
            self.thread_serial.ser_group['ser_' + axis].open()
            if self.thread_serial.ser_group['ser_' + axis].isOpen():
                self.flags['state_COM_' + axis] = True
                self.var['label_status_'+ axis].setText('\N{Large Red Circle}')
                self.var['label_status_' + axis].setStyleSheet(f"color: rgb{GREEN};")
                print(self.var['combobox_setCOM_' + axis].currentText() + " открыт")
            else:
                self.flags['state_COM_' + axis] = False
                self.var['label_status_'+ axis].setText('\N{Large Red Circle}')
                self.var['label_status_' + axis].setStyleSheet(f"color: rgb{RED};")
                print(self.var['combobox_setCOM_' + axis].currentText() + " не открылся")

        except Exception:
            print(f"Error open {self.var['name_COM_' + axis]}, try:", self.var['count_openCOM'])
            time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = Main_window()
    main_win.show()
    sys.exit(app.exec())
