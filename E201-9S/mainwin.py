'''
ui.py
Графический интерфей управления E201-9S
'''
import configparser
from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QMenuBar, QMenu, QFrame, QApplication, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox, QStatusBar, \
                            QRadioButton, QLineEdit, QTextEdit, QLabel, QAction, QSplashScreen
                            
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSlot
import sockthread
import opcthread
import comthread
import sys
import time


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.splash = QSplashScreen()
        self.image = QPixmap('D:\Code\Py\E201-9S\shield.png')
        self.splash.setPixmap(self.image)
        self.splash.show()

        self.config = configparser.ConfigParser()
        self.config.read("D:\Code\Py\E201-9S\settings.ini") # После преобразования в .exe указать другой путь

        self.setupUI()
        self.tags = [0] * 22 # Хранит значения тегов

        self.socket_thread = sockthread.MySocket(self)
        self.opc_thread = opcthread.OpcThread(self)
        self.com_thread = comthread.ComThread(self)
        self.socket_thread.start()  # запуск потока для сокета
        self.opc_thread.start()     # запуск потока для обработки OPC DA соединения
        self.com_thread.start()     # Запуск потока для обработки COM соединения
        QThread.msleep(1500)

        
    def setupUI(self):
        # Главное окно
        self.setWindowTitle("Пульт управления E201-9S")
        self.resize(1150, 720)
        self.setFont(QFont('Arial', 9))

        # Меню бар
        self.menubar = QMenuBar(self)
        file = self.menubar.addMenu("Настройки")
        self.menubar.addMenu(file)
        file.addAction("Порты")

        # Статус строка
        self.statusbar = QStatusBar(self)

        # (0) Рамка для всех виджетов
        self.frame_main = QFrame(self)

        # (1) Общие ------------------------------------------------------------
        self.gbox_general = QGroupBox('Общие', self.frame_main)
        self.gbox_general.setAlignment(Qt.AlignCenter)
 
        # (1.1) Панель упрвления
        self.gbox_remote = QGroupBox('Панель управления', self.gbox_general)
        self.btn_start = QPushButton('ЗАПУСК', self.gbox_remote)
        self.btn_start.clicked.connect(self.press_start)
        self.btn_stop = QPushButton('ОСТАНОВКА', self.gbox_remote)
        self.btn_stop.setDisabled(True)
        self.btn_stop.clicked.connect(self.press_stop)
        self.check_server = QCheckBox('Запуск сервера при старте программы', self.gbox_remote)
        self.check_server.setFont(QFont('Arial', 7))
        self.check_startup = QCheckBox('Автозагрузка программы', self.gbox_remote)
        self.check_startup.setFont(QFont('Arial', 7))
        self.layout_remote = QVBoxLayout(self.gbox_remote)
        self.layout_remote.addWidget(self.btn_start)
        self.layout_remote.addWidget(self.btn_stop)
        self.layout_remote.addWidget(self.check_server)
        self.layout_remote.addWidget(self.check_startup)

        # (1.2) Индикация обмена
        self.gbox_exchange = QGroupBox('Индикация обмена', self.gbox_general)
        self.lbl_exchange = QLabel(self.gbox_exchange)
        self.pixmap_exchange = QPixmap('D:\VSCode_projects\PY_projects\E201-9S\data_off.png')
        self.lbl_exchange.setPixmap(self.pixmap_exchange)
        self.lbl_exchange.setAlignment(Qt.AlignCenter)
        self.layout_exchange = QVBoxLayout(self.gbox_exchange)
        self.layout_exchange.addWidget(self.lbl_exchange)

        # (1.3) Сервер TCP/IP
        self.gbox_server = QGroupBox('Сервер', self.gbox_general)
        self.lbl_port = QLabel('IP', self.gbox_server)
        self.lbl_addres = QLabel('порт', self.gbox_server)
        self.layout_server = QVBoxLayout(self.gbox_server)
        self.layout_server.addWidget(self.lbl_port)
        self.layout_server.addWidget(self.lbl_addres)
        self.layout_server.setAlignment(Qt.AlignTop)

        # (1.4) Датчик линейных перемещений - COM
        self.gbox_sensor_com = QGroupBox('Датчик л/п', self.gbox_general)
        self.lbl_sensor_com = QLabel('COM#', self.gbox_sensor_com)
        self.lbl_sensor_com.setAlignment(Qt.AlignCenter)
        self.rbtn_sensor_start = QRadioButton('Вкл', self.gbox_sensor_com)
        self.rbtn_sensor_start.setChecked(True)
        self.rbtn_sensor_start.clicked.connect(lambda: self.gbox_sensor.setEnabled(True))
        self.rbtn_sensor_stop = QRadioButton('Выкл', self.gbox_sensor_com)
        self.rbtn_sensor_stop.clicked.connect(lambda: self.gbox_sensor.setEnabled(False))
        self.lbl_length = QLabel('31', self.gbox_sensor_com)
        self.lbl_length.setAlignment(Qt.AlignRight)
        self.layout_sensor_com = QVBoxLayout(self.gbox_sensor_com)
        self.layout_sensor_com.addWidget(self.lbl_sensor_com)
        self.layout_sensor_com.addWidget(self.rbtn_sensor_start)
        self.layout_sensor_com.addWidget(self.rbtn_sensor_stop)
        self.layout_sensor_com.addWidget(self.lbl_length)
        self.layout_sensor_com.setAlignment(Qt.AlignTop)

        # (1.5) Блок питания - COM
        self.gbox_supply_com = QGroupBox('Блок питания', self.gbox_general)
        self.lbl_supply_com = QLabel('COM#', self.gbox_supply_com)
        self.lbl_supply_com.setAlignment(Qt.AlignCenter)
        self.rbtn_supply_start = QRadioButton('Вкл', self.gbox_supply_com)
        self.rbtn_supply_start.setChecked(True)
        self.rbtn_supply_start.clicked.connect(lambda: self.gbox_supply.setEnabled(True))
        self.rbtn_supply_stop = QRadioButton('Выкл', self.gbox_supply_com)
        self.rbtn_supply_stop.clicked.connect(lambda: self.gbox_supply.setEnabled(False))
        self.layout_supply_com = QVBoxLayout(self.gbox_supply_com)
        self.layout_supply_com.addWidget(self.lbl_supply_com)
        self.layout_supply_com.addWidget(self.rbtn_supply_start)
        self.layout_supply_com.addWidget(self.rbtn_supply_stop)
        self.layout_supply_com.setAlignment(Qt.AlignTop)

        # (1.6) Черное тело 1 - COM
        self.gbox_blackbody_com1 = QGroupBox('Черное тело 1', self.gbox_general)
        self.lbl_blackbody_com1 = QLabel('COM#', self.gbox_blackbody_com1)
        self.lbl_blackbody_com1.setAlignment(Qt.AlignCenter)
        self.rbtn_blackbody_com1_start = QRadioButton('Вкл', self.gbox_blackbody_com1)
        self.rbtn_blackbody_com1_start.setChecked(True)
        self.rbtn_blackbody_com1_start.clicked.connect(lambda: self.gbox_blackbody1.setEnabled(True))
        self.rbtn_blackbody_com1_stop = QRadioButton('Выкл', self.gbox_blackbody_com1)
        self.rbtn_blackbody_com1_stop.clicked.connect(lambda: self.gbox_blackbody1.setEnabled(False))
        self.layout_blackbody_com1 = QVBoxLayout(self.gbox_blackbody_com1)
        self.layout_blackbody_com1.addWidget(self.lbl_blackbody_com1)
        self.layout_blackbody_com1.addWidget(self.rbtn_blackbody_com1_start)
        self.layout_blackbody_com1.addWidget(self.rbtn_blackbody_com1_stop)
        self.layout_blackbody_com1.setAlignment(Qt.AlignTop)

        # (1.7) Черное тело 2 - COM
        self.gbox_blackbody_com2 = QGroupBox('Черное тело 2', self.gbox_general)
        self.lbl_blackbody_com2 = QLabel('COM#', self.gbox_blackbody_com2)
        self.lbl_blackbody_com2.setAlignment(Qt.AlignCenter)
        self.rbtn_blackbody_com2_start = QRadioButton('Вкл', self.gbox_blackbody_com2)
        self.rbtn_blackbody_com2_start.setChecked(True)
        self.rbtn_blackbody_com2_start.clicked.connect(lambda: self.gbox_blackbody2.setEnabled(True))
        self.rbtn_blackbody_com2_stop = QRadioButton('Выкл', self.gbox_blackbody_com2)
        self.rbtn_blackbody_com2_stop.clicked.connect(lambda: self.gbox_blackbody2.setEnabled(False))
        self.layout_blackbody_com2 = QVBoxLayout(self.gbox_blackbody_com2)
        self.layout_blackbody_com2.addWidget(self.lbl_blackbody_com2)
        self.layout_blackbody_com2.addWidget(self.rbtn_blackbody_com2_start)
        self.layout_blackbody_com2.addWidget(self.rbtn_blackbody_com2_stop)
        self.layout_blackbody_com2.setAlignment(Qt.AlignTop)

        # (1) Макет - Oбщие
        self.layout_general = QHBoxLayout(self.gbox_general)
        self.layout_general.addWidget(self.gbox_remote)
        self.layout_general.addWidget(self.gbox_exchange)
        self.layout_general.addWidget(self.gbox_server)
        self.layout_general.addWidget(self.gbox_sensor_com)
        self.layout_general.addWidget(self.gbox_supply_com)
        self.layout_general.addWidget(self.gbox_blackbody_com1)
        self.layout_general.addWidget(self.gbox_blackbody_com2)
        
        # (2) Датчик линейных перемещений --------------------------------------
        self.gbox_sensor = QGroupBox('Датчик линейных перемещений', self.frame_main)
        self.gbox_sensor.setAlignment(Qt.AlignCenter)
        self.lbl_sensor_process = QLabel('Перемещение:', self.gbox_sensor)
        self.lbl_sensor_unit = QLabel('мм', self.gbox_sensor)
        self.line_sensor = QLineEdit('0.00', self.gbox_sensor)
        self.line_sensor.setAlignment(Qt.AlignCenter)
        self.line_sensor.setFont(QFont('Arial', 14))
        self.line_sensor.setReadOnly(True)
        self.layout_sensor = QHBoxLayout(self.gbox_sensor)
        self.layout_sensor.addWidget(self.lbl_sensor_process)
        self.layout_sensor.addWidget(self.line_sensor)
        self.layout_sensor.addWidget(self.lbl_sensor_unit)

        # (3) Блок питания -----------------------------------------------------
        self.gbox_supply = QGroupBox('Блок питания', self.frame_main)
        self.gbox_supply.setAlignment(Qt.AlignCenter)

        # (3.1) Канал 1
        self.gbox_channel1 = QGroupBox('Канал 1', self.gbox_supply)
        self.lbl_voltage1 = QLabel('Напряжение, В', self.gbox_channel1)
        self.lbl_amperage1 = QLabel('Сила тока, А', self.gbox_channel1)
        self.line_voltage1 = QLineEdit('0.000', self.gbox_channel1)
        self.line_voltage1.setReadOnly(True)
        self.line_amperage1 = QLineEdit('0.000', self.gbox_channel1)
        self.line_amperage1.setReadOnly(True)
        self.layout_channel1 = QGridLayout(self.gbox_channel1)
        self.layout_channel1.addWidget(self.lbl_voltage1, 0, 0)
        self.layout_channel1.addWidget(self.line_voltage1, 0, 1)
        self.layout_channel1.addWidget(self.lbl_amperage1, 1, 0)
        self.layout_channel1.addWidget(self.line_amperage1, 1, 1)
        
        # (3.2) Канал 2
        self.gbox_channel2 = QGroupBox('Канал 2', self.gbox_supply)
        self.lbl_voltage2 = QLabel('Напряжение, В', self.gbox_channel2)
        self.lbl_amperage2 = QLabel('Сила тока, А', self.gbox_channel2)
        self.line_voltage2 = QLineEdit('0.000', self.gbox_channel2)
        self.line_voltage2.setReadOnly(True)
        self.line_amperage2 = QLineEdit('0.000', self.gbox_channel2)
        self.line_amperage2.setReadOnly(True)
        self.layout_channel2 = QGridLayout(self.gbox_channel2)
        self.layout_channel2.addWidget(self.lbl_voltage2, 0, 0)
        self.layout_channel2.addWidget(self.line_voltage2, 0, 1)
        self.layout_channel2.addWidget(self.lbl_amperage2, 1, 0)
        self.layout_channel2.addWidget(self.line_amperage2, 1, 1)

        # (3.3) Канал 3
        self.gbox_channel3 = QGroupBox('Канал 3', self.gbox_supply)
        self.lbl_voltage3 = QLabel('Напряжение, В', self.gbox_channel3)
        self.lbl_amperage3 = QLabel('Сила тока, А', self.gbox_channel3)
        self.line_voltage3 = QLineEdit('0.000', self.gbox_channel3)
        self.line_voltage3.setReadOnly(True)
        self.line_amperage3 = QLineEdit('0.000', self.gbox_channel3)
        self.line_amperage3.setReadOnly(True)
        self.layout_channel3 = QGridLayout(self.gbox_channel3)
        self.layout_channel3.addWidget(self.lbl_voltage3, 0, 0)
        self.layout_channel3.addWidget(self.line_voltage3, 0, 1)
        self.layout_channel3.addWidget(self.lbl_amperage3, 1, 0)
        self.layout_channel3.addWidget(self.line_amperage3, 1, 1)

        # (3.4) Канал 4
        self.gbox_channel4 = QGroupBox('Канал 4', self.gbox_supply)
        self.lbl_voltage4 = QLabel('Напряжение, В', self.gbox_channel4)
        self.lbl_amperage4 = QLabel('Сила тока, А', self.gbox_channel4)
        self.line_voltage4 = QLineEdit('0.000', self.gbox_channel4)
        self.line_voltage4.setReadOnly(True)
        self.line_amperage4 = QLineEdit('0.000', self.gbox_channel4)
        self.line_amperage4.setReadOnly(True)
        self.layout_channel4 = QGridLayout(self.gbox_channel4)
        self.layout_channel4.addWidget(self.lbl_voltage4, 0, 0)
        self.layout_channel4.addWidget(self.line_voltage4, 0, 1)
        self.layout_channel4.addWidget(self.lbl_amperage4, 1, 0)
        self.layout_channel4.addWidget(self.line_amperage4, 1, 1)

        # (3.5) Состояние
        self.gbox_status = QGroupBox('Состояние', self.gbox_supply)
        self.lbl_status = QLabel(self.gbox_status)
        self.pixmap_status = QPixmap('D:\VSCode_projects\PY_projects\E201-9S\source_off.png')
        self.lbl_status.setPixmap(self.pixmap_status)
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.layout_status = QVBoxLayout(self.gbox_status)
        self.layout_status.addWidget(self.lbl_status)

        # (3) Макет - Блок питания
        self.layout_supply = QHBoxLayout(self.gbox_supply)
        self.layout_supply.addWidget(self.gbox_channel1)
        self.layout_supply.addWidget(self.gbox_channel2)
        self.layout_supply.addWidget(self.gbox_channel3)
        self.layout_supply.addWidget(self.gbox_channel4)
        self.layout_supply.addWidget(self.gbox_status)

        # (4) Черное тело 1 -----------------------------------------------------
        self.gbox_blackbody1 = QGroupBox('Чёрное тело 1', self.frame_main)
        self.lbl_blackbody1_temp = QLabel('Температура', self.gbox_blackbody1)
        self.lbl_blackbody1_set = QLabel('Уставка', self.gbox_blackbody1)
        self.line_blackbody1_temp = QLineEdit('0.00', self.gbox_blackbody1)
        self.line_blackbody1_temp.setReadOnly(True)
        self.line_blackbody1_set = QLineEdit('0.00', self.gbox_blackbody1)
        self.line_blackbody1_set.setReadOnly(True)
        self.layout_blackbody1 = QHBoxLayout(self.gbox_blackbody1)
        self.layout_blackbody1.addWidget(self.lbl_blackbody1_temp)
        self.layout_blackbody1.addWidget(self.line_blackbody1_temp)
        self.layout_blackbody1.addWidget(self.lbl_blackbody1_set)
        self.layout_blackbody1.addWidget(self.line_blackbody1_set)

        # (5) Черное тело 2 ----------------------------------------------------
        self.gbox_blackbody2 = QGroupBox('Чёрное тело 2', self.frame_main)
        self.lbl_blackbody2_temp = QLabel('Температура', self.gbox_blackbody2)
        self.lbl_blackbody2_set = QLabel('Уставка', self.gbox_blackbody2)
        self.line_blackbody2_temp = QLineEdit('0.00', self.gbox_blackbody2)
        self.line_blackbody2_temp.setReadOnly(True)
        self.line_blackbody2_set = QLineEdit('0.00', self.gbox_blackbody2)
        self.line_blackbody2_set.setReadOnly(True)
        self.layout_blackbody2 = QHBoxLayout(self.gbox_blackbody2)
        self.layout_blackbody2.addWidget(self.lbl_blackbody2_temp)
        self.layout_blackbody2.addWidget(self.line_blackbody2_temp)
        self.layout_blackbody2.addWidget(self.lbl_blackbody2_set)
        self.layout_blackbody2.addWidget(self.line_blackbody2_set)

        # (6) Информация -------------------------------------------------------
        self.gbox_info = QGroupBox('Информация', self.frame_main)
        self.gbox_info.setAlignment(Qt.AlignCenter)
        self.text_info = QTextEdit(self.gbox_info)
        self.text_info.setReadOnly(True)
        self.layout_info = QVBoxLayout(self.gbox_info)
        self.layout_info.addWidget(self.text_info)

        # (0) Макет общей рамки ------------------------------------------------
        self.layout_main = QVBoxLayout(self.frame_main)
        self.layout_main.addWidget(self.gbox_general)
        self.layout_main.addWidget(self.gbox_sensor)
        self.layout_main.addWidget(self.gbox_supply)
        self.layout_main.addWidget(self.gbox_blackbody1)
        self.layout_main.addWidget(self.gbox_blackbody2)
        self.layout_main.addWidget(self.gbox_info)

        # Макет главного окна
        self.layout_root = QVBoxLayout(self)
        self.layout_root.setSpacing(0)
        self.layout_root.setContentsMargins(0,0,0,0)
        self.layout_root.addWidget(self.menubar)
        self.layout_root.addWidget(self.frame_main)
        self.layout_root.addWidget(self.statusbar)


    @pyqtSlot()
    def press_start(self):
        self.opc_thread.work = True     # Переводит поток в рабочий режим


    @pyqtSlot()    
    def press_stop(self):
        self.opc_thread.work = False    # Переводит поток в ждущий режим


    @pyqtSlot(bool)
    def toggle_button(self, flag):
        if flag == True:
            self.btn_start.setEnabled(False) # Блокирование кнопоки старт
            self.btn_stop.setEnabled(True)   # активация кнопоки стоп
        else:
            self.btn_start.setEnabled(True) # активация кнопоки старт
            self.btn_stop.setEnabled(False) # Блокирование кнопоки стоп


    # @pyqtSlot(str)
    # def edit_info(self, text):
    #     self.text_info.setText(text)


    @pyqtSlot()
    def set_lbl_server(self):
        self.lbl_port.setText('IP: ' + self.config["Server"]["ip"])
        self.lbl_addres.setText('порт: ' + self.config["Server"]["port"])


    @pyqtSlot(int, float)
    def set_tags(self, num, val):
        self.tags[num] = val


    @pyqtSlot()
    def set_line_voltage(self):
        self.line_voltage1.setText(str(self.tags[10]))
        self.line_voltage2.setText(str(self.tags[12]))
        self.line_voltage3.setText(str(self.tags[14]))
        self.line_voltage4.setText(str(self.tags[16]))


    @pyqtSlot()
    def set_line_amperage(self):
        self.line_amperage1.setText(str(self.tags[11]))
        self.line_amperage2.setText(str(self.tags[13]))
        self.line_amperage3.setText(str(self.tags[15]))
        self.line_amperage4.setText(str(self.tags[17]))


    @pyqtSlot(bool)
    def set_lbl_exchange(self, flag):
        if flag:
            pixmap = QPixmap('D:\VSCode_projects\PY_projects\E201-9S\data_on.png')
            self.lbl_exchange.setPixmap(pixmap)
        else:
            pixmap = QPixmap('D:\VSCode_projects\PY_projects\E201-9S\data_off.png')
            self.lbl_exchange.setPixmap(pixmap)


    @pyqtSlot(bool)
    def set_lbl_status(self, flag):
        if flag:
            pixmap = QPixmap('D:\VSCode_projects\PY_projects\E201-9S\source_on.png')
            self.lbl_status.setPixmap(pixmap)
        else:
            pixmap = QPixmap('D:\VSCode_projects\PY_projects\E201-9S\source_off.png')
            self.lbl_status.setPixmap(pixmap)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.splash.finish(win) # Конец показа заставки
    sys.exit(app.exec())
