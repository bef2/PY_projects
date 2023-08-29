'''
opcthread.py
Поток для взаимодействия OPC соединения и графического интерфейса управления E201-9S
'''
import opcclient
from PyQt5.QtCore import QThread, pyqtSignal
from copy import copy
import time


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


class OpcThread(QThread):

    # edit_info_signal = pyqtSignal(str)
    toggle_button = pyqtSignal(bool)
    set_tags = pyqtSignal(int, float)
    set_lbl_exchange = pyqtSignal(bool)

    def __init__(self, ui=None):
        print("Поток OPC создан")
        super().__init__()
        self.ui = ui

        self.status = False # Начало/конец потока
        self.stay = False   # Ждущий режим потока
        self.work = False   # Рабочий режим потока

        # self.edit_info_signal.connect(self.ui.edit_info)
        self.toggle_button.connect(self.ui.toggle_button)
        self.set_tags.connect(self.ui.set_tags)
        self.set_lbl_exchange.connect(self.ui.set_lbl_exchange)


    # Запуск потока
    def run(self):
        print("Начало потока OPC")
        self.status = True
        self.stay = True
        self.work = False
        client = opcclient.OPCclient()
        opc_tags = [0] * 22

        # Ждущий цикл потока
        while self.stay:
            self.toggle_button.emit(False)
            self.set_lbl_exchange.emit(False)
            
            # Рабочий цикл потока
            while self.work:
                self.toggle_button.emit(True)
                self.set_lbl_exchange.emit(True)

                # Чтение тегов 
                try:
                    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        val = client.read(i)
                        self.set_tags.emit(i, val)
                except Exception:
                    print("Ошибка OPC: чтение тегов, проверьте соединение с сервером")
                    self.work = False
                    self.toggle_button.emit(False)
                    client = opcclient.OPCclient()
                
                # Запись в теги
                try:
                    for i in [10, 11, 12, 13, 14, 15, 16, 17]:
                        if opc_tags[i] != self.ui.tags[i]:
                            opc_tags[i] = copy(self.ui.tags[i])
                            client.write(i, opc_tags[i])
                except Exception:
                    print("Ошибка OPC: запись в теги, проверьте соединение с сервером")
                    self.work = False
                    self.toggle_button.emit(False)
                    client = opcclient.OPCclient()
                    
                time.sleep(0.2)
            time.sleep(0.5)

        # Конец потока
        self.status = False
        print("Конец потока OPC")
