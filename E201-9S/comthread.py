'''
comthread.py
Поток для взаимодействия COM соединения и графического интерфейса управления E201-9S
'''

import serial
from PyQt5.QtCore import QThread, pyqtSignal
import time
from copy import copy 


"""
Запись:
0 "linear_sensor"
10 "voltage_ch1_actual"
11 "amperage_ch1_actual"
12 "voltage_ch2_actual"
13 "amperage_ch2_actual"
14 "voltage_ch3_actual"
15 "amperage_ch3_actual"
16 "voltage_ch4_actual"
17 "amperage_ch4_actual" 
18 "blackbody1_temp" 
20 "blackbody2_temp"

Чтение:
1 "voltage_ch1" 
2 "amperage_ch1"
3 "voltage_ch2"
4 "amperage_ch2" 
5 "voltage_ch3"
6 "amperage_ch3"
7 "voltage_ch4"
8 "amperage_ch4"
9 "powerout"
19 "blackbody1_set"
21 "blackbody2_set"
"""


class ComThread(QThread):
    set_line_voltage = pyqtSignal()
    set_line_amperage = pyqtSignal()
    set_lbl_status = pyqtSignal(bool)


    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.status = False
        self.stay = False
        self.work = False
        self.source = serial.Serial()
        self.init_com(self.source)
        self.com_tags = [0] * 22

        self.set_line_voltage.connect(self.ui.set_line_voltage)
        self.set_line_amperage.connect(self.ui.set_line_amperage)
        self.set_lbl_status.connect(self.ui.set_lbl_status)


    def init_com(self, com):
        com.port = self.ui.config["Source"]["port"]                 # Имя порта
        com.baudrate = int(self.ui.config["Source"]["baudrate"])    # Бит в секунду
        com.bytesize = int(self.ui.config["Source"]["bytesize"])    # Биты данных = 8
        com.parity = self.ui.config["Source"]["parity"]             # Нет четности
        com.stopbits = int(self.ui.config["Source"]["stopbits"])    # Стоповые биты = 1
        com.timeout = 0.3   # Время ожидания данных чтения
        com.open()
        self.ui.lbl_supply_com.setText(com.port) # Отображаем имя порта в интерфейсе


    # Запуск потока
    def run(self):
        print("Начало потока COM")
        self.status = True
        self.stay = True
        self.work = True

        # Ждущий цикл потока
        while self.stay:

            # Рабочий цикл потока
            while self.work:
                

                try:
                    # Чтение актуальных напряжений и токов 1-4 каналов
                    for tag, chan in [(10, 1), (12, 2), (14, 3), (16, 4)]:
                        self.source.write(f"VOUT{chan}?\n".encode())
                        data_read = self.source.read(32).decode()
                        self.ui.tags[tag] = float(data_read.replace('V', ''))
                        if self.com_tags[tag] != self.ui.tags[tag]:
                            self.com_tags[tag] = copy(self.ui.tags[tag])

                        self.source.write(f"IOUT{chan}?\n".encode())
                        data_read = self.source.read(32).decode()
                        self.ui.tags[tag+1] = float(data_read.replace('A', ''))
                        if self.com_tags[tag+1] != self.ui.tags[tag+1]:
                            self.com_tags[tag+1] = copy(self.ui.tags[tag+1])


                    # Обновление значений напряжений и токов 1-4 каналов в интерфейсе
                    self.set_line_voltage.emit()
                    self.set_line_amperage.emit()


                    # Чтение регистра Выход питания
                    if self.com_tags[9] != self.ui.tags[9]:
                        self.com_tags[9] = copy(self.ui.tags[9])
                        if self.com_tags[9] == True:
                            self.source.write("OUT1\n".encode())
                            # Проверка включения выхода
                            self.source.write("STATUS?\n".encode())
                            answer = self.source.read(16).decode()
                            if "11010110" in answer:
                                self.set_lbl_status.emit(True)
                        else:
                            self.source.write("OUT0\n".encode())
                            # Проверка выключения выхода
                            self.source.write("STATUS?\n".encode())
                            answer = self.source.read(16).decode()
                            if "00010010" in answer:
                                self.set_lbl_status.emit(False)
                

                    # Чтение уставок напряжений и токов 1-4 каналов
                    for tag, chan in [(1, 1), (3, 2), (5, 3), (7, 4)]:
                        if self.com_tags[tag] != self.ui.tags[tag]:
                            self.com_tags[tag] = copy(self.ui.tags[tag])
                            self.source.write(f"VSET{chan}:{self.com_tags[tag]}\n".encode())

                        if self.com_tags[tag+1] != self.ui.tags[tag+1]:
                            self.com_tags[tag+1] = copy(self.ui.tags[tag+1])
                            self.source.write(f"ISET{chan}:{self.com_tags[tag+1]}\n".encode())


                except Exception:
                    print("Ошибка COM: чтение данных")

                time.sleep(0.2)

            time.sleep(0.5)   
        self.status = False
        