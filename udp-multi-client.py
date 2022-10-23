import socket
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

# The batch size is 64 KB

BATCHE_SIZE = 1024 * 36

# Define ClientMultiSocket class for receiving data from UDP server
class ClientMultiSocket (threading.Thread):
    def __init__(self, id, ip, n_clients):
        self.ip = ip
        self.id = id
        self.n_clients = n_clients
        self.client = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
        threading.Thread.__init__(self)

    def run(self):
        # Try to get data from UDP server in run
        self.client.sendto('Ready'.encode(FORMAT), ADDR)
        state_transfer = False
        while not state_transfer:
            # Recieve file from the server
            
            with open(f'client_{self.id}_file.bin', 'wb') as f:
                while True:
                    data, addr = self.client.recvfrom(BATCHE_SIZE)
                    if not data:
                        state_transfer = True
                        break
                    if addr == ADDR:
                        f.write(data)



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
        threads.append(ClientMultiSocket(id = i, ip = IP, n_clients = num_clientes))
        time.sleep(0.1)
    
    for thread in threads:
        thread.start()
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    print('All threads finished')

if __name__ == '__main__':
    main()
