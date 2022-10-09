import serial

ComPort = serial.Serial('COM15') # открыть COM15
ComPort.baudrate = 9600 # Бит в секунду
ComPort.bytesize = 8    # Биты данных = 8
ComPort.parity   = 'N'  # Нет четности
ComPort.stopbits = 1    # Стоповые биты = 1

data = "001M^\r"        # Команда по протоколу "Erstevak" в кодировке ASCII

dataOut = ComPort.write(data.encode())    # Запись данных

print(data)                      # Вывод в консоль отправленных данных
dataIn = ComPort.read(12)        # Ожидание и чтение данных
print(dataIn.decode())           # Вывод в консоль принятых данных

ComPort.close()         # Закрыть Com port