import socket
from PyQt5.QtCore import QThread, pyqtSignal
# import time


class MySocket(QThread):
    set_lbl_server_signal = pyqtSignal()

    def __init__(self, ui=None):
        super().__init__()
        self.ui = ui
        self.ip = self.ui.config["Server"]["ip"]
        self.port = int(self.ui.config["Server"]["port"])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.set_lbl_server_signal.connect(self.ui.set_lbl_server)


    def run(self):
        self.set_lbl_server_signal.emit()
        while True:
            print(f"Cокет: {self.ip}, порт {self.port}\n")
            self.sock.listen(1)
            conn, addr = self.sock.accept()






    # def __init__(self, ui=None):
    #     super().__init__()
    #     self.ui = ui
    #     self.status = False
    #     self.stay = False
    #     self.work = False
    #     self.ip = self.ui.config["Server"]["ip"]
    #     self.port = int(self.ui.config["Server"]["port"])
    #     while True:
    #         try:
    #             self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             self.sock.bind((self.ip, self.port))
    #             break
    #         except Exception:
    #             # time.sleep(0.1)
    #             pass
    #     self.set_lbl_server_signal.connect(self.ui.set_lbl_server)


    # # Запуск потока
    # def run(self):
    #     self.status = True
    #     self.stay = True
    #     self.work = True
    #     self.set_lbl_server_signal.emit()

    #     # Ждущий цикл потока
    #     while self.stay:

    #         # Рабочий цикл потока
    #         while self.work:
    #             print("-------------------------------------------")
    #             print(f"Создан сокет: {self.ip}, порт {self.port}")
    #             self.sock.listen(5)
    #             conn, addr = self.sock.accept()

    #         time.sleep(0.2)

    #     # Конец потока
    #     self.status = False
    #     print("Поток sockthread остановлен")
