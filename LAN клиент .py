import socket
import time

TCP_IP = "192.168.0.132"
TCP_PORT = 5000
BUFFER_SIZE = 256

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    # print("CONNECTED: ", s)
    send_dt = "dt\r\n"
    s.send(send_dt.encode())
    print('SEND:', send_dt)
    recv_dt = s.recv(BUFFER_SIZE).decode('cp1251')
    s.close()
    print("RECIEVE:", recv_dt)
    dead_time = int(recv_dt.split()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    send_data = "allsensors\r\n"
    s.send(send_data.encode())
    print('SEND:', send_data)
    recv_data = s.recv(BUFFER_SIZE).decode()
    s.close()
    print("RECIEVE:", recv_data)
    print('DEAD TIME:', dead_time)
    
    sens_lst = recv_data.split()
    print('SENSOR 1:', sens_lst[4])
    time.sleep(dead_time)
