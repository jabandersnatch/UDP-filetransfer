# This is the script for the server side of the file transfer program
# Author: Juan Andrés Méndez, Jesus David Barrios, Sergio Esteban Peñuela

import socket
import sys
import logging
import time
import os

'''
The connection will be made via UDP sockets
'''

## IP and port of the server note that the port must support UDP
IP = 'localhost'
PORT = 5000 
ADDR = (IP, PORT)
FORMAT = 'utf-8'

## The files to be sent
FILE_100MB = '100MB.bin'
FILE_250MB = '250MB.bin'
FILESIZE_100MB = os.path.getsize(FILE_100MB)
FILESIZE_250MB = os.path.getsize(FILE_250MB)

# Get file size from console
file_size = int(input("Ingrese el tamaño del archivo (100,250): "))

# Create a UDP sockets
server = None
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
        
# Bind the socket to the PORT
try:
    server.bind(ADDR)
except socket.error:
    print('Bind failed')
    sys.exit()

print('SERVER STARTED AT PORT: ', PORT)

def main():
    logging.basicConfig(filename=f'{time.strftime("%Y%m%d-%H%M%S")}'+'-log.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

    while True:
        data, addr = server.recvfrom(1024)
        logging.info(f'Client connected: {addr}')
        print('Client connected: ', addr)
        if data:
            if data == b'100MB':
                logging.info(f'Client requested 100MB file')
                send_file(FILE_100MB, FILESIZE_100MB, addr)
            elif data == b'250MB':
                logging.info(f'Client requested 250MB file')
                send_file(FILE_250MB, FILESIZE_250MB, addr)
            else:
                logging.info(f'Client requested unknown file')
                print('Unknown file requested')
                server.sendto(b'Unknown file requested', addr)
        else:
            logging.info(f'Client disconnected')
            print('Client disconnected')

def send_file(file, size, addr):
    # Send the file size
    server.sendto(str(size).encode(FORMAT), addr)
    # Send the file hash
    server.sendto(generate_hash(file), addr)
    # Send the file
    with open(file, 'rb') as f:
        data = f.read(1024)
        while data:
            if server.sendto(data, addr):
                data = f.read(1024)
    print('File sent')

    

def generate_hash(file):
    import hashlib
    with open(file, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash.encode(FORMAT)

if __name__ == '__main__':
    main()


