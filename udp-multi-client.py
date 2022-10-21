import socket
import sys
import os
import threading
import time

IP = '192.168.1.100'
PORT = 5000
ADDR = (IP, PORT)
FORMAT = 'utf-8'

# The files to be sent
FILE_100MB = '100MB.bin'
FILE_250MB = '250MB.bin'
FILESIZE_100MB = os.path.getsize(FILE_100MB)
FILESIZE_250MB = os.path.getsize(FILE_250MB)

# Define ClientMultiSocket class for receiving data from UDP server
class ClientMultiSocket:
    def __init__(self, ip, port, id, n_clients):
        self.ip = ip
        self.port = port
        self.id = id
        self.n_clients = n_clients
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((self.ip, self.port))
        self.client.setblocking(False)

    def run(self):
        # Try to get data from UDP server in run
        while True:
            try:
                data, addr = self.client.recvfrom(1024)
                print(data)
            except:
                pass

    def run(self):
        self.receive_thread.join()


def main():
    
    numero_clientes_definido = False
    while not numero_clientes_definido:
        num_clients = input('Number of clients (1, 5, 10, 25): ')
        if num_clients == '1' or num_clients == '5' or num_clients == '10' or num_clients == '25':
            num_clientes = int(num_clients)
            numero_clientes_definido = True
        else:
            print('Invalid number of clients')

    threads = []
    for i in range(num_clientes):
        print('Creating client ', i)
        threads.append(ClientMultiSocket(IP,PORT,i,num_clientes))
        time.sleep(0.1)
    
    for thread in threads:
        thread.start()
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    print('All threads finished')

if __name__ == '__main__':
    main()
