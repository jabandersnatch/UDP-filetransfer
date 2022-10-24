import socket
import os
import threading
import logging
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
NUM_TEST = 5

# The batch size is 64 KB

BATCHE_SIZE = 1024 * 8
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
        start = time.time()
        while not state_transfer:
            
            with open(f'./ArchivosRecibidos/client_{self.id}_prueba_{NUM_TEST}.txt', 'wb') as f:
                while True:
                    data, addr = self.client.recvfrom(BATCHE_SIZE)
                    if not data:
                        state_transfer = True
                        break
                    if addr == ADDR:
                        f.write(data)
        end = time.time()

        transferenciaExitosa = False
        # Verify if created file has the same size of the original file
        if os.path.getsize(f'./ArchivosRecibidos/client_{self.id}_prueba_{NUM_TEST}.txt') == FILESIZE_100MB or os.path.getsize(f'./ArchivosRecibidos/client_{self.id}_prueba_{NUM_TEST}.txt') == FILESIZE_250MB:
            transferenciaExitosa = True

        # log the information of the client
        logging.info(f'Client_id: {str(self.id)}, client address: {self.client.getsockname()}, successful transfer: {str(transferenciaExitosa)},  transference time: {str(end-start)} segs, file size: {str(os.path.getsize(f"./ArchivosRecibidos/client_{self.id}_prueba_{NUM_TEST}.txt"))}B')

def main():
    
    numero_clientes_definido = False
    while not numero_clientes_definido:
        num_clients = input('Number of clients (1, 5, 10, 25): ')
        if num_clients == '1' or num_clients == '5' or num_clients == '10' or num_clients == '25':
            num_clientes = int(num_clients)
            numero_clientes_definido = True
        else:
            print('Invalid number of clients')

    # Create log file for each client
    logging.basicConfig(filename=f'./Logs/{time.strftime("%Y-%m-%d-%H-%M-%S")}_{NUM_TEST}_prueba-log.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


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
