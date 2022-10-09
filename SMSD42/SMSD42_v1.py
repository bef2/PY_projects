import serial, time

class serial_stream:
    ser = serial.Serial()
    ser.baudrate = 9600 # Бит в секунду
    ser.bytesize = 8    # Биты данных = 8
    ser.parity   = 'E'  # Нет четности
    ser.stopbits = 1    # Стоповые биты = 1
    ser.timeout = 0.3   # Время ожидания данных чтения
    # ser.writeTimeout = 0.3
    dataOut = ''
    dataIn = ''

    def openPort(self, name_port):
        self.ser.port = name_port
        try:
            self.ser.open()
            if self.ser.isOpen():
                print('Порт', self.ser.port, 'открыт')
            else:
                print('Неудалось открыть порт', self.ser.port)
        except Exception:
            print('Ошибка при открытии порта', self.ser.port)

    def write(self, name_command):
        self.dataOut = name_command
        try:
            print('Начинаю запись:', self.dataOut)
            self.ser.write(self.dataOut.encode())
            print('Запись прошла')
        except Exception:
            print('Ошибка при записи', self.ser.port)

    def read(self):
        try:
            print('Начинаю чтение')
            self.dataIn = self.ser.read(64).decode()
            print('Чтение прошло:', self.dataIn)
        except Exception:
            print('Ошибка при чтении', self.ser.port)


if __name__ == '__main__':
    stream = serial_stream()
    print()

    stream.openPort('COM4')
    comand_word = 'DS*'
    stream.write(comand_word)
    stream.read()

    print('Конец программы')
